import leidenalg
import igraph as ig
import pymysql
import pandas as pd
import time
import numpy as np

path = r"C:\Users\79806\Desktop\SPO三元组\多谓词多疾病知识网络实验\predicate_count_selected.txt"
file_path = r"C:\Users\79806\Desktop\SPO三元组\多谓词多疾病知识网络实验\\"
predicate_pd = pd.read_csv(path,sep='\t',usecols=[0],header=None,names=['predicate'])
predicate_list = predicate_pd['predicate'].tolist()

refs = pd.read_csv(file_path+'predication_selected_pmid_reference_new.txt',sep='\t',header=0,names=['PMID','PMID_to'])


# predicate_list = ['AFFECTS','ASSOCIATED_WITH','AUGMENTS','CAUSES','COEXISTS_WITH','COMPLICATES',
#                   'DIAGNOSES','DISRUPTS','LOCATION_OF','MANIFESTATION_OF','MEASURES','OCCURS_IN',
#                   'PART_OF','PRECEDES','PREDISPOSES','PREVENTS','PRODUCES','TREATS']

db = pymysql.connect(host="localhost", user="root", password="hbw4897218", port=3306,db='pubmed')
cursor = db.cursor()

sql_disease = 'SELECT selected_disease from selected_diseases'
try:
    print('START')
    diseases_pd = pd.read_sql(sql_disease,db)
    print('sql_disease ok!')
except:
    print('sql_disease error!')
diseases = diseases_pd['selected_disease'].tolist()

