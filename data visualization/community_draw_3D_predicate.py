import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from adjustText import adjust_text

data_all = pd.read_csv('community_all.csv',usecols=[1,2,3,11,13,16])
# list = data_all[('predicate','year')].unique()
pair_list = np.array(data_all[['predicate','year']].drop_duplicates()).tolist()
disease_list = data_all['disease'].unique()
# print(pair_list)
index_list = ['com_true_len','gini','similarity_com','TD']
# data_all['color'] = 0
for i in range(len(disease_list)):
    disease = disease_list[i]
    data_all.loc[data_all["disease"]==disease,"color"] = i
# print(data)


for pair in pair_list:
    # print(pair)
    # if pair[1] != 2019:
    #     continue
    if pair[0]!='TREATS':
        break

    print(pair)
    data = data_all.loc[(data_all['predicate']==pair[0]) &( data_all['year']==pair[1])]
    # print(data)

    x=data['similarity_com']
    y=data['gini']
    size = data['com_true_len']
    color = data['color']
    color_li = np.array(color).tolist()
    # print(color)
    plt.figure(figsize=(16, 8))
    scatter = plt.scatter(x, y, s=size, c=color, cmap='rainbow',alpha=0.7)
    # a,b = scatter.legend_elements()
    # print(a)
    # print(b)
    plt.legend(*scatter.legend_elements(),loc="upper right", title="Classes",fontsize=8)
    plt.xlim((0,0.7))
    plt.ylim((0,0.95))
    ax = plt.gca()
    y_major_locator=MultipleLocator(0.1)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.xlabel('similarity_com')
    plt.ylabel('gini')
    plt.title(f'{pair[0]}_{pair[1]}')

    i = 0
    texts = []
    for a,b in zip(x,y):
        texts.append(plt.text(a, b, int(color_li[i]), fontdict={'fontsize':8}))
        i = i+1
    adjust_text(texts)
    plt.savefig(f'./2D_pic/{pair[0]}_{pair[1]}.png', dpi=350)
    plt.close()
    # plt.show()



# for i in range(0,len(predicate_list),10):
#     data = data_all.loc[data_all['color'].isin(range(i,i+10))]
#     x=data['com_true_len']
#     y=data['gini']
#     z=data['similarity_com']
#     color = data['color']
#
#     fig = plt.figure()
#     ax = Axes3D(fig)
#     scatter = ax.scatter(x, y, z, c=color,cmap='rainbow')  #c指颜色，c=label_pred刚好四个分类四个颜色。相比普通三维散点图只改了这里！！！
#     # 添加坐标轴
#     legend1 = ax.legend(*scatter.legend_elements(),loc="lower right", title="Classes")
#     ax.add_artist(legend1)
#     ax.set_xlabel('community_len', fontdict={'size': 10, 'color': 'black'})
#     ax.set_ylabel('gini', fontdict={'size': 10, 'color': 'black'})
#     ax.set_zlabel('similarity', fontdict={'size': 10, 'color': 'black'})
#
#     plt.legend(loc=2)
#     plt.show()