from ..models import keyword_insert
import gensim
from konlpy.tag import Hannanum, Twitter,Okt
import spacy
import gensim.corpora as corpora
from . import correlation
from gensim.models import CoherenceModel
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import NMF
from gensim.models.tfidfmodel import TfidfModel
import nltk
import pyLDAvis.gensim as gensimvis
import pyLDAvis
import pandas as pd
from time import time
from gensim import matutils
class LDA:
    def __init__(self, content_list, types):
        self.content = content_list
        self.stop_words= ['0','◆','&','동영상','뉴스','醫', 'ы', '쇱','湲곗','щ','紐⑤'
        ,'硫', '몄', '쇰','異', '泥','등','것','[경제365]','[맛있는경제]','레이어','닫기','1','수','기사','이번','포','비롯','김씨',
         '원','설','■','뉴시스','▶','거','◀','시시각각','원활한','다양한','정도','평','발','달','ㆍ','◀ＳＹＮ▶',
         '이','지','군','곳','할','고','격','◀ＡＮＣ▶','믈','당','남','케이윌','이상형','사랑','스타들','가수','연속','하반기','싱싱볼','농기원',
         '기자','앵커','때문','올해','때','공연','모바','댁','샤워','4','여산','를','레','엽기의상','”','블룸버그통신','유죄','열광',
         '가운데','시','메','글레이즈브룩','굴착','12.','<녹취>','★','네이버','☞','중','9%↑)','8%↑)','7.','5%↑)','0%↑)',
         '17.','10대','0.','이석기','추천','이사','),','조사','경우','로','시즌2','도시락’','4','(함양=뉴스1)','함양군',
         '할','[패스트푸트','마천농협','목포세관','紐⑤_보내기','최상돈','라','2.5','씨',')’','군민','정부','ⓒ','뉴스1코리아,','실시','버터구'
         ,'해','산지폐','5','영상','판','인터뷰','쌍구','톤','◇부산','전남도','\"청혈주스','언론사','2g,','일부','전','3월','23개'
             '남상호','후','면','NEWS1','/특)','리포터','기','제보','▲','기준','내','공감언론','13','역설','살','【','프레시웨','1차',
             '우','클래시코','포블라노','【서울=뉴시스】','안','@','저작권자','무단복제','재배포','금지','메인','버튼','vcr','ａｎｃ','의령',
             '강종효','의령군', '양재준기자','양재준','양재준입니','부터','자동','ez','동원f','동안','최근','김정숙','박명진','서초구', '지난주',
             'mbn리치','포대','모두','마케팅','양재동','기자들','아티초크','아웃링크','소컵','임태희','스팸클래식','에콰도르','여러분'
             ,'연어시장','여러명','이동해','동원산업','음란행위','에어익스프레스','수사의뢰','트위터','취재','기사배열','스파이더맨','추천요소','뒷이야기'
             ,'와이파','노선','서부농업기술센터','여성인권','관련뉴스','무단전재','조사결과','재킷','지난해','전환','새누리','관련뉴스','클라시코','오피스텔'
             ,'여성인권','시금치','잇따라','기간','제주농협','농진청','예정','평년동기','농림축산식품부','자전거','인터넷','보이피싱','준비중','농식품부','경계경보'
             ,'보복운전','축제','포기당','지난달','농협','배추','장바구니','이후','집계','생필품','시민들','도도맘','연합뉴스','연합뉴스tv','낙찰받았습니','전남농협'
             ,'페이지','대부분','성폭행','대통령','지정운','차관','올해산','본격화','한국경제','오늘','한겨울','사육두수','대위','만원','세상','외부','이랑현미'
             ,'이명박','박진원','이랑현미','정보화','정승혜','이용료','선정','광우병','청산가리','김민선','선언','전쟁터','이종열','신세계','인천점','가운데','김재영','소비자'
             ,'노경진', 'ｉｎｔ','서민들','방안','정부중앙청사','남자답','오토바이','대피하지','제수용품','섹드립','여인홍','실손보험','단속','이하','서울신문', '머니투데이'
             ,'아니다','중장기','관계자','예측','소비자들','심술통','수요','심재억기자','아시아경제','내년','재정','이데일리','정치권', '한다','정치적','김영식','기획재정부','박재완'
             ,'있습니다','것으로','쓰레기를','나옵니다','메인으로','jtbc','하지만','합니다','모아보기','선정하며','모두에게_보여주고','일반','마늘은','봉투에','버리는','있는'
             ,'쓰레기가','같은','재배면적이','news','따르면','모바일','무단','사실상','크게','mbc','com','ｓｙｎ','어제보다','ｖｃｒ','계속','요즘','페이스북','카카오스토리','이동','불편'
             ,'전문가','저작권_한국','이처럼','이유','이용문','일제','조합원','오히려','완화','시장','저장성','미나리','보지','역시','가까이','가까스로','가상현실','가장자리','가지나','엉터리'
             ,'모내기','모래밭','가치나','갑자기','메르','바싹','미터','무니','가파른','가뜩이나','부들','반면','강병규','비교','바로미터','부랴부랴','행정','갈수록','건데','게다가','박은지',
             '예년','오큘러스','오지랖','무기한','말라가','마찬가지']  # 불용어처리
        self.needlesslist=['햄버거','치킨','피자','버거','돈가스','돈까스','꽁치','주꾸미','쭈꾸미','골프','하나로클럽','쓰레기']
        self.needlist=['재배면적','생산량','작황','폭설','가뭄','양파노균병','잎마름병','출하','조생양파','조기출하','할당관세','메르스','구제역','병해충','물량확보','재고물량','저장양','해충','우박']
        self.type=types
    def TopicModeling(self, content,total_str, result_list):
              #   print("content:{0}".format(content))
              #     s = PorterStemmer()
              print(total_str)
              nltk.download('wordnet')
              token_ko = Twitter().pos(total_str)
              for i in token_ko:
                   for k in self.stop_words:
                    if i[1] =="Noun" and i[0] not in k:
                         result_list.append(i[0])
                         break      
              yield (gensim.utils.simple_preprocess(str(result_list), deacc=True)) # 불용어 2차 제거 , deacc=True이면 쉼표 제거함.
    def Bigram(self):
         topic_list=[]
         total_list=[]
         result_list=[]
         total_str=""
         for i in self.content: # 문장 하나하나씩 돌려봄
              total_list.append(i['Content']) #
              total_str+=i['Content']
         vectorizer =TfidfVectorizer(ngram_range=(1,1),use_idf=True, smooth_idf=True) # ngram_range를 (1,1)로 준 이유는 단어를 의미있게 나눌 때 1개의 단어로 구분하기 위해서
         # use_idf=True를 사용한 이유는 역문서의 개념 즉, 다양한 문서에서 동일한 단어가 나타나는 경우 가중치를 감소, raw documents를 TF-IDF 모양의 매트릭스로 변환
         print("vectorizer:{0}".format(vectorizer))
         x = vectorizer.fit_transform(total_list) # 학습을 진행함. 
         idf = vectorizer.idf_
         vocab = vectorizer.vocabulary_
         print("idf, vocab:{0},{1}".format(idf, vocab))
         print("x:{0}".format(x))
     #     position = vectorizer.vocabulary_['메르스']
     #     print("position:{0}".format(position))
     #     x[:,position] *=2.0
     #     count_vectorizer = CountVectorizer(min_df=1,stop_words="english")
     #     term_freq_matrix = count_vectorizer.fit_transform(total_list)
     #     tfidf = TfidfTransformer(norm="l2")
     #     tfidf.fit(term_freq_matrix)
     #     tf_idf_matrix = tfidf.transform(term_freq_matrix)
     #     position = count_vectorizer.vocabulary_['메르스']
     #     tf_idf_matrix[:, position] *= 2.0
         data_words = list(self.TopicModeling(i['Content'], total_str, result_list))
         bigram = gensim.models.Phrases(data_words) # higher threshold fewer phrases
              #Faster way to get a sentence clubbed as a trigram/bigram
         print("data_words:{0}".format(data_words))
         bigram_mod = gensim.models.phrases.Phraser(bigram)
         data_words_nostops = self.remove_stopwords(data_words) #불용어 3차 제거
         data_words_bigrams = self.make_bigrams(data_words_nostops,bigram_mod)
         print("data_words_bigrams:{0}".format(data_words_bigrams))
         data_lemmatized = self.lemmatization(data_words_nostops, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    #         # print(data_lemmatized[:1])
         id2word = corpora.Dictionary(data_lemmatized) # dictionary 생성
         for i in range(0, len(id2word)):
              if id2word[i] in self.stop_words:
                   del id2word[i]
     #     print("id2word의 개수:{0}".format(len(id2word)))
         texts = data_lemmatized
              # Term Document Frequency
         corpus = [id2word.doc2bow(text) for text in texts]   
              # print(corpus[:1])
         print("corpus의 값:{0}".format(matutils.Sparse2Corpus(x)))
         print("self.type:{0}".format(self.type))
         if self.type == "1":
          lda_model = gensim.models.ldamodel.LdaModel(
              matutils.Sparse2Corpus(x),
              id2word=id2word,
              num_topics=3,
              passes=30)
         else:
              lda_model = gensim.models.ldamodel.LdaModel(
              id2word=id2word,
              num_topics=3,
              passes=30)
         data = lda_model.print_topics(num_words=10)
         print("data:{0}".format(data))
         doc_lda = lda_model[corpus]
     #     print('\nPerplexity: ', lda_model.log_perplexity(corpus)) # a measure of how good the model is. lower the better.
     #            # Compute Coherence Score
     #     coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v') 
     #     coherence_lda = coherence_model_lda.get_coherence()
     #     print('\nCoherence Score: ', coherence_lda)
         prepared_data = gensimvis.prepare(lda_model, corpus, id2word,mds='tsne')
         pyLDAvis.display(prepared_data)
         pyLDAvis.save_html(prepared_data,'visualization/templates/agrifoodtfidf/onion.html')
    def remove_stopwords(self,texts):
       return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in self.stop_words] for doc in texts]

    def make_bigrams(self, texts,bigram_mod):
       return [bigram_mod[doc] for doc in texts] 

    def lemmatization(self, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']): #표준형변환을 진행하기 위해서 사용하는 함수
        # """https://spacy.io/api/annotation"""
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        texts_out = []
        for sent in texts:
          doc = nlp(" ".join(sent))
          texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags]) 
          return texts_out   