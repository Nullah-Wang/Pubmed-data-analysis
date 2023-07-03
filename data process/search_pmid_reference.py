import pandas as pd
import numpy as np

# =====excel输入，需先添加predication_id===============
# disease = 'treat_subname_time'
# pmid_list = 'all_pmid_list_new'
# sheet = pd.read_excel('./{}.xlsx'.format(pmid_list), sheet_name="myeloma_time")
# inputs = np.array(sheet)
# i = 0
# id_list = []
# id_list = sheet['PMID'].tolist()

# =====txt输入，没有predication_id=============
pmid_list = 'predication_selected_pmid'
file = open("{}.txt".format(pmid_list))
inputs = file.readlines()

results = []
none_id = []
ref_pair = []
old_id = 0
a = 0
b = 0
c = len(inputs)
for pmid in inputs:
    # print(pmid)
    item = collection.find_one({'pmid': pmid})
    a = a+1
    if item:
        b = b+1
        result = [item["pmid"], item["pub_date"], item["ref_num"], item["refs"], item["cit_num"], item["cits"],
                  item["pub_year"]]
        results.append(result)
        #         print(result)
        refs = item['cits']
        for ref in refs:
            if ref in id_list:
                ref_pair.append([pmid, ref])
    else:
        none_id.append(pmid)
    old_id = pmid
    if a % 100 == 0:
        print("已完成进度：%d/%d，查询成功进度：%d/%d" % (a,c,b,c))


df1 = pd.DataFrame(results)
df2 = pd.DataFrame(none_id)
df3 = pd.DataFrame(ref_pair)
df1.to_csv('{}_citation.csv'.format(pmid_list), index=False,
           header=['pmid', 'pub_date', 'ref_num', 'refs', 'cit_num', 'cits', 'pub_year'])
df2.to_csv('{}_left_id.csv'.format(pmid_list), index=False)
df3.to_csv('{}_reference.csv'.format(pmid_list), index=False, header=[ 'PMID1', 'PMID2'])
print("ok")