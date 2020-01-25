from django.shortcuts import render
from .models import TrendWithSales, TrendWithItemFreq, keyword_insert, topic_class,practice, publish_onion
from .ldafile import lda, correlation, koreanlda
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.db import connection
from datetime import datetime, timedelta
from django.db.models import Avg, Sum, Count
import json
import pandas as pd
from pymongo import MongoClient
import pandas as pd
import numpy as np
from functools import reduce
import operator
from konlpy.tag import Kkma # 형태소분석기를 만들기 위해서 설정함.
from collections import Counter # Counter생성함.
from konlpy.tag import Hannanum # 형태소분석기를 만들기 위해서 설정함.
import operator # dictionary를 정렬하기 위해서 구현함.
from collections import defaultdict
from collections import Counter
import random
import pymongo
from pymongo import MongoClient
from konlpy.tag import Twitter
import re


# Create your views here.
def underDev(request):
    return render(request, 'underdev/underdev.html')

def agrifoodAnalysis(request):
    if request.method == 'POST':
        foodname = request.POST.get('foodname')
        drStart = request.POST.get('drStart')
        drEnd = request.POST.get('drEnd')
        period = request.POST.get('period')

        media = request.POST.getlist('media')
        serveMenu = request.POST.getlist('servemenu')

        if foodname != '양파':
            return HttpResponseNotFound('Data is not found.')

        if drStart is None or drEnd is None:
            return HttpResponseBadRequest('Term is not set.')

        if len(media) == 0 and len(serveMenu) == 0:
            return HttpResponseBadRequest('Options are not selected')

        dateStart = datetime.strptime(drStart, '%Y-%m-%d')
        dateEnd = datetime.strptime(drEnd, '%Y-%m-%d')
        dateEnd = dateEnd.replace(hour=23, minute=59, second=59)

        mediaNames_bl = request.POST.getlist('mediaName_bl')
        mediaNames_bc = request.POST.getlist('mediaName_bc')
        mediaNames_pn = request.POST.getlist('mediaName_pn')
        mediaNames_en = request.POST.getlist('mediaName_en')

        q_list = [Q(channel__exact='socialMedia'), Q(Q(sub_channel__in=list(mediaNames_bl))
                                                     & Q(channel__exact='blogs'))]

        if len(mediaNames_bc) == 0:
            q_list.append(Q(Q(sub_channel__in=list(['def'])) & Q(
                channel__exact='broadcastNews')))
        elif 'others' in mediaNames_bc:
            mediaNames_bc2 = []
            if '뉴시스' not in mediaNames_bc:
                mediaNames_bc2.append('뉴시스')
            if '뉴시스' not in mediaNames_bc:
                mediaNames_bc2.append('SBS 뉴스')
            if 'MBN' not in mediaNames_bc:
                mediaNames_bc2.append('MBN')
            if '한국경제TV' not in mediaNames_bc:
                mediaNames_bc2.append('한국경제TV')
            if 'MBC 뉴스' not in mediaNames_bc:
                mediaNames_bc2.append('MBC 뉴스')

            q_list.append(Q(~Q(sub_channel__in=list(mediaNames_bc2)), Q(
                channel__exact='broadcastNews')))
        else:
            q_list.append(Q(Q(sub_channel__in=list(mediaNames_bc)), Q(
                channel__exact='broadcastNews')))

        if len(mediaNames_pn) == 0:
            q_list.append(Q(Q(sub_channel__in=list(['def'])) & Q(
                channel__exact='publishedNews')))
        elif 'others' in mediaNames_pn:
            mediaNames_pn2 = []
            if '연합뉴스' not in mediaNames_pn:
                mediaNames_pn2.append('연합뉴스')
            if '아시아경제' not in mediaNames_pn:
                mediaNames_pn2.append('아시아경제')
            if '매일경제' not in mediaNames_pn:
                mediaNames_pn2.append('매일경제')
            if '머니투데이' not in mediaNames_pn:
                mediaNames_pn2.append('머니투데이')
            if '레이디경향' not in mediaNames_pn:
                mediaNames_pn2.append('레이디경향')

            q_list.append(Q(~Q(sub_channel__in=list(mediaNames_pn2)) & Q(
                channel__exact='publishedNews')))
        else:
            q_list.append(Q(Q(sub_channel__in=list(mediaNames_pn)) & Q(
                channel__exact='publishedNews')))

        if len(mediaNames_en) == 0:
            q_list.append(Q(Q(sub_channel__in=list(['def'])) & Q(
                channel__exact='entertainment')))
        elif 'others' in mediaNames_en:
            mediaNames_en2 = []
            if '시사/교양프로그램' not in mediaNames_en:
                mediaNames_en2.append('시사/교양프로그램')
            if '뉴스' not in mediaNames_en:
                mediaNames_en2.append('뉴스')
            if '예능_먹방' not in mediaNames_en:
                mediaNames_en2.append('예능_먹방')
            if '예능' not in mediaNames_en:
                mediaNames_en2.append('예능')
            if '예능_건강' not in mediaNames_en:
                mediaNames_en2.append('예능_건강')

            q_list.append(Q(~Q(sub_channel__in=list(mediaNames_en2)) & Q(
                channel__exact='entertainment')))
        else:
            q_list.append(Q(Q(sub_channel__in=list(mediaNames_en)) & Q(
                channel__exact='entertainment')))

        print(q_list)
        dataFrame = None

        if period == 'yearly':
            data = TrendWithSales.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values(
                'year').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('-year')[:200]

            if len(data) > 0:
                dfSales = pd.DataFrame(list(data))

                data_freq = TrendWithItemFreq.objects.filter(
                    Q(cdate__range=(dateStart, dateEnd)), Q(category__exact=foodname), reduce(operator.or_, q_list)).values('year', 'channel', 'sub_channel').annotate(freq=Sum('item_freq')).order_by('-year')

                if len(data_freq) > 0:
                    dfFreq = pd.DataFrame(list(data_freq))
                    dfFreq = pd.pivot_table(dfFreq, values='freq', index=[
                        'year'], columns='channel', aggfunc=np.sum).reset_index()

                    dataFrame = dfSales.merge(dfFreq, on=['year'], how='left')
        elif period == 'monthly':

            data = TrendWithSales.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values(
                'year', 'month').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('-year', '-month')[:200]

            if len(data) > 0:
                dfSales = pd.DataFrame(list(data))

                data_freq = TrendWithItemFreq.objects.filter(
                    Q(cdate__range=(dateStart, dateEnd)), Q(category__exact=foodname), reduce(operator.or_, q_list)).values('year', 'month', 'channel', 'sub_channel').annotate(freq=Sum('item_freq')).order_by('-year', '-month')

                if len(data_freq) > 0:
                    dfFreq = pd.DataFrame(list(data_freq))
                    dfFreq = pd.pivot_table(dfFreq, values='freq', index=[
                        'year', 'month'], columns='channel', aggfunc=np.sum).reset_index()
                    dataFrame = dfSales.merge(
                        dfFreq, on=['year', 'month'], how='left')

        elif period == 'weekly':
            data = TrendWithSales.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values(
                'year', 'week').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('-year', '-week')[:200]

            if len(data) > 0:
                #Q(Q(sub_channel__in=list(mediaNames_bc)) | Q(sub_channel__in=list(mediaNames_pn)) | Q(sub_channel__in=list(mediaNames_bl)) | Q(sub_channel__in=list(mediaNames_en)))
                dfSales = pd.DataFrame(list(data))
                data_freq = TrendWithItemFreq.objects.filter(
                    Q(cdate__range=(dateStart, dateEnd)),
                    Q(category__exact=foodname),
                    reduce(operator.or_, q_list)
                ).values('year', 'week', 'channel', 'sub_channel').annotate(freq=Sum('item_freq')).order_by('-year', '-week')

                if len(data_freq) > 0:
                    dfFreq = pd.DataFrame(list(data_freq))
                    dfFreq = pd.pivot_table(dfFreq, values='freq', index=[
                        'year', 'week'], columns='channel', aggfunc=np.sum).reset_index()

                    dataFrame = dfSales.merge(
                        dfFreq, on=['year', 'week'], how='left')
        else:
            data = TrendWithSales.objects.filter(
                Q(cdate__range=(dateStart, dateEnd))
            ).values(
                'year', 'month', 'day').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('-year', '-month', '-day')[:200]

            if len(data) > 0:
                dfSales = pd.DataFrame(list(data))
                data_freq = TrendWithItemFreq.objects.filter(
                    Q(cdate__range=(dateStart, dateEnd)),
                    Q(category__exact=foodname), reduce(operator.or_, q_list)).values('year', 'month', 'day', 'channel', 'sub_channel').annotate(freq=Sum('item_freq')).order_by('-year', '-month', '-day')
                if len(data_freq) > 0:
                    dfFreq = pd.DataFrame(list(data_freq))

                    dfFreq = pd.pivot_table(dfFreq, values='freq', index=[
                                            'year', 'month', 'day'], columns='channel', aggfunc=np.sum, fill_value=0).reset_index()

                    dataFrame = dfSales.merge(
                        dfFreq, on=['year', 'month', 'day'], how='left')

        if dataFrame is not None:
            data_list = dataFrame.to_json(orient='records')
        else:
            data_list = json.dumps([])

        return render(request, "agrifoodanalysis/inc-visualization.html", {'data_list': data_list, 'media':  json.dumps(media), 'serveMenu': json.dumps(serveMenu)})

    return render(request, "agrifoodanalysis/analysis.html")


