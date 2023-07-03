import pandas as pd
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
import random
import numpy as np
import time

path = r"C:\Users\79806\Desktop\SPO三元组\时序路径excel\gephi_output\\"
data_node_dict = pd.read_csv(path+'diagnose_node_6.21.csv',sep=',',index_col=0,header='infer',usecols=[0,1,4])
data_node = pd.read_csv(path+'diagnose_node_6.21.csv',sep=',',header='infer',usecols=[0,1,4])
data_edge = pd.read_csv(path+'diagnose_edge_6.21.csv',sep=',',header='infer',usecols=[0,1])

nodes = data_node.values[0::,0::]
edges = data_edge.values[0::,0::]
nodes = nodes.tolist()
edges = edges.tolist()
nodes_dict = data_node_dict.to_dict()

print(nodes)
print(edges)

year = 2017
rubbish = []
while year>1955:
    nodes_update = []
    edges_update = []
    for item in nodes:
        if item[2]<year:
            nodes_update.append(item)
        else:
            rubbish.append(item[0])
    nodes = nodes_update
    for item in edges:
        if item[0] not in rubbish and item[1] not in rubbish:
            edges_update.append(item)
    edges = edges_update
    print(year)
    print(len(nodes))
    print(edges)

    # 构建网
    # 节点：[1,label='Kidney Function Tests']
    # 边：[1,200]
    G = nx.Graph()

    for node in nodes:
        G.add_node(node[0],label=node[1])
    G.add_edges_from(edges)

    # 社区检测：格纹算法
    # communities = girvan_newman(G)
    # for com in next(communities):
    #     node_groups.append(list(com))
    communities = greedy_modularity_communities(G)
    print(len(communities))
    print("==================")
    # node_groups = []

    count = 1
    output = []
    for node_group in communities:
        # print(node_group)
        num = len(node_group)
        for node in node_group:
            y = nodes_dict['dp:int'][node]
            if y<year and y>=year-3:
                list = []
                list.append(node)
                list.append(nodes_dict['Label'][node])
                list.append(nodes_dict['dp:int'][node])
                list.append(count)
                list.append(num)
                output.append(list)
        count = count+1
    df = pd.DataFrame(output,columns=['id','node','year','class','num'])
    df.to_csv(path+'community_gap3_{}.csv'.format(year))
    year = year-3
