from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Sum
from visualization.models import TrendWithSales, TrendWithItemFreq
from datetime import datetime
import pandas as pd
import numpy as np
# Create your views here.


def index(request):
    return render(request, 'apiApp/index/index.html')


@require_http_methods(['GET'])
def agriFoodTrend(request):
    # http://127.0.0.1:8000/api/agrifoodtrend/?foodname=%EC%96%91%ED%8C%8C&drStart=2016-01-01&drEnd=2016-03-01&period=weekly&media=2,5,6&servemenu=1,2

    foodname = request.GET.get('foodname', '')

    if foodname != '양파':
        return JsonResponse([], safe=False)

    drStart = request.GET.get('drStart', '')
    drEnd = request.GET.get('drEnd', '')
    period = request.GET.get('period', '')

    media = request.GET.get('media', '')
    serveMenu = request.GET.get('servemenu', '')

    if foodname == '' or drStart == '' or drEnd == '' or period == '':
        return JsonResponse({'error': 'A parameter is missing.'}, status=400)

    if media == '' and serveMenu == '':
        return JsonResponse({'error': 'A parameter is missing.'}, status=400)

    if media == '':
        media = []
    else:
        media = media.split(',')

    if serveMenu == '':
        serveMenu = []
    else:
        serveMenu = serveMenu.split(',')

    dateStart = datetime.strptime(drStart, '%Y-%m-%d')
    dateEnd = datetime.strptime(drEnd, '%Y-%m-%d')
    dateEnd = dateEnd.replace(hour=23, minute=59, second=59)

    vals = ['year']
    if period == 'monthly':
        vals = ('year', 'month')
    elif period == 'weekly':
        vals = ('year', 'week')
    elif period == 'daily':
        vals = ('year', 'month', 'day')

    data = TrendWithSales.objects.filter(
        cdate__range=(dateStart, dateEnd)).values(*vals)

    for m in media:
        if m == '2':
            data = data.annotate(Sum('news_freq'))
            continue
        if m == '5':
            data = data.annotate(Sum('blog_freq'))
            continue
        if m == '6':
            data = data.annotate(Sum('video_freq'))
            continue

    for s in serveMenu:
        if s == '2':
            data = data.annotate(Avg('wholesale_price'))
            continue
        if s == '3':
            data = data.annotate(Avg('retail_price'))
            continue
        if s == '4':
            data = data.annotate(Avg('panel_purchase_amount_ave'))
            continue
        if s == '5':
            data = data.annotate(Avg('panel_purchase_amount_sum'))
            continue

    data_list = list(data)

    return JsonResponse(data_list, safe=False)


def medFreq(request):

    dateStart = datetime.strptime('2016-01-01', '%Y-%m-%d')
    dateEnd = datetime.strptime('2016-01-02', '%Y-%m-%d')
    dateEnd = dateEnd.replace(hour=23, minute=59, second=59)

    print('{} - {}'.format(dateStart, dateEnd))

    # try:
    data = TrendWithItemFreq.objects.filter(
        cdate__range=(dateStart, dateEnd), category__exact='양파').values('year', 'month', 'day', 'channel', 'sub_channel').annotate(freq=Sum('item_freq')).order_by('-year', '-month', '-day')

    data2 = TrendWithSales.objects.filter(
        cdate__range=(dateStart, dateEnd)).values('year', 'month', 'day').annotate(Avg('wholesale_price'), Avg('retail_price'), Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum')).order_by('-year', '-month', '-day')

    if len(data2) > 0:
        dataFrame2 = pd.DataFrame(list(data2))

    if len(data) > 0:
        dataFrame = pd.DataFrame(list(data))
        dataFrame = pd.pivot_table(dataFrame, values='freq', index=[
            'year', 'month', 'day'], columns='channel', aggfunc=np.sum).reset_index()

        result = dataFrame2.merge(
            dataFrame, on=['year', 'month', 'day'], how='left')

        return HttpResponse(result.to_json(orient='records'), content_type='application/json')

    return JsonResponse([], safe=False)

    # except Exception as e:
    #     return JsonResponse({'error': str(e)}, status=500)
