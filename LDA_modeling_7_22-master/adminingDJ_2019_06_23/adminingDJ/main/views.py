from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.db import connections
from django.db.models import Sum, Count, Avg
from django.core import serializers
from djongo.base import DatabaseWrapper
from django.core.serializers import serialize
from django.db.models import Q
from datetime import datetime, timezone
from .models import dalabtest, Feedback
from .forms import FeedbackForm
from django.http import JsonResponse
import re
# Create your views here.


def index(request):
    return render(request, "index/index.html")


def instruction(request):
    return render(request, "instruction/index.html")


def timeline(request):
    return render(request, "timeline/index.html")


def agrifood(request):

    drStart = request.GET.get('drStart')
    drEnd = request.GET.get('drEnd')
    period = request.GET.get('period')

    if drStart is None:
        return HttpResponseBadRequest()

    period = request.GET.get('period')

    dateStart = datetime.strptime(drStart, '%Y-%m-%d')
    dateEnd = datetime.strptime(drEnd, '%Y-%m-%d')
    if period == 'yearly':
        data = dalabtest.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values(
            'year').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('year')[:100]
    elif period == 'monthly':
        data = dalabtest.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values(
            'year', 'month').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('year', 'month')[:100]

    elif period == 'weekly':
        data = dalabtest.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values(
            'year', 'week').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('year', 'week')[:100]
    else:
        data = dalabtest.objects.filter(Q(cdate__range=(dateStart, dateEnd))).values(
            'year', 'month', 'day').annotate(Avg('panel_purchase_amount_ave'), Avg('panel_purchase_amount_sum'), Avg('retail_price'), Avg('wholesale_price')).order_by('year', 'month', 'day')[:100]

    data_list = list(data)
    response = JsonResponse(data_list, safe=False)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response


def feedback(request):
    fullName = request.POST.get('fullName', None)
    email = request.POST.get('email', None)
    message = request.POST.get('message', None)

    if fullName is None:
        return JsonResponse({'message': 'Insert full name'}, safe=False, status=400)

    if email is None:
        return JsonResponse({'message': 'Insert email'}, safe=False, status=400)

    match = re.match(
        "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email)

    if match == None:
        return JsonResponse({'message': 'Check email address'}, safe=False, status=400)

    if message is None:
        return JsonResponse({'message': 'Insert message'}, safe=False, status=400)

    ip = request.META.get('HTTP_X_FORWARDED_FOR',
                          '') or request.META.get('REMOTE_ADDR')

    info = request.META['HTTP_USER_AGENT']

    feed = Feedback.objects.filter(
        ipAddress__exact=ip, deviceInfo=info).order_by('-created_date')
    if feed is not None and len(feed) > 0:
        feed = feed[0]
        currentDate = datetime.now(timezone.utc)
        duration_in_s = (currentDate - feed.created_date).total_seconds()

        if int(duration_in_s) < 180:
            return JsonResponse({'message': '3 Seconds'}, safe=False, status=400)

    feed = Feedback()
    feed.fullName = fullName
    feed.email = email
    feed.feedback = message
    feed.ipAddress = ip
    feed.deviceInfo = info
    feed.save()

    return JsonResponse({'message': 'Successfull'}, safe=False)
