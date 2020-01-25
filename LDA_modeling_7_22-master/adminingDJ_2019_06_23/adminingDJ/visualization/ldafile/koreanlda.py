from collections import Counter
import random
import pymongo
from pymongo import MongoClient
from konlpy.tag import Twitter
import pandas as pd
import re,csv
from ..ldafile import pylda
class korean:
 def __init__(self):
     self.firstlist=[]
     self.conn = MongoClient('113.198.137.147', port=27017,
     username='root',password='gac81-344', authSource='admin')
     self.countlist=[]
 def returncount(self): 
   onion_dict= {} # dictionary 
#    for i in range(0,10):
#        broad_name = '201'+str(i)+'broadcastNews'
#        publish_name = '201'+str(i)+'publishedNews'
#        db = self.conn["admin"]
#        broad = db[broad_name]
#        publish = db[publish_name]
#        query = {"Origin Keyword":"양파" ,"Content":{"$regex":"잎마름병"}}
#        data = broad.find(query).count()
#        data2 = publish.find(query).count()
#        print("data, data2:{0},{1}".format(data, data2))
#        self.countlist.append(data+data2)
#    print("self.countlist:{0}".format(self.countlist))
   data = pd.read_csv('C:/Users/82104/Desktop/adminingDJ_2019_06_23/adminingDJ/visualization/ldafile/jinhyun.csv') # 절대경로 설정
   dry_onion={2010:1, 2011:0, 2012:7,2013:2,2014:0, 2015:2, 2016:3, 2017:5, 2018:28, 2019:1}
   for index, row in data.iterrows():
       onion_dict[row['index']]= row['value']
   self.countlist.append(onion_dict)
   self.countlist.append(dry_onion) 
   return self.countlist
 def returnnewdocument(self, documents, data):
    twitter = Twitter()
    for i in data:
     f = open("visualization/stopwords.txt", "r",encoding='UTF8')    
     noun_body = twitter.nouns(i['Content'])
     text_list=[]
     while True:
        line = f.readline()
        line = re.sub('\n', '',line)
        text_list.append(line)
        if not line: break
     text_list = set(text_list)
     filtered_sentence = [w for w in noun_body if not w in text_list] 
     documents.append(filtered_sentence)
    return documents
 def korean_method(self):
    published_name = '2018'+'publishedNews'
    broad_name = '2018'+'broadcastNews'
    db = self.conn["admin"]
    publish = db[published_name]
    broad = db[broad_name]
    query = {"Origin Keyword":"양파" ,"Content":{"$regex":"잎마름병"}, "Date":{"$gte":"2018-01-01", "$lte":"2018-12-31"}}
    query2 = {"Origin Keyword":"양파", "Content":{"$regex":"노균병"}, "Date":{"$gte":"2018-01-01", "$lte":"2018-12-31"}}
    data = publish.find(query)
    data2 = broad.find(query)
    data3 = publish.find(query2)
    data4 = broad.find(query2)
    twitter = Twitter()
    documents = []
    newdata = self.returnnewdocument(documents, data)
    new2data = self.returnnewdocument(newdata, data2)
    new3data = self.returnnewdocument(new2data, data3)
    new4data = self.returnnewdocument(new3data, data4)
    visual = pylda.PyLda(new4data)
    visual.visualization()

    k=3 # 토픽의 수
    random.seed(0) # 일정한 난수를 생성하기 위해서 선택함 
    D = len(documents) # 총 문서의 수 15개
    document_topic_counts = [Counter() for _ in documents] # 문서 , 토픽간의 카운팅 배열 ex) 1번쨰 문서에 3번 주제의 개수
    topic_word_counts = [Counter() for _ in range(k)] # 토픽, 단어간의 카운팅 배열 ex) 2번 주제의 '버섯'의 개수
    topic_counts = [0 for _ in range(k)] # 각 토픽의 총 단어 수
    document_lengths = list(map(len, documents)) # 각 문서에 포함되는 총 단어 수
    distinct_words = set(word for document in documents for word in document) # 단어 종류
    V = len(distinct_words) # 총 단어 수
    print("총 단어 수:{0}".format(V))
    def p_topic_given_document(topic, d, alpha=0.1): # 문서 d의 모든 단어 가운데 topic에 속하는 단어의 비율 (alpha를 더해 smoothing)
     return((document_topic_counts[d][topic]+ alpha)/
            (document_lengths[d] + k * alpha))

    def p_word_given_topic(word, topic, beta=0.1): # topic에 속한 단어 가운데 word의 비율 (beta를 더해 smoothing)
     return((topic_word_counts[topic][word] + beta)/
             (topic_counts[topic] + V *beta))

    def topic_weight(d, word, k):# 문서와 문서의 단어가 주어지면 k번째 토픽의 weight를 반환
     return p_word_given_topic(word,k) * p_topic_given_document(k,d)

    def choose_new_topic(d, word): # 새로운 토픽을 지정하는 부분
     return sample_from([topic_weight(d,word,k) for k in range(k)])

    def sample_from(weights): # i를 weights[i] / sum(weights)
     total = sum(weights) # 확률로 변환
     rnd = total * random.random() #0과 total 사이를 균일하게 선택
     for i, w in enumerate(weights):#아래 식을 만족하는 가장 작은 i를 반환
        rnd -= w #weights[0] + ... + weights[i]>=rnd
        if rnd<=0:
            return i