network_id = 0
for predicate in predicate_list:
    print(predicate)
    # predicate = 'INTERACTS_WITH'
    pre_nodes = pd.read_csv(file_path + 'nodes_time_{}.csv'.format(predicate),usecols=[1,2,3,4,5,6])
    # pre_nodes = np.array(pre_nodes)
    # pre_nodes_list = pre_nodes.tolist()
    for disease in diseases:
        # disease = 'Diabetes'
        print(disease)
        edges_list = []
        nodes_list = []

        # start = time.perf_counter()
        # print('START')

        nodes_pd = pre_nodes.loc[(pre_nodes['SUBJECT_NAME']==disease) | (pre_nodes['OBJECT_NAME']==disease)]
        nodes_pd.insert(0, 'ID', range(0, len(nodes_pd)))

        # print(nodes_pd)
        new_pd1 = pd.merge(refs, nodes_pd.iloc[:, [0, 2]], how='inner', on='PMID')
        new_pd1.columns = ['PMID_FROM', 'PMID', 'ID_FROM']
        edges_pd = pd.merge(new_pd1, nodes_pd.iloc[:, [0, 2]], how='inner', on='PMID')
        # print(edges_pd)
        nodes_list = nodes_pd.values.tolist()
        edges_list = edges_pd.iloc[:, [2, 3]].values.tolist()

        # end = time.perf_counter()
        # print('Running time: %s Seconds' % (end - start))

        # sql = "SELECT TID1,TID2 FROM all_pmid_list_new_reference WHERE EQ_PREDICATE='{}'".format(predicate)
        # print(sql)
        # try:
        #     edge = pd.read_sql(sql,db)
        #     edge = np.array(edge)
        #     # 然后转化为list形式
        #     edges_list = edge.tolist()
        #     # print(edges_list)
        # except:
        #     print("error")
        #
        # sql = "SELECT * FROM myeloma_time WHERE predicate = '{}'".format(predicate)
        # print(sql)
        # try:
        #     node = pd.read_sql(sql, db)
        #     node = np.array(node)
        #     # 然后转化为list形式
        #     nodes_list = node.tolist()
        #     # print(nodes_list)
        # except:
        #     print('error')

        # sql_nodes = 'SELECT a.*,citations.PYEAR from ' \
        #             '(SELECT PREDICATION_ID,PMID,PREDICATE,SUBJECT_NAME,OBJECT_NAME FROM predication_selected ' \
        #             'where PREDICATE="{}" and (SUBJECT_NAME="{}" OR OBJECT_NAME="{}")) a ' \
        #             'LEFT JOIN citations on a.PMID=citations.PMID'.format(predicate,disease,disease)
        # start = time.perf_counter()
        # try:
        #     print('START')
        #     nodes = pd.read_sql(sql_nodes, db)
        # except:
        #     print('{}+{} sql_nodes error!'.format(predicate,disease))
        #     break
        # if nodes.shape[0]==0:
        #     print('{}+{} 结果为空!'.format(predicate, disease))
        #     break
        # end = time.perf_counter()
        # print(nodes.shape)
        # print('{}+{} sql_nodes Running time: %s Seconds'.format(predicate,disease) % (end - start))

        # sql_edges = 'SELECT * FROM predication_selected_pmid_reference b ' \
        #             'WHERE b.PMID_from AND b.PMID_to IN ' \
        #             '(SELECT a.PMID FROM predication_selected a ' \
        #             'where a.PREDICATE="{}" and (a.SUBJECT_NAME="{}" OR a.OBJECT_NAME="{}"))'.format(predicate,disease,disease)
        #
        # start = time.perf_counter()
        # try:
        #     edges = pd.read_sql(sql_edges, db)
        # except:
        #     print('{}+{} sql_edges error!'.format(predicate,disease))
        #     break
        # end = time.perf_counter()
        # print(edges.shape)
        # print('{}+{} sql_edges Running time: %s Seconds'.format(predicate,disease) % (end - start))

        # nodes.to_csv(file_path + 'nodes\\{}+{}+{}.csv'.format(predicate, disease,len(nodes)))
        # edges.to_csv(file_path + 'edges\\{}+{}+{}.csv'.format(predicate,disease,len(edges)))

        for year in range(1962, 2020, 3):
            G = ig.Graph(directed=True)
            G.add_vertices(len(nodes_list))
            G.add_edges(edges_list)

            # 待解决
            for node in nodes_list:
                G.vs[node[0]]['PREDICATION_ID'] = node[1]
                G.vs[node[0]]['PMID'] = node[2]
                G.vs[node[0]]['PREDICATE'] = node[3]
                G.vs[node[0]]['SUBJECT_NAME'] = node[4]
                G.vs[node[0]]['OBJECT_NAME'] = node[5]
                G.vs[node[0]]['PYEAR'] = node[6]

            # 删除不存在的节点
            delete_ids = [v.index for v in G.vs if v.degree() == 0]
            G.delete_vertices(delete_ids)

            delete_ids = [v.index for v in G.vs if v['PYEAR']>year]
            G.delete_vertices(delete_ids)
            if len(G.es) <= 3:
                continue
            print(year)
            # print(len(G.vs))
            # print(predicate)
            community = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)
            community_len = len(community)
            community_scale = []
            entities_list = []
            com_id = 0
            com_true_len = 0
            for com in community:
                entity = []
                if len(com)==1:
                    break
                for c in com:
                    someone = G.vs[c]
                    if someone['SUBJECT_NAME']==disease:
                        entity.append(someone['OBJECT_NAME'])
                    else:
                        entity.append(someone['SUBJECT_NAME'])
                community_scale.append(len(com))
                com_true_len = com_true_len + 1
                entity = pd.Series(entity)  # 转换数据类型
                entity_len = entity.value_counts().to_dict()  # 计数
                entity_len = str(entity_len)
                entity_list = [network_id, com_id, predicate, disease, year,len(com),com_true_len,entity_len]
                entities_list.append(entity_list)
                com_id = com_id + 1

            density = G.density()  # 网络密度
            transitivity = G.transitivity_avglocal_undirected()  # 平均聚类系数
            ave_path_len = G.average_path_length()  # 平均路径长度
            ave_degree = ig.mean(G.degree())  # 平均度
            node_len = len(G.vs)
            edge_len = len(G.es)
            community_scale = str(community_scale)
            output = [[network_id, predicate, disease, year, node_len, edge_len, density, transitivity,
                      ave_path_len, ave_degree, community_len, com_true_len,community_scale]]
            # print(output)

            df = pd.DataFrame(output,columns=['network_id', 'predicate', 'disease','year','node_len',
                                              'edge_len','density','transitivity','ave_path_len',
                                              'ave_degree', 'community_len', 'com_true_len','community_scale'])
            df2 = pd.DataFrame(entities_list,columns=['network_id','com_id','predicate','disease','year',
                                                      'com_len','com_true_len','entity_len'])
            df.to_csv(file_path + 'community_ac//community_{}.csv'.format(predicate),mode='a',header=False)
            df2.to_csv(file_path + 'entity_ac//entity_{}.csv'.format(predicate), mode='a', header=False)

            network_id = network_id+1

            # 输出每个社区的每个三元组节点
            # i = 1
            # output = []
            # for p in community:
            #     for pp in p:
            #         someone = G.vs[pp]
            #         list = []
            #         list.append(someone['PREDICATION_ID'])
            #         list.append(someone['PMID'])
            #         list.append(someone['PREDICATE'])
            #         list.append(someone['SUBJECT_NAME'])
            #         list.append(someone['OBJECT_NAME'])
            #         list.append(someone['PYEAR'])
            #         list.append(i)
            #         output.append(list)
            #     i = i+1

