import csv
import json
from operator import length_hint
from threading import local
import numpy as np
import pandas as pd

with open(r'./data/json/subdivision/cold-hot.json', encoding='utf8', mode='r') as f:
    data_ch = json.load(f)
with open(r'./data/json/subdivision/hot-cold.json', encoding='utf8', mode='r') as f:
    data_hc = json.load(f)
with open(r'./data/json/subdivision/both.json', encoding='utf8', mode='r') as f:
    data_bo = json.load(f)
with open(r'./P_Cognitive_result.csv', encoding='utf8', mode='r') as f:
    p_value = pd.read_csv(f)


#获取json中包含的所有键（包括嵌套字典）
def getJsonKey(json_data):
    #递归获取字典中所有key
    key_list=[]
    for key in json_data.keys():
        key_list.append(key)
    return key_list

#print(getJsonKey(data_bo))

def readData(data):
    data_cold_hot = []
    data_keys = []
    for i in data.keys():
        temp = []
        for j in data[i].keys():
            if j == "User_Info":
                continue
            try:
                for k in data[i][j].keys():
                    if j+"_"+k not in data_keys:
                        data_keys.append(j+"_"+k)
                for x in data[i][j].values():
                    temp.append(x)
            except AttributeError:
                temp.append(data[i][j])
                if j not in data_keys:
                    data_keys.append(j)
        data_cold_hot.append(temp)
    data_cold_hot = np.array(data_cold_hot)
    data_keys = np.array(data_keys)
    return data_cold_hot,data_keys

data_cold_hot,data_cold_hot_keys = readData(data_ch)
data_hot_cold,data_hot_cold_keys = readData(data_hc)
data_both,data_both_keys = readData(data_bo)

data = pd.DataFrame(data_both, columns = data_both_keys)
#print(data.shape)
#print(data_both_keys)

p_value.dropna(axis= 0,subset= ['user'],inplace= True)
#print(p_value)

data['userinfo'] = data_bo
data['d_stress_STAI'] = (data['Post_Hot_STAI'] - data['Pre_Hot_STAI']) - (data['Post_Cold_STAI'] - data['Pre_Cold_STAI'])
data['d_stress_VAS'] = (data['Post_Hot_VAS'] - data['Pre_Hot_VAS']) - (data['Post_Cold_VAS'] - data['Pre_Cold_VAS'])

'''
#查看负值个数
a = 0
for value in data['d_stress_STAI']:
   if value < 0:
    a = a+1

a = 0
for value in data['d_stress_VAS']:
   if value < 0:
    a = a+1
print(a)    
'''

p_value= pd.DataFrame(p_value).set_index('user')
data = pd.DataFrame(data).set_index('userinfo')

#print(p_value)
#print(data)

data_p_keys = p_value.columns.values.tolist()
STAI= pd.DataFrame(columns= data_p_keys)
VAS = pd.DataFrame(columns= data_p_keys)

for users in data.index:
    if float(users+'.0') in p_value.index:
        STAI.loc[users] = p_value.loc[float(users+'.0')]/ data.loc[users,'d_stress_STAI']
        VAS.loc[users] = p_value.loc[float(users+'.0')]/ data.loc[users,'d_stress_VAS']

STAI.to_csv("resilience_STAI.csv")
VAS.to_csv("resilience_VAS.csv")