def generateItemFreq(request):

    try:
        conn = MongoClient('113.198.137.147', port=27017,
                           username='root', password='gac81-344', authSource='admin')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = conn.admin

    freqCollection = db.get_collection(name='mediaItemFrequency')

    channelName = request.GET.get('channelName', None)

    if channelName == 'broadcastNews':
        for ye in range(2010, 2020):
            ye = '{}broadcastNews'.format(ye)
            collection = db.get_collection(name=ye)
            cursor = getCursor(collection, channelName)
            insertOrUpdateCollection(freqCollection, cursor, channelName)
    elif channelName == 'publishedNews':
        for ye in range(2010, 2020):
            ye = '{}publishedNews'.format(ye)
            collection = db.get_collection(name=ye)
            cursor = getCursor(collection, channelName)
            insertOrUpdateCollection(freqCollection, cursor, channelName)
    elif channelName == 'socialMedia':
        for ye in range(2010, 2020):
            ye = '{}Twitter'.format(ye)
            collection = db.get_collection(name=ye)
            cursor = getCursor(collection, 'twitter')
            insertOrUpdateCollection(
                freqCollection, cursor, channelName, 'twitter')
    elif channelName == 'blogs':
        for ye in range(2010, 2020):
            ye = '{}daumBlog'.format(ye)
            collection = db.get_collection(name=ye)
            cursor = getCursor(collection, 'daum')
            insertOrUpdateCollection(
                freqCollection, cursor, channelName, 'daum')

        for ye in range(2010, 2020):
            ye = '{}naverBlog'.format(ye)
            collection = db.get_collection(name=ye)
            cursor = getCursor(collection, 'naver')
            insertOrUpdateCollection(
                freqCollection, cursor, channelName, 'naver')
    elif channelName == 'entertainment':
        ye = 'video_data'
        collection = db.get_collection(name=ye)
        cursor = getCursor(collection, 'video_data')
        insertOrUpdateCollection(
            freqCollection, cursor, channelName)
    return JsonResponse({'s': 1})


