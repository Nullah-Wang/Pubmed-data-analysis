import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

data_all = pd.read_csv('community_all_2019_3D.csv',usecols=[1,11,13,16])
predicate_list = data_all['predicate'].unique()
# index_list = ['com_true_len','gini','similarity_com','TD']
data_all['color'] = 0
for i in range(len(predicate_list)):
    predicate = predicate_list[i]
    data_all.loc[data_all["predicate"]==predicate,"color"] = i
# print(data)

for i in range(0,len(predicate_list),10):
    data = data_all.loc[data_all['color'].isin(range(i,i+10))]
    x=data['com_true_len']
    y=data['gini']
    z=data['similarity_com']
    color = data['color']

    fig = plt.figure()
    ax = Axes3D(fig)
    scatter = ax.scatter(x, y, z, c=color,cmap='rainbow')  #c指颜色，c=label_pred刚好四个分类四个颜色。相比普通三维散点图只改了这里！！！
    # 添加坐标轴
    legend1 = ax.legend(*scatter.legend_elements(),loc="lower right", title="Classes")
    ax.add_artist(legend1)
    ax.set_xlabel('community_len', fontdict={'size': 10, 'color': 'black'})
    ax.set_ylabel('gini', fontdict={'size': 10, 'color': 'black'})
    ax.set_zlabel('similarity', fontdict={'size': 10, 'color': 'black'})

    plt.legend(loc=2)
    plt.show()

# for i in range(0,len(predicate_list),10):
#     data = data_all.loc[data_all['color'].isin(range(i, i + 10))]
#     x=data['similarity_com']
#     y=data['gini']
#     size = data['com_true_len']
#     color = data['color']
#
#     print(color)
#     scatter = plt.scatter(x, y, c=color, s=size*0.1, cmap='rainbow',alpha=0.5)
#     a,b = scatter.legend_elements()
#     print(a)
#     print(b)
#     plt.legend(*scatter.legend_elements(),loc="lower right", title="Classes")
#     # plt.add_artist(legend1)
#     plt.xlabel('similarity_com')
#     plt.ylabel('gini')
#     plt.show()