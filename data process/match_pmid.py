import pandas as pd

# 读取并处理txt数据
f1 = open('predication_selected_pmid.txt',encoding='utf-8')
f2 = open('predication.txt',encoding='utf-8')

line = (f1.readline().strip())
pmid_data = []
while line:
    pmid_data.append(line)
    line = f1.readline().strip()

line = f2.readline().strip()
a = line.split('\t')
ref_data = []
while line:
    ref_data.append(a)
    line = f2.readline().strip()
    a = line.split('\t')

f1.close()
f2.close()

# 转换为int格式
pmid_data = list(int(x) for x in pmid_data)
ref_data = list([int(y[0]),int(y[1])] for y in ref_data)

# 排序
pmid_data.sort()
ref_data.sort(key=lambda x:x[0])

print(pmid_data)
print(ref_data)

# 匹配
pmid_len = len(pmid_data)
ref_len = len(ref_data)
i = 0
j = 0
m = 0
result = []
while i<pmid_len and j<ref_len:
    m = m+1
    if pmid_data[i]==ref_data[j][0]:
        result.append(ref_data[j])
        j = j+1

    elif pmid_data[i] > ref_data[j][0]:
        j = j + 1
    else:
        i = i+1
    if m % 1000 == 0:
        print('已完成%d次,ref已完成%d/%d,pmid已完成%d/%d' % (m,j, ref_len, i, pmid_len))

print(result)

df = pd.DataFrame(result)
df.to_csv('predication_selected_pmid_reference_new.txt', sep='\t', index=False, header=[ 'PMID_from', 'PMID_to'])


