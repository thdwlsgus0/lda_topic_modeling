from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='m_index'),
    path('instruction', views.instruction, name='m_instruction'),
    path('timeline', views.timeline, name='m_timeline'),
    path('agrifood', views.agrifood, name='m_agrifood'),
    path('feedback', views.feedback, name='m_feedback')
]