# 문서 생성 과정
    document_topics = [[random.randrange(k) for word in document] for document in documents] # 각 단어를 임의의 토픽에 랜덤 배정 
    for d in range(D): # 문서의 개수만큼 반복문을 돌림
     for word, topic in zip(documents[d], document_topics[d]):
        document_topic_counts[d][topic]+=1 # 문서당 토픽수에 값 추가
        topic_word_counts[topic][word]+=1 # 토픽당 단어수에 값 추가
        topic_counts[topic]+=1 # 각 토픽의 총 개수

    for iter in range(1000): # 깁스 샘플링 시작, 표본을 바꿔가면서 1000번 정도 반복하면 토픽이 수렴함
     for d in range(D):
        for i, (word,topic) in enumerate(zip(documents[d], document_topics[d])):
            document_topic_counts[d][topic]-=1 #해당 표본을 제외하기 위해서 문서 내의 해당 토픽의 수를 -1을 취한다.
            topic_word_counts[topic][word]-=1 #해당 표본을 제외하기 위해서 토픽 내의 해당 단어의 수를 -1을 취한다.
            topic_counts[topic]-=1 #해당 표본을 제외하기 위해서 해당 토픽의 총 단어수를 -1을 취한다. 
            document_lengths[d]-=1 #해당 표본을 제외하기 위해서 해당 문서에 포함되는 총 단어수를 -1을 취한다.

            new_topic = choose_new_topic(d,word) # 이 부분이 토픽을 바꿔주는 부분
            document_topics[d][i] = new_topic # 새로운 토픽을 넣어줌

            # 샘플링 대상 word의 새로운 topic을 반영해
            # 말뭉치 정보 업데이트
            document_topic_counts[d][new_topic]+=1 
            topic_word_counts[new_topic][word]+=1
            topic_counts[new_topic]+=1 
            document_lengths[d]+=1 
# value = [i for i in document_topic_counts]
# topic_word_count = [i for i in topic_word_counts]
# print("value:{0}, topic_word_count:{1}".format(value,topic_word_count))
    f = open("topic.csv",'w',encoding='utf-8', newline='')
    wr = csv.writer(f) 
    for i in range(0,3):
        #print("topic_word_counts{0}:{1}".format(i, topic_word_counts[i].most_common(3)))
        self.firstlist.append(dict(topic_word_counts[i].most_common(3)))   
    #print("countlist:{0}".format(self.countlist))   
    #print("firstlist:{0}".format(self.firstlist[0])) 
    wr.writerow(['topic', 'keyword','count'])
    for i in range(0,3):
        for key, value in self.firstlist[i].items():
            #print("key, value:{0},{1}".format(key, value))
            wr.writerow([i+1, key, value])
    return self.firstlist    