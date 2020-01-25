from django.urls import path
from .import views

urlpatterns = [
    path('index/', views.index, name='api_index'),
    path('agrifoodtrend/', views.agriFoodTrend, name="api_agrifoodtrend"),
    path('medfreq/', views.medFreq, name="api_medfreq")
]
