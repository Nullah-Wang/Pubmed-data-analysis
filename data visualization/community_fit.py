import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# path = r'D:\PychamProject\HBW\community_cal（网络数据计算结果）\\'
# dir = os.listdir(path)
# print(dir)
cnames = {
'aqua':                 '#00FFFF',
'black':                '#000000',
'blue':                 '#0000FF',
'blueviolet':           '#8A2BE2',
'brown':                '#A52A2A',
'burlywood':            '#DEB887',
'cadetblue':            '#5F9EA0',
'chartreuse':           '#7FFF00',
'chocolate':            '#D2691E',
'coral':                '#FF7F50',
'cornflowerblue':       '#6495ED',
'crimson':              '#DC143C',
'darkblue':             '#00008B',
'darkcyan':             '#008B8B',
'darkgoldenrod':        '#B8860B',
'darkgray':             '#A9A9A9',
'darkgreen':            '#006400',
'darkkhaki':            '#BDB76B',
'darkmagenta':          '#8B008B',
'darkolivegreen':       '#556B2F',
'darkorange':           '#FF8C00',
'darkorchid':           '#9932CC',
'darkred':              '#8B0000'}

colors = list(cnames.keys())
all_info = pd.read_csv('community_all.csv')
disease_list = all_info['disease'].unique()
predicate_list = all_info['predicate'].unique()
index_list = ['com_true_len','gini','similarity_com','TD']
for disease in disease_list:
    disease_info = all_info[all_info.disease == disease]
    for index in index_list:
        for i in range(len(predicate_list)):
            predicate = predicate_list[i]
            data = disease_info[disease_info.predicate == predicate]
            # data = predicate_info
            x = data['year']
            y = data[index]
            if len(y) ==0:
                continue
            # print(y)
            z1 = np.polyfit(x, y, 3)    # 曲线拟合，返回值为多项式的各项系数
            p1 = np.poly1d(z1)          # 返回值为多项式的表达式，也就是函数式子
            # print(p1)
            y_pred = p1(x)              # 根据函数的多项式表达式，求解 y
            plot1 = plt.plot(x, y, '*', label=predicate,color=colors[i])
            plot2 = plt.plot(x, y_pred, 'r',color=colors[i])

            # if i ==4:
            #     break
        plt.title('')
        plt.xlabel('')
        plt.ylabel('')
        plt.legend(loc=2, bbox_to_anchor=(1.05, 1.0), borderaxespad=0.,fontsize=5)
        plt.subplots_adjust(right=0.8)
        if not os.path.exists(f'./fitpic_{index}'):
            os.makedirs(f'./fitpic_{index}')
        plt.savefig(f'./fitpic_{index}/{disease}.png', dpi=250)
        plt.close()
