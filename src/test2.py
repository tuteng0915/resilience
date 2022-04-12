import json
from xml.etree.ElementTree import tostringlist
from cv2 import mean
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#import seaborn as sns
from scipy import stats
from zmq import PROTOCOL_ERROR_ZMTP_INVALID_SEQUENCE

C_Cold = pd.read_csv(".\data\CognitiveData_Cold.csv")
C_Hot = pd.read_csv(".\data\CognitiveData_Hot.csv")
temp = []
for i in C_Cold.keys():
    temp.append(i)
    if len(temp) < 10:
        continue
    else:
        print(temp)
        temp = []
for i in C_Cold.keys():
    if 'Baseline_RT' in i:
        print(i)
C_Cold
cold_id = [i for i in C_Cold['User']]
hot_id = [i for i in C_Hot['User']]
count_temp = 0
for i in range(len(cold_id)):
    if cold_id[i] not in hot_id:
        # print(i)
        C_Cold = C_Cold.drop(i-count_temp,axis=0)
        # count_temp += 1
cold_id = [i for i in C_Cold['User']]
count_temp = 0
for i in range(len(hot_id)):
    if hot_id[i] not in cold_id:
        # print(i)
        C_Hot = C_Hot.drop(i-count_temp,axis=0)
        # count_temp += 1
key_name = ['Baseline_RT', 'Baseline_TTL',"RI_RT","RI_False_Alarms","Shifting_Congruent_RT","Shifting_Congruent_Accuracy",
    "Shifting_Congruent_FA",'Shifting_1_Shifting_Incongruent_RT', 'Shifting_Incongruent_Accuracy', 
    'Shifting_Incongruent_FA',"Total_Errors","CogInhib_Incongruent_Accuracy",
    "CogInhib_Incongruent_RT",'CogInhib_Incongruent_Accuracy', 
    'Conflict_Resolution_Accuracy', 'Conflict_Resolution_RT',
    'WM_Hits','WM_FA', 'WM_PR', 'Min_moves_exit', 'n_Attempts', 'WM_Return_Efficiency' ]
new_cold_data = {}
for i in key_name:
    temp = []
    for j in C_Cold.keys():
        if i in j:
            temp.append(C_Cold[j])
    new_cold_data[i] = temp
# new_cold_data
new_hot_data = {}
for i in key_name:
    temp = []
    for j in C_Hot.keys():
        if i in j:
            temp.append(C_Hot[j])
    new_hot_data[i] = temp
test_C = np.array(new_cold_data["Shifting_Congruent_FA"]).T
test_H = np.array(new_hot_data["Shifting_Congruent_FA"]).T
test = []
for i in range(len(test_C)):
    test_D = test_C[i] - test_H[i]
    test.append(stats.ttest_1samp(test_D,0).pvalue)
#print(test)

result = {}
for i in key_name:
    test_C = np.array(new_cold_data[i]).T
    test_H = np.array(new_hot_data[i]).T
    test = []
    for j in range(len(test_C)):
        test_D = test_C[j] - test_H[j]
        dffer = np.mean(test_C[j])- np.mean(test_H[j])
        pvalue = stats.ttest_1samp(test_D,0).pvalue
        performance = 1/pvalue *np.sign(dffer)
        test.append(performance)
        
    print(i)
    print(test)
    result[i] = test

'''
result = {}

for i in key_name:
    test_C = np.array(new_cold_data[i])
    test_H = np.array(new_hot_data[i])
    test = []
    for j in range(len(test_C)):
        test_D = test_C[j] - test_H[j]
        test.append(stats.ttest_1samp(test_D,0).pvalue)
    print(i)
    print(test)
'''    
result = pd.DataFrame(result)

result['user'] = C_Cold['User'] 
print(result)
result.to_csv("P_Cognitive_result.csv")