def getCursor(collection, channelName):
    if channelName == 'broadcastNews':
        return collection.aggregate([
            {'$project': {'keyword': "$Sub-category", 'subchannel': '$Publisher',
                          "date": {'$arrayElemAt': [{'$split': ["$Date", " "]}, 0]}}},
            {'$match': {'keyword': '양파'}},
            {'$group': {'_id': {'keyword': "$keyword", 'subchannel': '$subchannel',
                                'date': "$date"}, 'count': {'$sum': 1}}},
            {'$sort': {"_id.date": 1}}
        ])
    if channelName == 'publishedNews':
        return collection.aggregate([
            {'$project': {'keyword': "$Sub-category", 'subchannel': '$Publisher',
                          "date": {'$arrayElemAt': [{'$split': ["$Date", " "]}, 0]}}},
            {'$match': {'keyword': '양파'}},
            {'$group': {'_id': {'keyword': "$keyword", 'subchannel': '$subchannel',
                                'date': "$date"}, 'count': {'$sum': 1}}},
            {'$sort': {"_id.date": 1}}
        ])
    if channelName == 'twitter':
        return collection.aggregate([
            {'$project': {'keyword': "$Sub-category",
                          "date": {'$arrayElemAt': [{'$split': ["$Date", " "]}, 0]}}},
            {'$match': {'keyword': '양파'}},
            {'$group': {'_id': {'keyword': "$keyword",
                                'date': "$date"}, 'count': {'$sum': 1}}},
            {'$sort': {"_id.date": 1}}
        ])
    if channelName == 'daum':
        return collection.aggregate([
            {'$project': {'keyword': "$Sub-category",
                          "date": {'$arrayElemAt': [{'$split': ["$Date", " "]}, 0]}}},
            {'$match': {'keyword': '양파'}},
            {'$group': {'_id': {'keyword': "$keyword",
                                'date': "$date"}, 'count': {'$sum': 1}}},
            {'$sort': {"_id.date": 1}}
        ])
    if channelName == 'naver':
        return collection.aggregate([
            {'$project': {'keyword': "$Sub-category",
                          "date": {'$substr': ["$Date", 0, 10]}}},
            {'$match': {'keyword': '양파'}},
            {'$group': {'_id': {'keyword': "$keyword",
                                'date': "$date"}, 'count': {'$sum': 1}}},
            {'$sort': {"_id.date": 1}}
        ])
    if channelName == 'video_data':
        return collection.aggregate([
            {'$match': {'target_item': {'$elemMatch': {'term': '양파'}}}},
            {'$group': {'_id': {'keyword': "양파", 'subchannel': '$genre', 'date': "$published_date"},
                        'count': {'$sum': 1}}},
            {'$sort': {"_id.date": 1}}
        ])
    return None


