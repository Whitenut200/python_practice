#!/usr/bin/env python
# coding: utf-8

# # COVID-19 (Chinese tourists)

# ### 코로나 바이러스의 영향으로 중국인 관광객이 얼마나 줄었는지 알아보자

# ## 1. 모든 데이터를 불러올 함수 만들기

# In[11]:


import pandas as pd
def create_kto_data(yyyy,mm):
    # 파일 불러오기
    file_path='G:/내 드라이브/파이썬/4_Tourists_Event/files/kto_{}{}.xlsx'.format(yyyy,mm)
    
    # 엑셀 불러오기
    # header:1열 목차로, skipfooter:밑에 4열 없앰, usecols:A에서 G열까지만 출력
    df=pd.read_excel(file_path,header=1,skipfooter=4,usecols='A:G')
    
    # '기준년월' 칼럼 추가
    df['기준년월']='{}-{}'.format(yyyy,mm)
    
    # '국적' 칼럼에서 특정 국적 제외
    ignore_list=['아시아주','미주','구주','대양주','아프리카주','기타대륙','교포소계']
    
    # ignore_list에 포함 되지 않는 국가명만 선택
    condition=(df['국적'].isin(ignore_list)==False)
    
    # 인덱스 초기화 # 로우 인덱스 값이 존재
    df_country=df[condition].reset_index(drop=True) 
    
    # '대륙' 칼럼 추가
    continents=['아시아']*25+['아프리카']*5+['유럽']*23+['대양주']*3+['아프리카']*2+['기타대륙']+['교포']
    df_country['대륙']=continents
    
    # 국가별 '관광객비율(%)' 칼럼 추가
    df_country['관광객비율(%)']=round(df_country.관광/df_country.계*100,1)
    
    # '전체비율(%)' 칼럼 추가 (전체 관광객중 해당 관광객)
    tourist_sum=sum(df_country['관광'])
    df_country['전체비율(%)']=round(df_country['관광']/tourist_sum*100,1)
    
    # 결과
    return(df_country)


# In[12]:


# 2018년 10월 데이터 불러오기
kto_test=create_kto_data(2018,10)
kto_test.head()


# ##  2. 모든 데이터 하나로 합치기

# ### (1) kto_(yyyydd)에 맞게 기준월일 (yyyydd)로 바꾸기 (이중 반목문)

# In[14]:


for yyyy in range(2010,2021):
    for mm in range(1,13):
        mm_str=str(mm).zfill(2)
        yymm='{}{}'.format(yyyy,mm_str)
        print(yymm)


# ### (2) 이중 반목문을 통해 데이터 하나로 합치기

# In[15]:


df=pd.DataFrame()
# 연도는 2010년 부터 2020년도 까지
for yyyy in range(2010,2021):
    # 월은 1월부터 12일
    for mm in range(1,13):
        # 202006~202012까지의 데이터 누락 
        try :
            
            temp=create_kto_data(str(yyyy),str(mm).zfill(2))
            
            # 가져온 데이터 모두 합치기
            df=df.append(temp)
        except:
            pass


# In[16]:


df.head(10)


# In[17]:


df.info()


# ### (3)  합친 데이터 저장

# In[18]:


df.to_excel('G:/내 드라이브/파이썬/4_Tourists_Event/files/kto_total.xlsx',index=False)


# ## 4. 국적별 관광객 데이터 저장하기

# In[20]:


cntry_list=df['국적'].unique()


# In[21]:


cntry_list


# In[24]:


len(cntry_list)


# In[25]:


condition=(df['국적']=='중국')


# In[27]:


df_2=df[condition]
df_2.head(10)


# In[23]:


for cntry in cntry_list:
    # 국적 하나하나 대입
    condition=(df['국적']==cntry)
    df_filter=df[condition]
    
    # 국적명을 반영한 파일명 만들기
    file_path='G:/내 드라이브/파이썬/4_Tourists_Event/files/[국적별 관광객 데이터] {}.xlsx'.format(cntry)
    
    # 저장하기
    df_filter.to_excel(file_path, index=False)


