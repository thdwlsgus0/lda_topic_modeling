from ..models import keyword_insert, TrendWithSales
import pandas as pd
from collections import Counter, defaultdict
from django.db.models import Q
from konlpy.tag import Hannanum
import csv
class Corr:
  
  def __init__(self, startdate, enddate):
      self.startdate = startdate
      self.enddate = enddate
      self.checklist =['폭설','한파','물량','출하','대형마트','할인마트','납품업체','과잉생산','재배면적','계약재배',
      '저장량','조생종','노균병','메르스','구제역','가뭄','장마','이상기후','잎마름병',
      '일조량','수매검사','냉해','생육','병해','병해충','재고물량','햇양파','태풍','황사','생산량','미세먼지','폭염']
      self.remove_list=[',','.','(',')','-','"']
  def totalcsv(self, onion):
          f = open('output1.csv', 'w', encoding='utf-8', newline='')
          wr = csv.writer(f)
          wr.writerow(['date', 'snow','cold_wave', 'Shipment','volume','big_mart','sale_mart','supplier','Overproduction',
          'Cultivation_area','Contract_cultivation','amount_of_storage','early_of_life','Nocicept','Mers'
          ,'Foot-and-mouth-disease','drought','rainy_season','abnormal_climate','Leaf_blight','sunshine',
          'Purchase_inspection','Cold_weather','Growth','Disease','pest','Inventory','honey_onion','typhoon','dust_storm'
          ,'output','free_dust'])
          for onion_list in onion:
              d = defaultdict(int)
              d={'폭설':0,'한파':0, '물량':0,'출하':0, '대형마트':0,'할인마트':0,'납품업체':0,'과잉생산':0,'재배면적':0,
              '계약재배':0, '저장량':0,'조생종':0,'노균병':0,'메르스':0,'구제역':0,'가뭄':0,'장마':0,'이상기후':0,'잎마름병':0,
              '일조량':0,'수매검사':0,'냉해':0,'생육':0,'병해':0, '병해충':0,'재고물량':0,'햇양파':0, '태풍':0,'황사':0,'생산량':0,
              '미세먼지':0,'폭염':0}
              words = onion_list['Content'] # 뉴스 기사
              day = str(onion_list['Date']) # 날짜 string으로 무조건 바꿔줘야함.
              data = Hannanum().nouns(words) # 공백으로 구분하기 위해서 설정함.
              new_day= day.split(" ")[0] #날짜 앞에 받음
              for i in data:
                  i.replace(",","")
                  i.replace(".","")
                  i.replace("-","")
                  i.replace("(","")
                  i.replace(")","")
              counter_list = Counter(data)
              for k,v in counter_list.items():
                 if k in self.checklist:
                     d[k]+=v
              wr.writerow([new_day,d['폭설'],d['한파'],d['물량'],d['출하'],d['대형마트'],d['할인마트'],d['납품업체'],d['과잉생산'],d['재배면적'],d['계약재배'],d['저장량'],d['조생종'],d['노균병'],
              d['메르스'],d['구제역'],d['가뭄'],d['장마'],d['이상기후'],d['잎마름병'],d['일조량'],d['수매검사'],d['냉해'],d['생육'],d['병해'],d['병해충'],d['재고물량'],d['햇양파'],d['태풍'],
              d['황사'],d['생산량'],d['미세먼지'],d['폭염']])
  def Calculate(self):
      onion = keyword_insert.objects.filter(Q(Date__range=(self.startdate, self.enddate))).values('Content', 'Date') 
      total_list=[]
    #   drought = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/가뭄.csv")
    #   print("가뭄:{0}".format(drought.corr()))
    #   snow = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/폭설.csv")
    #   print("폭설:{0}.".format(snow.corr()))
    #   vegetable = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/노균병.csv")
    #   print("노균병:{0}".format(vegetable.corr()))
    #   output = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/생산량.csv")
    #   print("생산량 및 재배면적{0}".format(output.corr()))
    #   mers = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/메르스.csv")
    #   print("메르스 {0}".format(mers.corr()))
    #   spring = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/봄.csv")
    #   print("봄철 :{0}".format(spring.corr()))
    #   summer = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/여름.csv")
    #   print("여름철 :{0}".format(summer.corr()))
    #   autumn = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/가을.csv")
    #   print("가을철 :{0}".format(autumn.corr()))
    #   winter = pd.read_csv("C:/Users/82104/agriculture_folder/대학원1년/adminingDJ_백업본/adminingDJ/visualization/ldafile/겨울.csv")
    #   print("겨울철:{0}".format(winter.corr()))
    #   self.totalcsv(onion)
        #  f = open("jinhyun.txt","w",encoding='utf8')
        #  for li in data:
        #      if li not in total_list:
        #          total_list.append(li)
        #  for li in total_list:
        #      f.write(li+'\n')
        #  f.close()
         
  