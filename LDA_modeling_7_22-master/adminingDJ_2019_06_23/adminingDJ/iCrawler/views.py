from uuid import uuid4
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from .models import NaverBlog, MyCollection, MyCollectionStats, MyCollectionDetail, MyKeyword, Twitter, NaverNews, DaumBlog
from .forms import CollectingForm
from django.db.models import Max, Count
from .aggregates import Concat
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
import urllib
import pandas as pd
import sys
from django.db.models import Q

import csv
import xlwt

# Create your views here.
scrapyd = ScrapydAPI('http://localhost:6800')


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def index(request):
    form = CollectingForm()
    return render(request, "icrawler/index.html", {"form": form})


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def crawl(request):
    if request.method == "POST":

        keywords = request.POST.get("key_words", None)
        if keywords is None:
            return JsonResponse({'error': 'Select keywords'})

        keywords = collectKeyWords(keywords)
        print(keywords)
        

        unique_id = str(uuid4())

        mediaName_bc = request.POST.getlist('mediaName_bc', [])
        mediaName_pn = request.POST.getlist('mediaName_pn', [])
        mediaName_bl = request.POST.getlist('mediaName_bl', [])
        mediaName_sc = request.POST.getlist('mediaName_sc', [])

        term = request.POST.get('term', None)
        termStart, termEnd = term.split(' - ', 1)

        coll = MyCollection()
        coll.unique_id = unique_id
        coll.search_keyword = keywords
        coll.channel_broadcast = ','.join(mediaName_bc)
        coll.channel_published = ','.join(mediaName_pn)
        coll.channel_blog = ','.join(mediaName_bl)
        coll.channel_sns = ','.join(mediaName_sc)
        coll.start_date = termStart
        coll.end_date = termEnd

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')
        useragent = request.META['HTTP_USER_AGENT']
        coll.user_ip = ipaddress
        coll.user_agent = useragent

        coll.save()

        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': useragent
        }

        if len(mediaName_sc) > 0:
            scrapyd.schedule("default", "twitter",
                             settings=settings, uid=unique_id, keyword=keywords, termStart=termStart, termEnd=termEnd)

        if len(mediaName_bl) > 0:
            if 'naver' in mediaName_bl:
                scrapyd.schedule("default", "naver_blog", keyword=keywords,
                                 settings=settings, uid=unique_id, termStart=termStart, termEnd=termEnd)

            if 'daum' in mediaName_bl:
                scrapyd.schedule("default", "daum_blog", keyword=keywords,
                                 settings=settings, uid=unique_id, termStart=termStart, termEnd=termEnd)

        if len(mediaName_bc) > 0 or len(mediaName_pn) > 0:
            scrapyd.schedule("default", "naver_news", settings=settings, keyword=keywords,
                             broadcasts=mediaName_bc, uid=unique_id, newspapers=mediaName_pn, termStart=termStart, termEnd=termEnd)

        return HttpResponseRedirect(reverse('ic_collected'))
    elif request.method == "GET":
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({"error": "Missing args"})

        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                item = NaverBlog.objects.get(unique_id=unique_id)
                return JsonResponse({'status': status, 'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})


def getScrapydAPI(path, postData=None):
    url = "http://localhost:6800/" + path

    if postData is not None:
        try:
            data = requests.post(url=url, data=postData).json()
            return data
        except Exception as e:
            return json.dumps({"error": str(e)})

    try:
        data = requests.get(url).json()
        return data
    except Exception as e:
        return json.dumps({"error": str(e)})


def collectedData(request):
    data = MyCollection.objects.all().values('id', 'unique_id', 'search_keyword', 'channel_broadcast', 'channel_published', 'channel_blog', 'channel_sns', 'start_date', 'end_date', 'created_date', 'jobids', 'status').annotate(stats=Count('mycollectionstats')).order_by('-created_date')[:10]

    dtJS = getScrapydAPI('listjobs.json?project=default')
    pending_jobs = dtJS['pending']
    running_jobs = dtJS['running']


    for i in range(len(data)):
        status = data[i]['status']
        if status == 'finished':
            id = data[i]['id']
            details = MyCollectionDetail.objects.filter(collection_id=id)

            tweetIds = []
            naverNewsIds = []
            naverBlogIds = []
            daumBlogIds = []
            for det in details:
                if det.twitter_id:
                    tweetIds.append(det.twitter_id)
                if det.naver_news_id:
                    naverNewsIds.append(det.naver_news_id)
                if det.naver_blog_id:
                    naverBlogIds.append(det.naver_blog_id)
                if det.daum_blog_id:
                    daumBlogIds.append(det.daum_blog_id)

            totalSize = 0
            totalRows = 0
            if len(tweetIds) > 0:
                twitters = Twitter.objects.filter(id__in=tweetIds).values('search_keyword', 'content')
                dataFrame = pd.DataFrame(list(twitters))
                totalSize += physicalVolumeBytes(dataFrame)
                totalRows += len(twitters)

            if len(naverNewsIds) > 0:
                news = NaverNews.objects.filter(id__in=naverNewsIds).values('search_keyword', 'title', 'content')
                dataFrame = pd.DataFrame(list(news))
                totalSize += physicalVolumeBytes(dataFrame)
                totalRows += len(news)
            
            if len(naverBlogIds) > 0:
                blogN = NaverBlog.objects.filter(id__in=naverBlogIds).values('search_keyword', 'title', 'content')
                dataFrame = pd.DataFrame(list(blogN))
                totalSize += physicalVolumeBytes(dataFrame)
                totalRows += len(blogN)
            
            if len(daumBlogIds) > 0:
                blogD = DaumBlog.objects.filter(id__in=daumBlogIds).values('search_keyword', 'title', 'content')
                dataFrame = pd.DataFrame(list(blogD))
                totalSize += physicalVolumeBytes(dataFrame)
                totalRows += len(blogD)
            
            data[i]['stats'] = totalRows
            data[i]['size'] = physicalSize(totalSize)
        else:
            uid = data[i]['unique_id']
            collect = MyCollection.objects.get(unique_id=uid)
            if collect:
                jids = []
                try:
                    jids = data[i]['jobids'].split(' ')
                except:
                    jids = []

                found = 'finished'
                for jid in jids:
                    for job in pending_jobs:
                        if job['id'] == jid:
                            found = 'running'
                            break

                    if found == 'finished':
                        for job in running_jobs:
                            if job['id'] == jid:
                                found = 'running'
                                break
                collect.status = found
                collect.save()
                    
            
        
    return render(request, "icrawler/collected.html", {
        'documents': data
    })


def collectedDetailData(request, id):
    collection = MyCollection.objects.get(id=id)

    details = MyCollectionDetail.objects.filter(collection_id=id)

    htmlParams = {}
    htmlParams['blogs'] = []
    htmlParams['news'] = []
    htmlParams['sns'] = []

    tweetIds = []
    naverNewsIds = []
    naverBlogIds = []
    daumBlogIds = []
    for det in details:
        if det.twitter_id:
            tweetIds.append(det.twitter_id)
        if det.naver_news_id:
            naverNewsIds.append(det.naver_news_id)
        if det.naver_blog_id:
            naverBlogIds.append(det.naver_blog_id)
        if det.daum_blog_id:
            daumBlogIds.append(det.daum_blog_id)

    print('t', tweetIds)
    print('nn', naverNewsIds)
    print('nb', naverBlogIds)
    print('db', daumBlogIds)

    totalSize = 0
    totalRows = 0
    if len(tweetIds) > 0:
        twitters = Twitter.objects.filter(id__in=tweetIds).values('search_keyword', 'content')
        dataFrame = pd.DataFrame(list(twitters))
        size = physicalVolumeBytes(dataFrame)
        totalSize += size
        rows = len(twitters)
        totalRows += rows
        htmlParams['sns'].append({'name': 'Twitter', 'size': physicalSize(size), 'rows': rows})

    if len(naverNewsIds) > 0:
        news = NaverNews.objects.filter(id__in=naverNewsIds).values('search_keyword', 'title', 'content')
        dataFrame = pd.DataFrame(list(news))


        size = physicalVolumeBytes(dataFrame)
        totalSize += size
        rows = len(news)
        totalRows += rows

        htmlParams['news'].append({'name': 'Naver', 'size': physicalSize(size), 'rows': rows})
    
    if len(naverBlogIds) > 0:
        blogN = NaverBlog.objects.filter(id__in=naverBlogIds).values('search_keyword', 'title', 'content')
        dataFrame = pd.DataFrame(list(blogN))
        size = physicalVolumeBytes(dataFrame)
        totalSize += size
        rows = len(blogN)
        totalRows += rows

        htmlParams['blogs'].append({'name': 'Naver', 'size': physicalSize(size), 'rows': rows})
    
    if len(daumBlogIds) > 0:
        blogD = DaumBlog.objects.filter(id__in=daumBlogIds).values('search_keyword', 'title', 'content')
        dataFrame = pd.DataFrame(list(blogD))
        size = physicalVolumeBytes(dataFrame)
        totalSize += size
        rows = len(blogD)
        totalRows += rows
        htmlParams['blogs'].append({'name': 'Daum', 'size': physicalSize(size), 'rows': rows})
    
    print(htmlParams['news'])

    htmlParams['collection'] = collection
    htmlParams['stats'] = ''
    htmlParams['cid'] = id

    return render(request, 'icrawler/collected_detail.html', htmlParams)


def collectKeyWords(keywords):
    examples = keywords.split(',')
    newWords = []

    s_ws = []
    s_is = []
    for example in examples:
        try:
            word = MyKeyword.objects.get(search_word=example)
            if word.id:
                s_is.append(word.id)
            if word.parent_id:
                s_is.append(word.parent_id)
            if word.id:
                s_ws.append(word.search_word)
        except ObjectDoesNotExist:
            newWords.append(example)
    
    words = MyKeyword.objects.filter(Q(search_word__in=s_ws) | Q(parent_id__in=s_is) | Q(id__in=s_is))
    for w in words:
        newWords.append(w.search_word)
    
    return ','.join(newWords)

def physicalVolumeBytes(df):
    size = sys.getsizeof(df)
    return round(size, 2)

def physicalSize(size):
    sizeName = 'bytes'
    if size >= 1024:
        sizeName = 'KB'
        size = size / 1024

    if size >= 1024:
        sizeName = 'MB'
        size = size / 1024

    if size >= 1024:
        sizeName = 'GB'
        size = size / 1024
    return '{} {}'.format(round(size, 2), sizeName)

def physicalVolume(df):
    sizeName = 'bytes'
    size = sys.getsizeof(df)

    if size >= 1024:
        sizeName = 'KB'
        size = size / 1024

    if size >= 1024:
        sizeName = 'MB'
        size = size / 1024

    if size >= 1024:
        sizeName = 'GB'
        size = size / 1024

    return '{} {}'.format(round(size, 2), sizeName)


def categorizeChannel(mediaStr):
    mediaStr = removeDuplicate(mediaStr)

    socialList = ['twitter']
    bcList = ["뉴시스", "SBS 뉴스", "MBC 뉴스", "YTN", "MBN", "한국경제TV", "SBS CNBC","뉴스1","채널A","enews24","KBS 연예","JTBC","KBS 뉴스","SBS funE","연합뉴스TV","TV조선","채널A"]
    pnList = ["신동아", "TV리포트", "연합뉴스", "동아일보", "SBS", "헤럴드POP", "조세일보","헤럴드경제","경향신문","한겨례", "노컷뉴스","중앙일보","한국일보","머니투데이","주간경향","문화일보","부산일보","세계일보","스포츠서울","데일리안","헤럴드경제","헬스조선"]
    blList = ['naver', 'daum']

    socials = []
    bcs = []
    pns = []
    bls = []

    datas = set(mediaStr.split(','))
    for d in datas:
        if d in socialList:
            socials.append(d)
            continue
        if d in bcList:
            bcs.append(d)
            continue
        if d in pnList:
            pns.append(d)
            continue
        if d in blList:
            bls.append(d)
            continue
    
    channels = ''
    if len(socials) > 0:
        channels += 'SNS (' + ','.join(socials) + '),'
    if len(bcs) > 0:
        channels += ' 방송뉴스 (' + ','.join(bcs) + '),'
    
    if len(pns) > 0:
        channels += ' 신문뉴스 (' + ','.join(pns) + '),'
    if len(bls) > 0:
        channels += ' 블로그 (' + ','.join(bls) + '),'
    
    return channels




def removeDuplicate( dataStr):
    datas = set(dataStr.split(','))
    return ','.join(datas)


def exportCsv(request):

    ids = request.GET.getlist('uid')
    if len(ids) <= 0:
        return HttpResponse()

    filename = ids[0]

    # response = HttpResponse() 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)

    try:
        writer = csv.writer(response)
        writer.writerow(['keyword', 'Title', 'Content'])

        # collection = MyCollectionStats.objects.filter(collection_id__in=ids).values_list('search_keyword', 'title', 'content')
        details = MyCollectionDetail.objects.filter(collection_id__in=ids)
        
        tweetIds = []
        naverNewsIds = []
        naverBlogIds = []
        daumBlogIds = []
        for det in details:
            if det.twitter_id:
                tweetIds.append(det.twitter_id)
            if det.naver_news_id:
                naverNewsIds.append(det.naver_news_id)
            if det.naver_blog_id:
                naverBlogIds.append(det.naver_blog_id)
            if det.daum_blog_id:
                daumBlogIds.append(det.daum_blog_id)

        if len(tweetIds) > 0:
            twitters = Twitter.objects.filter(id__in=tweetIds).values_list('search_keyword', 'username', 'content')
            for ob in twitters:
                writer.writerow([ob['search_keyword'], ob['username'], ob['content']])
            

        if len(naverNewsIds) > 0:
            news = NaverNews.objects.filter(id__in=naverNewsIds).values('search_keyword', 'title', 'content')
            for ob in news:
                writer.writerow([ob['search_keyword'], ob['title'], ob['content']])
        
        if len(naverBlogIds) > 0:
            blogN = NaverBlog.objects.filter(id__in=naverBlogIds).values('search_keyword', 'title', 'content')
            for ob in blogN:
                writer.writerow([ob['search_keyword'], ob['title'], ob['content']])
            
        
        if len(daumBlogIds) > 0:
            blogD = DaumBlog.objects.filter(id__in=daumBlogIds).values('search_keyword', 'title', 'content')
            for ob in blogD:
                writer.writerow([ob['search_keyword'], ob['title'], ob['content']])
           

    except Exception as e:
        print('Error CSV',  str(e))
    finally:
        return response

def exportXls(request):

    ids = request.GET.getlist('uid')
    if len(ids) <= 0:
        return HttpResponse()


    filename = ids[0]

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(filename)

    try:
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Data')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['keyword', 'Title', 'Content']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # collection = MyCollectionStats.objects.filter(collection_id__in=ids).values_list( 'search_keyword', 'title', 'content')

        details = MyCollectionDetail.objects.filter(collection_id__in=ids)
        
        tweetIds = []
        naverNewsIds = []
        naverBlogIds = []
        daumBlogIds = []
        for det in details:
            if det.twitter_id:
                tweetIds.append(det.twitter_id)
            if det.naver_news_id:
                naverNewsIds.append(det.naver_news_id)
            if det.naver_blog_id:
                naverBlogIds.append(det.naver_blog_id)
            if det.daum_blog_id:
                daumBlogIds.append(det.daum_blog_id)

        if len(tweetIds) > 0:
            twitters = Twitter.objects.filter(id__in=tweetIds).values_list('search_keyword', 'username', 'content')
            for ob in twitters:
                row_num += 1
                for col_num in range(len(ob)):
                    content = ob[col_num]
                    if content is not None:
                        content = content[:32766]
                    ws.write(row_num, col_num, content, font_style)
            

        if len(naverNewsIds) > 0:
            news = NaverNews.objects.filter(id__in=naverNewsIds).values_list('search_keyword', 'title', 'content')
            for ob in news:
                row_num += 1
                for col_num in range(len(ob)):
                    content = ob[col_num]
                    if content is not None:
                        content = content[:32766]
                    ws.write(row_num, col_num, content, font_style)
        
        if len(naverBlogIds) > 0:
            blogN = NaverBlog.objects.filter(id__in=naverBlogIds).values_list('search_keyword', 'title', 'content')
            for ob in blogN:
                row_num += 1
                for col_num in range(len(ob)):
                    content = ob[col_num]
                    if content is not None:
                        content = content[:32766]
                    ws.write(row_num, col_num, content, font_style)
            
        
        if len(daumBlogIds) > 0:
            blogD = DaumBlog.objects.filter(id__in=daumBlogIds).values_list('search_keyword', 'title', 'content')
            for ob in blogD:
                row_num += 1
                for col_num in range(len(ob)):
                    content = ob[col_num]
                    if content is not None:
                        content = content[:32766]
                    ws.write(row_num, col_num, content, font_style)
        
        wb.save(response)
    except Exception as e:
        print('Error XLS',  str(e))
    finally:
        return response

def visualization(request, nm):

    js_data = None
    chartData = []
    if request.method == 'POST':
        formFile = None
        try:
            formFile = request.FILES['data']
        except Exception:
            pass
        
        try:
            df = pd.read_csv(formFile).head(25)
            chartData = df.values.tolist()
            js_data = json.dumps(chartData)
        except Exception:
            pass

    return render(request, "icrawler/chart_pie.html", {'nm': nm,'data': js_data, 'chartData': chartData})


def updateKeyWords(request):
    
    if request.method == "GET":
        # example = request.GET.get('search')
        examples = 'onion,agriculture'.split(',')
        keywords = [] 

        s_ws = []
        s_is = []
        for example in examples:
            try:
                word = MyKeyword.objects.get(search_word=example)
                if word.id:
                    s_is.append(word.id)
                if word.parent_id:
                    s_is.append(word.parent_id)
                if word.id:
                    s_ws.append(word.search_word)
            except ObjectDoesNotExist:
                keywords.append(example)
        
        
        words = MyKeyword.objects.filter(Q(search_word__in=s_ws) | Q(parent_id__in=s_is) | Q(id__in=s_is))
        for w in words:
            keywords.append(w.search_word)

        print(keywords)

    if request.method == "POST":    
        fl = request.FILES['file']

        df = pd.read_excel(fl)

        for row in df.iterrows():
            item = row[1]['Item']
            main = row[1]['main']
            sub = row[1]['sub']
            search = row[1]['search']

            try:
                parentW = MyKeyword.objects.get(search_word=search)
            except ObjectDoesNotExist:
                parentW = MyKeyword()
                parentW.item = item
                parentW.main_category = main
                parentW.middle_category = sub
                parentW.search_word = search
                parentW.save()
            
            sims = [row[1]['sim1'],row[1]['sim2'],row[1]['sim3'],row[1]['sim4'],row[1]['sim5'],row[1]['sim6'],row[1]['sim7'],row[1]['sim8'],row[1]['sim9'],row[1]['sim10']]
            for sim in sims:
                if not sim:
                    continue
                try:
                    word = MyKeyword.objects.get(search_word=sim)
                except ObjectDoesNotExist:
                    word = MyKeyword()
                    word.parent = parentW
                    word.item = item
                    word.main_category = main
                    word.middle_category = sub
                    word.search_word = sim
                    word.save()
            

        

    return render(request, "icrawler/update_kw.html")