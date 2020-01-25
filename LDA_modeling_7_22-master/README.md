# LDA_modeling_7_22


Topic modeling using LDA algorithm 

주요 기능은 다음과 같습니다.

1. LDA TopicModeling을 이용해서 시설채소 관련 데이터를 토픽별로 시각화할 수 있습니다.
2. 시설채소별 날짜별 관련 키워드들을 추출할 수 있습니다. 
3. 워드클라우드와 점그래프를 이용해서 원하는 키워드를 시각화할 수 있습니다.


### 워드클라우드를 이용한 양파와 관련된 키워드 추출

d3.js의 wordcloud를 이용해서 연도별 양파의 유사한 키워드 추출

![default](imgs/wordcloud.png)

### d3.js를 이용한 날짜별 선택한 키워드 관련된 키워드와 개수 추출

사용자가 키워드와 매체 기간을 설정하면 키워드와 매체에 맞게 연/월/주/일별로 데이터를 뽑아내서 
결과를 line graph로 보여줍니다.

![default](imgs/line.png)


### ldavis를 이용한 시설채소 토픽별 그룹 만들기

사용자가 선택한 시설채소를 기반으로 하여 비슷한 주제를 가진 키워드들을 묶어서 원그래프로 시각해합니다.

![default](imgs/ldavis.png)

