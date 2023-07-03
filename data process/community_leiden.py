import leidenalg
import igraph as ig
# import pymsql
#
#
# db = pymysql.connect(host="localhost", user="root", password="******", port=3306)
# cursor = db.cursor()
#
# predicate_list = ['diagnoses','aaa']
# for predicate in predicate_list:
#     edges_list = []
#     sql = "SELECT * FROM students WHERE predicate = '{}'".format(predicate)
#     try:
#         cursor.execute(sql)
#         print("count:", cursor.rowcount)
#         row = cursor.fetchone()
#         while row:
#             print("Row:", row)
#             # edges_list.append((row[0],row[1]))
#             if row[0]:
#                 name_list.append(row[0])
#             else:
#                 name_list.append(" ")
#             age_list.append(row[1])
#             row = cursor.fetchone()
#     except:
#         print(error)
#
#     sql = "SELECT id1 FROM ralentship WHERE predicate = '{}'".format(predicate)
#     try:
#         cursor.execute(sql)
#         print("count:", cursor.rowcount)
#         row = cursor.fetchone()
#         while row:
#             print("Row:", row)
#             # edges_list.append((row[0],row[1]))
#             nodes_list.append(row)
#             age_list.append(row[1])
#             row = cursor.fetchone()
#     except:
#         print(error)


G = ig.Graph(directed=True)
edge_list = [(1,2),(1,6),(4,5),(3,1)]
G.add_vertices(7)
G.add_edges(edge_list)

# 待解决
for node in nodes_list:
    G.vs[node[0]]['id'] = node[0]
    G.vs[node[0]]['xxx'] = node[1]
    G.vs[node[0]]['aaa'] = node[2]
    G.vs[node[0]]['bbb'] = node[3]
G.vs[3]["name"] =15000
# G.vs["name"] = name_list[1500,1800,]
# G.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
# G.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
# G.es["is_formal"] = [False, False, True, True, True, False, True, False, False]

# 删除不存在的节点
delete_ids = [v.index for v in G.vs if v.degree() == 0]
G.delete_vertices(delete_ids)

print(G)
print("\n")

part = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)
print(part)