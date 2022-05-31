#Import packages
from calendar import day_name
from os import stat
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()

# id: root
# pwd: autoset
# ip: localhost:3306
# database: teamProject
engine = create_engine(f"mysql+mysqldb://{'root'}:{'autoset'}"\
                    f"@{'localhost'}:3306/{'teamProject'}",
                    encoding="utf-8")

# conn = pymysql.connect(host='localhost', user='root', passwd='autoset',charset='utf8',database='teamProject')

# cursur = conn.cursor()

# e = cursur.execute("select * from for_analyze")

anal_data = pd.read_sql(con=engine, sql="select * from for_analyze")    # db에서 for_analyze view 전달

anal_data = anal_data.where(pd.notnull(anal_data), anal_data.mean(), axis='columns') # 분석을 위해 NaN 값을 평균으로 대체
anal_data = anal_data.drop(['legal_code'], axis=1)

print(anal_data)

feature_list = anal_data.columns[1:6]
# print(feature_list)
features = anal_data.iloc[:, 1:6]
# print(features)
# print(feature_list)

stats.pearsonr(features['petHosp_cnt'], features['abandoned_cnt'])

def corr_c(dataframe):
    col_length=len(dataframe.columns)
    idx_length=len(dataframe.index)
    for idx in range(idx_length):
        for col in range(col_length):
            dataframe.iloc[idx,col] = stats.pearsonr(features[feature_list[idx]], features[feature_list[col]])[0]
    return dataframe
            
def corr_p(dataframe):
    col_length=len(dataframe.columns)
    idx_length=len(dataframe.index)
    for col in range(col_length):
        for idx in range(idx_length):
            dataframe.iloc[idx,col] = stats.pearsonr(features[feature_list[idx]], features[feature_list[col]])[1]
    return dataframe

#correlation coefficient dataframe
corr_coefficient=pd.DataFrame(np.zeros((5,5)))
corr_coefficient.columns = feature_list
corr_coefficient.index = feature_list

corr_c(corr_coefficient)

#correlation P-values dataframe
corr_p_values=pd.DataFrame(np.zeros((5,5)))
corr_p_values.columns = feature_list
corr_p_values.index = feature_list

corr_p(corr_p_values)

#correlation coefficient heatmap
plt.figure(figsize=(5,5))
plt.title("correlation coefficient")
sns.heatmap(corr_coefficient, annot=True, fmt = '.4f', linewidths=.5, cmap='Blues')
# plt.show()

#correlation P-values heatmap
plt.figure(figsize=(5,5))
plt.title("corr p-value")
sns.heatmap(corr_p_values, annot=True, fmt = '.5f', linewidths=.5, cmap='Reds')
# plt.show()

#Scatterplots for specific variables
sns.lmplot(x='petHosp_cnt', y='abandoned_cnt', data=features, line_kws={'color':"red"}, ci=None)
plt.title("vs pet hospital")
#plt.show()


sns.lmplot(x='income_lv', y='abandoned_cnt', data=features, line_kws={'color':"red"}, ci=None)
plt.title("vs income level")
#plt.show()

sns.lmplot(x='medi_expense', y='abandoned_cnt', data=features, line_kws={'color':"red"}, ci=None)
plt.title("vs medical expense")
#plt.show()

sns.lmplot(x='pet_count', y='abandoned_cnt', data=features, line_kws={'color':"red"}, ci=None)
plt.title("vs pet count")
plt.show()