# ## 5. 시각화

# ### (1) 시계열 그래프

# In[29]:


import matplotlib.pyplot as plt


# In[30]:


from matplotlib import font_manager, rc
import platform

if platform.system()=='Windows':
    path='c:/Windows/Fonts/malgun.ttf'
    font_name=font_manager.FontProperties(fname=path).get_name()
    rc('font',family=font_name)
elif platform.system()=='Darwin':
    rc('font',family='AppleGothic')
else:
    print('Check your OS system')


# In[31]:


# 중국
condition=(df['국적']=='중국')
df_filter=df[condition]
df_filter.head(10)


# In[32]:


plt.plot(df_filter['기준년월'],df_filter['관광'])
plt.show()


# In[35]:


# 꾸미기
# 그래프 크기 조절
plt.figure(figsize=(12,4)) # 가로 12 세로 4

plt.plot(df_filter['기준년월'],df_filter['관광'])

# 그래프 & 축 이름
plt.title('중국 관광객 추이')
plt.xlabel('기준년월')
plt.ylabel('관광객수')

# x축 눈금 값 설정
plt.xticks(['2010-01','2011-01','2012-01','2012-01','2013-01','2014-01','2015-01','2016-01','2017-01','2018-01','2019-01','2020-01',])

plt.show()


# #### 1. 2015년 6월 전까지 증가 추세
# #### 2. 2015년 6월에 관광객 수 감소 ( 메르스)
# #### 3. 2017년 1월에도 관광객 수 감소(사스 보복)
# #### 4. 2020년도에 거의 0에 가까워짐 (코로나)

# In[41]:


# 중국, 일본, 대만, 미국, 홍콩 시계열 그래프 그리기
cntry_list=['중국','일본', '대만', '미국', '홍콩']

for cntry in cntry_list:
    plt.figure(figsize=(12,4))
    condition=(df['국적']==cntry)
    df_filter=df[condition]
    plt.plot(df_filter['기준년월'],df_filter['관광'])
    plt.title('{} 관광객 추이'.format(cntry))
    plt.xlabel('기준년월')
    plt.ylabel('관광객수')
    
    plt.xticks(['2010-01','2011-01','2012-01','2012-01','2013-01','2014-01','2015-01','2016-01','2017-01','2018-01','2019-01','2020-01',])
    plt.show()



# ### 히트맵

# In[42]:


# 연도, 월 생성
df['년도']=df['기준년월'].str.slice(0,4)
df['월']=df['기준년월'].str.slice(5,7)
df.head()


# In[43]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[44]:


# 중국
condition=(df['국적']=='중국')
df_filter=df[condition]


# In[45]:


# 피벗테이블
df_pivot=df_filter.pivot_table(values='관광', index='년도',columns='월')
df_pivot


# In[46]:


plt.figure(figsize=(16,10))
# annot:실제값 표시 fmt:소수점이 없는 실수형 cmap:색 조합
sns.heatmap(df_pivot, annot=True, fmt='.0f',cmap='rocket_r')
plt.title('중국 관광객 히트맵')
plt.show()


# #### 1. 점차 증가하다가 2015년 6-7월에 감소 (메르스)
# #### 2. 다시 증가하다가 2017년 4-6월 감소 (사드보복)
# #### 3. 2020년 3-5월 대폭 감소 (코로나)

# In[48]:


# 중국, 일본, 대만, 미국, 홍콩 시계열 그래프 그리기
cntry_list=['중국','일본', '대만', '미국', '홍콩']

for cntry in cntry_list:
    plt.figure(figsize=(12,4))
    condition=(df['국적']==cntry)
    df_filter=df[condition]
    
    df_pivot=df_filter.pivot_table(values='관광', index='월',columns='년도')
    sns.heatmap(df_pivot, annot=True, fmt='.0f',cmap='rocket_r')
    plt.title('{} 관광객 추이'.format(cntry))

    plt.show()


# In[ ]:




