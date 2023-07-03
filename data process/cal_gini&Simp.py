import pandas as pd
import random
import numpy as np
import time
import matplotlib as mpl
import matplotlib.pyplot as pl
from scipy.integrate import odeint
from scipy import spatial
import json
from collections import Counter
import os
import pymysql


def gini(input):
    cum_input = np.cumsum(sorted(np.append(input, 0)))
    #print(cum_input)
    # 加上0，再排序，再计算cumsum
    # 取最后一个，也就是原数组的和
    sum_input = cum_input[-1]
    #print(sum_input)
    # 倒数第一个
    # 人数的累积占比
    # 就是每个点都会产生一个横坐标
    xarray = np.array(range(0, len(cum_input))) / np.float64(len(cum_input) - 1)
    # 均衡收入曲线
    # 就是45度曲线
    upper = xarray
    # 收入累积占比
    yarray = cum_input / sum_input
    # print(xarray)
    # print(yarray)
    # cumsum的占比
    # 绘制基尼系数对应的洛伦兹曲线
    pl.plot(xarray, yarray)
    pl.plot(xarray, upper)
    # 上面画的是45度线
    # ax.plot(xarray, yarray)
    # ax.plot(xarray, upper)
    # ax.set_xlabel(u'人数累积占比')
    # ax.set_ylabel(u'收入累积占比')
    # pl.show()
    # 计算曲线下面积的通用方法
    B = np.trapz(yarray, x=xarray)
    # 总面积 0.5
    A = 0.5 - B
    G = A / (A + B)
    return G

def simpson(input):
    sum = 0
    a = 0
    for i in range(len(input)):
        sum = sum + input[i]
    if sum != 0:
        for i in range(len(input)):
            b = input[i] / sum
            a = a + b ** 2
    else:
        a = 0
    simpson_result = 1 - a
    return simpson_result

def similarity(max, p_community):
    # # result1 = pd.get_dummies(data.node).groupby(data.community).apply(max)
    #
    # # 计算每个社区每种实体的个数
    # result = data.groupby(['community', 'entity']).size()
    # # print(result)
    #
    # # 计算每个社区的N
    # community_len = data['community'].value_counts()
    # # print(community_len)
    #
    # # 分别返回社区和实体的不重复列表
    # community = data['community'].unique()
    # label = data['entity'].unique()
    #
    # dict = {}
    # for i in range(len(label)):
    #     dict[i] = label[i]
    # # print(dict)
    # # print(label)
    # # print(community)
    # # print(result[1])
    # max = []
    #
    # sum = 0
    # s = []
    # for i in range(len(community)):
    #     sum = sum + community_len[community[i]]
    # for i in range(len(community)):
    #     s.append(community_len[community[i]] / sum)
    #
    # for i in range(len(community)):
    #     line = []
    #     for j in range(len(label)):
    #         try:
    #             line.append(result[community[i]][label[j]])
    #         except:
    #             line.append(0)
    #     # print(line)
    #     max.append(line)
    # print('start')
    # print(max)
    label = max.columns.values.tolist()
    community = max._stat_axis.values.tolist()
    max = np.array(max)
    # print(community)
    num = len(max)
    similarity = 0
    TD_sum = 0
    for i in range(num):
        for j in range(i + 1, num):
            cos_sim = 1 - spatial.distance.cosine(max[i], max[j])
            TD_ij = cos_sim * p_community[i] * p_community[j]
            TD_sum = TD_sum + TD_ij
            similarity = similarity + cos_sim
    if TD_sum != 0:
        td = 1/TD_sum
    else:
        td = 0
    N1 = len(label)
    N2 = len(community)
    if (N1 * N1 - 1) !=0:
        similarity_ent = 2 * similarity / (N1 * N1 - 1)
    else:
        similarity_ent = 0
    if (N2 * N2 - 1) !=0:
        similarity_com = 2 * similarity / (N2 * N2 - 1)
    else:
        similarity_com = 0
    return similarity_ent, similarity_com, td


# 读取mysql中的谓词列表 21个元素
path = r"C:\Users\79806\Desktop\SPO三元组\多谓词多疾病知识网络实验\predicate_count_selected.txt"
# predicate_pd = pd.read_csv(path,sep='\t',usecols=[0],header=None,names=['predicate'])
# predicate_list = predicate_pd['predicate'].tolist()

file_path = r'C:\Users\79806\Desktop\SPO三元组\论文用图\{}_Alzheimer_community_cal.csv'
# file_path2 = r'C:\Users\79806\Desktop\SPO三元组\论文用图\{}_Alzheimer_community_cal_similarity.csv'
file_path2 = r'{}_Alzheimer_community_cal_similarity.csv'
path_community = r'C:\Users\79806\Desktop\SPO三元组\论文用图\{}_Alzheimer_community.csv'
# path_entity = r'C:\Users\79806\Desktop\SPO三元组\论文用图\{}_Alzheimer_community_entity.csv'
path_entity = r'{}_Alzheimer_community_entity.csv'
# file_list = os.listdir(path)
output_list = []
# print(file_list)

predicate_list = ["TREATS"]
diseases= ["Alzheimer's Disease"]