def insertOrUpdateCollection(collection, cursor, channelName, channelSub=''):

    for record in cursor:
        try:
            dateStr = record['_id']['date']
            dateStr = dateStr.replace(' ', '').replace('.', '-')
            aDate = datetime.strptime(dateStr, '%Y-%m-%d')

            year = aDate.year
            month = aDate.month
            week = int(aDate.strftime('%U'))
            day = aDate.day
            category = record['_id']['keyword']

            subChannel = ''
            if channelSub == '':
                try:
                    subChannel = record['_id']['subchannel']
                except:
                    subChannel = ''
            else:
                subChannel = channelSub

            freq = int(record['count'])

            item = collection.find_one({
                'year': year,
                'month': month,
                'day': day,
                'channel': channelName,
                'sub_channel': subChannel,
                'category': category,

            })

            if item:
                collection.find_and_modify(query={'_id': item['_id']}, update={
                    '$set': {'item_freq': freq}}, upsert=False, full_response=True)
            else:
                data = {
                    'cdate': aDate,
                    'year': year,
                    'month': month,
                    'week': week,
                    'day': day,
                    'channel': channelName,
                    'sub_channel': subChannel,
                    'category': category,
                    'sub_category': '',
                    'tags': '',
                    'item_freq': freq
                }
                collection.insert_one(data)
        except Exception as e:
            print('{},{}'.format(dateStr, str(e)))
def agrifoodPredict(request):
    return render(request, "agrifoodpredict/predict.html")
    
def agrifoodWordCloud(request):
    value = koreanlda.korean() 
    # firstlist = value.korean_method()
    return_count = value.returncount() # 라인 차트 생성하기 위한 것
    value.korean_method() # 토픽별 키워드 분포 계산
    return render(request, "agrifoodwordcloud/word_cloud.html", {"return_count":return_count})
