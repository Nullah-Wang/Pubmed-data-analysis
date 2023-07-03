import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_time = pd.read_csv('community_all.csv',usecols=[1,2,3,11,13,16])
predicate_list = data_time['predicate'].unique()
disease_list = data_time['disease'].unique()
g =[]
c = []
s = []
for predicate in predicate_list:
    g_list = []
    c_list = []
    s_list = []
    for disease in disease_list:
        data = data_time.loc[(data_time['predicate']==predicate) & (data_time['disease']==disease)]
        if len(data)!=0:
            max_df = data.loc[data['year'] == 2019]
            min_df = data.loc[(data['year'] == data['year'].min())]
            gap_g = max_df['gini']-min_df['gini']
            # print(max_df)
            gap_c = max_df['com_true_len']-min_df['com_true_len']
            gap_s = max_df['similarity_com']-min_df['similarity_com']
            print(gap_g)
            g_list.append(gap_g)
            c_list.append(gap_c)
            s_list.append(gap_s)
        else:
            print('nope')
    g.append(g_list)
    c.append(c_list)
    s.append(s_list)
    break
# print(g)
plt.boxplot(x = g,
            patch_artist=True,
            labels = predicate_list, # 添加具体的标签名称
            showmeans=True
            # boxprops = {'color':'black','facecolor':'blck'},
            # flierprops = {'marker':'o','markerfacecolor':'red','color':'pink'}
            # meanprops = {'linestyle':'-','markerfacecolor':'indianred'},
            # medianprops = {'linestyle':'s','color':'black'}
            )

# 显示图形
plt.show()