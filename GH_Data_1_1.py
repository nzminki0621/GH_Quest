#연속형 자료 산점도 해석 및 상관분석(1)
#필요한 패키지 가져오기
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

app_store_df = pd.read_csv("./app_store.csv")       #csv 가져오기

#missing data inspection
total = app_store_df.isnull().sum().sort_values(ascending=False)        
print(total)

#Price, Size, Installs datatype integer로 변환
app_store_df['NPriceD'] = app_store_df.Price.map(lambda x : float(x[1:]))
app_store_df['NSizeM'] = app_store_df.Size.map(lambda x : float(x.rstrip('M').replace(',','')) if(x[-1] == 'M') else float(x.rstrip('k').replace(',',''))/1000)
app_store_df['Installs'] = app_store_df.Installs.map(lambda x : int(x.rstrip('+').replace(',','')))

#Reviews, Installs 상용로그 취하기
app_store_df['Reviews_logscale'] = app_store_df.Reviews.map(lambda x : np.log(x))
app_store_df['Installs_logscale'] = app_store_df.Installs.map(lambda x : np.log(x))

#변환 및 추가된 데이터 missing inspection
total = app_store_df.isnull().sum().sort_values(ascending=False)
print(total)

#R에서 사용하기 위해 데이터프레임 내보내기
app_store_df.to_csv('app_store_modified.csv')

#산점도 그리기
plt.figure(figsize = (8,30))
plt.subplots_adjust(top=1)
columns = ['Reviews','Reviews_logscale','Installs','Installs_logscale', 'NPriceD', 'NSizeM']
ylabels = ['Reviews','log10_Reviews','Installs','log10_Installs', 'Price', 'Size']

#Reviews_logscale과 Reviews에 대한 rating값 linear regression
reg1 = LinearRegression().fit(X = app_store_df['Reviews_logscale'].values.reshape(-1,1), y = app_store_df.Rating)
reg2 = LinearRegression().fit(X = app_store_df['Reviews'].values.reshape(-1,1), y = app_store_df.Rating)

for i in list(range(6)):        #각 열에 대해 산점도 그리기
    plt.subplot(6,1,i+1)
    plt.title('plot'+str(i+1)+'. '+ylabels[i]+' & Rating')
    plt.ylabel('Rating')
    plt.xlabel(ylabels[i])

    if i == 1:                  #Reviews_logscale plot xtick 단위 1
        plt.xticks(list(range(20)))
    elif i == 4:                #Price x값 범위 설정
        plt.xlim(-5,40)
    elif i == 5:                #Size x값 범위 설정
        plt.xlim(-5,150)

    plt.plot( app_store_df[columns[i]],app_store_df.Rating,'o',markersize=2)

    if i == 1:                  #Reviews_logscale 선형회귀 그래프 그리기
        plt.plot([0,14],reg1.predict([[0],[14]]),color = 'r')
    elif i == 0:                #Reviews 선형회귀 그래프 그리기
        plt.plot([1,650000],reg2.predict([[1],[650000]]),color = 'r')

print(app_store_df.corr())

#카테고리별 아노바 분석

#아노바 분석을 위해 싸이파이 패키지 가져오기
import scipy.stats as stats

#모든 카테고리 이름 저장
all_categories = []
for i in list(range(len(app_store_df))):
    if app_store_df['Category'][i] in all_categories:
        pass
    else:
        all_categories.append(app_store_df['Category'][i])

#ANOVA_pairs에 유의확률이 유의수준 이하인 카테고리쌍 저장
ANOVA_pairs = []
for i in list(range(len(all_categories))):
    for j in list(range(i+1, len(all_categories))):
        if stats.f_oneway(app_store_df['Rating'][app_store_df['Category'] == all_categories[i]],
               app_store_df['Rating'][app_store_df['Category'] == all_categories[j]]).pvalue <= 0.05:
               ANOVA_pairs.append([all_categories[i],all_categories[j]])

#해당 두 카테고리의 평균치 대소관계 표시
for i in ANOVA_pairs:
    if app_store_df['Rating'][app_store_df['Category'] == i[0]].mean() > app_store_df['Rating'][app_store_df['Category'] == i[1]].mean():
        print(i[0]+' > '+i[1])
    else:
        print(i[0]+' < '+i[1])