def agrifoodTopic(request): #topic_visualization
    if request.method == 'POST':
        foodname = request.POST.get('foodname')
        drStart = request.POST.get('drStart')
        print("시작{0}".format(drStart))
        drEnd = request.POST.get('drEnd')
        period = request.POST.get('period')
        media = request.POST.getlist('media')
        serveMenu = request.POST.getlist('servemenu')
        start_year = drStart.split("-")[0]
        end_year = drEnd.split("-")[0]
        start_year = int(start_year)
        end_year = int(end_year)
        print("start_year, end_year:{0},{1}".format(start_year,end_year))
        if foodname != '양파':
            return HttpResponseNotFound('Data is not found.')

        if drStart is None or drEnd is None:
            return HttpResponseBadRequest('Term is not set.')

        if len(media) == 0 and len(serveMenu) == 0:
            return HttpResponseBadRequest('Options are not selected')
        
        dateStart = datetime.strptime(drStart, '%Y-%m-%d')
        dateEnd = datetime.strptime(drEnd, '%Y-%m-%d')
        dateEnd = dateEnd.replace(hour=23, minute=59, second=59)
        print('{},{}'.format(dateStart,dateEnd))
        
        if period == 'yearly':
            data = topic_class.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values('year','keyword_list','count_list')
            data = list(data)
            df = None
            for item in data:
                if df is None:
                    df = pd.DataFrame(item)
                else:
                    df2 = pd.DataFrame(item)
                    df = df.append(df2)
            df = df.groupby(['year', 'keyword_list'],as_index=False).sum()  
            df =  df.sort_values(['year','count_list'],ascending=[True, False]).groupby(['year']).head(3) 
            List=[] 
            for index, row in df.iterrows():
               List.append({'year':row['year'], 'keyword':row['keyword_list'],'count':row['count_list']})    
            print(List)   
        elif period == 'monthly':
            data = topic_class.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values('year','month','keyword_list','count_list')
            data=list(data)
            df = None
            for item in data:
                if df is None:
                    df = pd.DataFrame(item)
                else:
                    df2 = pd.DataFrame(item)
                    df = df.append(df2)
            df = df.groupby(['year','month', 'keyword_list'],as_index=False).sum()  
            df =  df.sort_values(['year','month','count_list'],ascending=[True, True, False]).groupby(['year','month']).head(3)
            List=[] 
            for index, row in df.iterrows():
               List.append({'year':row['year'],'month':row['month'], 'keyword':row['keyword_list'],'count':row['count_list']})    
            print(List)
        elif period == 'weekly':
            data = topic_class.objects.filter(Q(cdate__range=(dateStart,dateEnd))).values('year', 'month','week', 'keyword_list','count_list')
            data = list(data)
            df = None
            for item in data:
                if df is None:
                    df = pd.DataFrame(item)
                else:
                    df2 = pd.DataFrame(item)
                    df = df.append(df2)
            df = df.groupby(['year','month','week', 'keyword_list'],as_index=False).sum()  
            df =  df.sort_values(['year','month','week','count_list'],ascending=[True, True,True, False]).groupby(['year','month','week']).head(3)
            List=[] 
            for index, row in df.iterrows():
               List.append({'year':row['year'],'month':row['month'],'week':row['week'], 'keyword':row['keyword_list'],'count':row['count_list']})    
            print(List)
        else:
            data = topic_class.objects.filter(Q(cdate__range=(dateStart,dateEnd))).values('year', 'month','day','keyword_list','count_list')
            data = list(data)
            df = None
            for item in data:
                if df is None:
                    df = pd.DataFrame(item)
                else:
                    df2 = pd.DataFrame(item)
                    df = df.append(df2)
            df = df.groupby(['year','month','day', 'keyword_list'],as_index=False).sum()  
            df =  df.sort_values(['year','month','day','count_list'],ascending=[True, True,True, False]).groupby(['year','month','day']).head(3)
            List=[] 
            for index, row in df.iterrows():
               List.append({'year':row['year'],'month':row['month'],'day':row['day'], 'keyword':row['keyword_list'],'count':row['count_list']})    
            print(List)
        data_list =list(List)
        data_list = json.dumps(data_list, ensure_ascii=False)
        return render(request, "agrifoodtopic_analysis/inc-visualization.html",{'data_list':data_list,'media':  json.dumps(media), 'serveMenu': json.dumps(serveMenu)})

    return render(request, "agrifoodtopic_analysis/topic.html")
def agrifoodModeling(request):
    if request.method == 'POST':
       content_list = []
       drStart = request.POST.get('drStart')
       drEnd = request.POST.get('drEnd')
       dateStart = datetime.strptime(drStart, '%Y-%m-%d')
       dateEnd = datetime.strptime(drEnd, '%Y-%m-%d')
       dateEnd = dateEnd.replace(hour=23, minute=59, second=59)
       content = keyword_insert.objects.filter(Q(Date__range=(dateStart, dateEnd))).values('Content')
       data = list(content)
       for i in data:
          content_list.append(i)   
       Corr = correlation.Corr(dateStart, dateEnd)
       Corr.Calculate()          
       ldaModel = lda.LDA(content, request.POST.get('decidetfidf'))
       ldaModel.Bigram()    
       return render(request, "agrifoodtfidf/onion.html")
    return render(request, "agrifoodtfidf/tfidf.html")
def agrifoodnotidf(request):
    if request.method == 'POST':
       content_list = []
       drStart = request.POST.get('drStart')
       drEnd = request.POST.get('drEnd')
       dateStart = datetime.strptime(drStart, '%Y-%m-%d')
       dateEnd = datetime.strptime(drEnd, '%Y-%m-%d')
       dateEnd = dateEnd.replace(hour=23, minute=59, second=59)
       content = keyword_insert.objects.filter(Q(Date__range=(dateStart, dateEnd))).values('Content')
       data = list(content)
       for i in data:
          content_list.append(i)   
       Corr = correlation.Corr(dateStart, dateEnd)
       Corr.Calculate()          
       ldaModel = lda.LDA(content, request.POST.get('decidetfidf'))
       ldaModel.Bigram()    
       return render(request, "agrifoodtfidf/onion.html")
    return render(request, "agrifoodnottfidf/nottfidf.html")    
