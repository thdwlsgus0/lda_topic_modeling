from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ic_index'),
    path('crawl', views.crawl, name='ic_crawl'),
    path('collected', views.collectedData, name='ic_collected'),
    path('collected/c<int:id>', views.collectedDetailData, name='ic_collected_det'),
    path('visualization/<slug:nm>', views.visualization, name='ic_visualization'),
    path('export/csv', views.exportCsv, name='ic_csv'),
    path('export/xls', views.exportXls, name='ic_xls'),

    path('update/kw', views.updateKeyWords, name='ic_updateKeyWords')
]