for predicate in predicate_list:
    entity_data_pd = pd.read_csv(path_entity.format(predicate),header=0)
    entity_data = entity_data_pd.iloc[:, 0:].values.tolist()
    # print(entity_data_pd)
    # community_data_pd = pd.read_csv(path_community.format(predicate),header=0)
    # community_data = community_data_pd.iloc[:,0:].values.tolist()
    # start = 0
    # new_community_list = []
    # network_len = len(community_data)
    network_len = 13
    # for community in community_data:
    #     print('{}_{}_{}'.format(predicate,community[2],community[0]))
    #     # 计算辛普森和基尼系数
    #     # community_len_list = community[-1].strip('[').strip(']').split(', ')
    #     community_len_list = json.loads(community[-1])
    #     community_len_list = list(map(int, community_len_list))
    #     # print(community_len_list)
    #     if community_len_list[-1] == 1:
    #         community_len_list.pop()
    #     # print(community_len_list)
    #
    #     if int(community[-2]) ==0:
    #         gini_result = 0
    #         simpson_result = 0
    #         similarity_ent = 0
    #         similarity_com = 0
    #         td = 0
    #         community.pop()
    #         new_community = community + [community_len_list, gini_result, simpson_result,
    #                                      similarity_ent, similarity_com, td]
    #         new_community_list.append(new_community)
    #         continue
    #
    #     c_sum = sum(community_len_list)
    #     # print(sum)
    #     p_community = [a/c_sum for a in community_len_list]
    #     # print(p_community)
    #     # print(community_len_list)
    #     simpson_result = simpson(community_len_list)
    #     gini_result = gini(community_len_list)
    #     # print(gini)
    #
    #     network_id = community[0]
    #     community_size = int(community[-2])
    #     max = {}
    #     for i in range(start, start+community_size):
    #         # print(entity_data[i][0])
    #         max[entity_data[i][1]] = eval(entity_data[i][7])
    #     start = start + community_size
    #
    #     max = pd.DataFrame(max).T.fillna(0)
    #     # print(max)
    #     similarity_ent, similarity_com, td = similarity(max, p_community)
    #     community.pop()
    #     new_community = community + [community_len_list,gini_result,simpson_result,
    #                                  similarity_ent, similarity_com, td]
    #     new_community_list.append(new_community)
    # df = pd.DataFrame(new_community_list, columns=['network_id', 'predicate', 'disease', 'year', 'node_len',
    #                                                'edge_len', 'density', 'transitivity', 'ave_path_len',
    #                                                'ave_degree', 'community_len', 'com_true_len', 'community_scale',
    #                                                'gini', 'simpson', 'similarity_ent', 'similarity_com', 'TD'])
    # df.to_csv(file_path.format(predicate), index=False)

    community_similarity = []
    for i in range(network_len-1):
        j = i+1
        for cur_id in range(len(entity_data_pd[entity_data_pd['network_id']==i])):
            for next_id in range(len(entity_data_pd[entity_data_pd['network_id']==j])):
                print("{}-{}-{}".format(i,cur_id,next_id))
                # print(entity_data_pd[entity_data_pd['network_id']==i])
                cur_com = entity_data_pd[entity_data_pd['network_id']==i].iloc[cur_id]
                # print(cur_com)
                next_com = entity_data_pd[entity_data_pd['network_id'] == j].iloc[next_id]
                # print(next_com)
                max = {}
                max[0] = eval(cur_com['entity_len'])
                max[1] = eval(next_com['entity_len'])
                # print(max[0])
                # print(max)
                max = pd.DataFrame(max).T.fillna(0)
                # print(max.iloc[0])
                cos_sim = 1 - spatial.distance.cosine(max.iloc[0], max.iloc[1])
                community_similarity.append([i,cur_com['com_id'], j,next_com['com_id'], cos_sim])
    df = pd.DataFrame(community_similarity, columns=['network_id1', 'com_id1', 'network_id2', 'com_id2', 'community_similarity'])
    df.to_csv(file_path2.format(predicate), index=False)



# for k in range (0,len(file_list)):
#     file = file_list[k]
#     file_name = file.strip('community_leiden_').strip('.csv')
#     print(file_name)
#     if file_name.startswith('community_leiden'):
#         continue
#     data_input = pd.read_csv(path+'\\community_leiden_{}.csv'.format(file_name),sep=',',header='infer',usecols=[4,5,7])
#     data_input.columns = ['subject','object', 'community']
#
#     # 删除病名，将三列合并为两列
#     data = pd.DataFrame(columns = ['entity', 'community'])
#     for i in range(len(data_input)):
#         if data_input.loc[i][0] == 'Multiple Myeloma':
#             entity = data_input.loc[i][1]
#         else:
#             entity = data_input.loc[i][0]
#         data.loc[i] = [entity, data_input.loc[i][2]]
#     # print(data)
#
#     community_count = data['community'].value_counts()
#     community_count = community_count.values[0::]
#     community_count = community_count.tolist()
#     # community_count为每个社群的个数列表：[49,30,3,1]
#     print(community_count)
#     simpson_result = simpson(community_count)
#     gini_result = gini(community_count)
#     similarity_ent, similarity_com, N = similarity(data)
#     output = [file_name, N, gini_result, similarity_ent, similarity_com, simpson_result]
#     output_list.append(output)
#     df = pd.DataFrame(output_list,columns=['predicate', 'N', 'gini', 'similarity_ent', 'similarity_com', 'simpson'])
#     df.to_csv(path + '//community_leiden_1_result.csv',mode='a', header=False,index=False)
