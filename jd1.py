# import pandas
# info = pandas.read_csv('jd12.csv',encoding='gbk')
# print(type(info))
# print(info.dtypes)
# print(info.head())
# print(info.columns)
# print(info.shape)
# print(info.loc[0])
# print(info['cid'])
# print(info.columns.tolist())
# all_names = info.columns.tolist()
# id_columns = []
#
# for id in all_names:
#     if id.endswith('id'):
#         id_columns.append(id)
# id_df = info[id_columns]
# print(id_df.head())

# info1000 = info['reference_id'] + '1000'
# print(info.shape)
# info['ref1000'] = info1000
# print(info.shape)

# info = info.convert_objects(convert_numeric=True)
# print(info.dtypes)

# info.sort_values('comment_id',inplace=True,ascending=False)
# print(info['comment_id'])

import pandas as pd
import numpy as np

# titan = pd.read_csv('泰坦尼克号数据.csv')
# # print(titan.head())
# age = titan['Age']
# # print(age.loc[:10])
# age_is_null = pd.isnull(age)
# print(age_is_null)
# age_null_true = age[age_is_null]
# # print(age_null_true)
# age_null_count = len(age_null_true)
# print(age_null_count)
# c1 = titan['Age'].mean()
# print(c1)


# passenger_classes = [1, 2, 3]
# fares_class = {}
# for this_class in passenger_classes:
#     pclass_rows = titan[titan['Pclass'] == this_class]
#     pclass_fares = pclass_rows['Fare']
#     fare_for_class = pclass_fares.mean()
#     fares_class[this_class] = fare_for_class
# print(fares_class)

# passenger_fares = titan.pivot_table(index='Pclass',values='Fare',aggfunc=np.mean)
# print(passenger_fares)

# new_info = titan.dropna(axis=0,subset=['Age','Cabin'])
# print(new_info)

# def not_null_count(column):
#     column_null = pd.isnull(column)
#     null = column[column_null]
#     return len(null)
#
#
# column_null_count = titan.apply(not_null_count)
# print(column_null_count)


# def is_minor(row):
#     if row['Age'] < 18:
#         return True
#     else:
#         return False
# minors = titan.apply(is_minor,axis=1)
# print(minors)


# fandango = pd.read_csv('fandango_score_comparison.csv')
# series_film = fandango['FILM']
# # print(series_film[:5])
# series_rt = fandango['RottenTomatoes']
# # print(series_rt[:5])
#
# from pandas import Series
#
# film_names = series_film.values
# rt_scores = series_rt.values
# # print(film_names[:5])
# # # print(rt_scores[:5])
# series_custom = Series(rt_scores,index=film_names)
# # print(series_custom)
#
# fiveten = series_custom[5:10]
# print(fiveten)

#
# unrate = pd.read_csv('UNRATE.csv')
# unrate['DATE'] = pd.to_datetime(unrate['DATE'])
# print(unrate.head(12))

import matplotlib as mpl
import matplotlib.pyplot as plt
# plt.plot()
# plt.show()

# 解决中文乱码问题

# sans-serif就是无衬线字体，是一种通用字体族。

# 常见的无衬线字体有 Trebuchet MS, Tahoma, Verdana, Arial, Helvetica, 中文的幼圆、隶书等等。

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体 SimHei为黑体

mpl.rcParams['axes.unicode_minus'] = False # 用来正常显示负号


# first_twelve = unrate[0:8]
# plt.plot(first_twelve['DATE'],first_twelve['VALUE'])
# plt.xticks(rotation=45)
# plt.xlabel('年份')
# plt.ylabel('失业率')
# plt.title('1948年失业率')
# plt.show()

# unrate['MONTH'] = unrate['DATE'].dt.month
# unrate['MONTH'] = unrate['DATE'].dt.month
# fig = plt.figure(figsize=(6,4))
#
# plt.plot(unrate[:12]['MONTH'],unrate[:12]['VALUE'],c='red',label='1948')
# plt.plot(unrate[12:24]['MONTH'],unrate[12:24]['VALUE'],c='blue',label='1949')
# plt.legend(loc='best')
# plt.show()


reviews = pd.read_csv('fandango_score_comparison.csv')
cols = ['FILM','RT_user_norm','Metacritic_user_nom','IMDB_norm','Fandango_Ratingvalue','Fandango_Stars']
norm_reviews = reviews[cols]
num_cols = ['RT_user_norm','Metacritic_user_nom','IMDB_norm','Fandango_Ratingvalue','Fandango_Stars']

bar_heights = norm_reviews.ix[0,num_cols].values # 取第一行
# print(bar_heights)
from numpy import arange
bar_positions = arange(5)+0.75
# # print(bar_positions)
# fig,ax = plt.subplots()
# ax.bar(bar_positions,bar_heights,0.5)
# plt.show()
plt.plot(bar_positions,bar_heights,'--',0.5) # 0.5柱的宽度
plt.show()

# fandango_distribution = norm_reviews['Fandango_Ratingvalue'].value_counts()
# fandango_distribution = fandango_distribution.sort_index() # 排序

# print(fandango_distribution)

# imdb_distribution = norm_reviews['IMDB_norm'].value_counts()
# imdb_distribution = imdb_distribution.sort_index()
# # print(imdb_distribution)
# fig,ax = plt.subplots()
# ax.hist(norm_reviews['Fandango_Ratingvalue'],bins=20,range=(4,5)) # bins总共有几条柱状图 range 哪些区间取数据
# plt.show()

# fig = plt.figure(figsize=(5,5))
# ax1 = fig.add_subplot(4,1,1) # 四行一列
# ax1.hist(norm_reviews['Fandango_Ratingvalue'])
# ax1.set_title('啊啊啊啊啊')
# ax1.set_ylim(0,50) # 设置y轴参数
# # ax2 = fig.add_subplot(4,1,2)
# # ax3 = fig.add_subplot(4,1,3)
# # ax4 = fig.add_subplot(4,1,4)
# plt.show()