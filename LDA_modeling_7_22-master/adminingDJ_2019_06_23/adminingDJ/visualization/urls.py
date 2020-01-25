from django.urls import path
from . import views

urlpatterns = [
    path('underdev/', views.underDev, name="vis_af_dev"),
    path('agri_food_trend/', views.agrifoodAnalysis, name='vis_af_trend'),
    path('agri_food_predict/', views.agrifoodPredict, name='vis_af_predict'),
    path('agri_food_topic/', views.agrifoodTopic, name='vis_af_topic'),#word_count visualization
    #path('agri_food_word_count/', views.agrifoodWord, name='vis_af_word'), #word_count and topic_modeling analysis
    path('agri_food_modeling/', views.agrifoodModeling, name='vis_af_modeling'), # topic_modeling  
    path('agri_food_notidf/', views.agrifoodnotidf, name='vis_af_notidf'),
    path('gif/', views.generateItemFreq, name='vis_af_gif'),
    path('agri_food_wordcloud/', views.agrifoodWordCloud, name='vis_af_wordcloud')
]
