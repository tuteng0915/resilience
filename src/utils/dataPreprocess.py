"""
Data Preprocessing
** 已经手动修正了部分数据，因此dataPreprocess不再建议使用 **
"""
import os
import pandas as pd
import numpy as np


def dataPreprocess(write=False):
    for i, j, k in os.walk(r"./data/raw"):
        fileList = k
    print(fileList)

    all_data = []
    for fileName in fileList:
        file = pd.read_csv(r"./data/raw/" + fileName)
        file = file.dropna(axis=0, how='all')
        temp = []
        if fileName == 'Baseline_selfreport.csv':
            file = file.drop([0, 1], axis=0)
            for j in file.keys()[17:-2]:
                temp.append(file[j].values)
            df = pd.DataFrame(np.array(temp).T, columns=file.keys()[17:-2])
            df.sort_values([file.keys()[19]], ascending=True, inplace=True)
            df.reset_index(drop=True, inplace=True)
            if write:
                df.to_csv(r'./data/' + fileName)
            all_data.append(pd.DataFrame(np.array(temp).T, columns=file.keys()[17:-2]))
        elif fileName in ['CognitiveData_Cold.csv', 'CognitiveData_Hot.csv']:
            for j in file.keys():
                temp.append(file[j].values)
            df = pd.DataFrame(np.array(temp).T, columns=file.keys())
            df.sort_values([file.keys()[1]], ascending=True, inplace=True)
            df.reset_index(drop=True, inplace=True)
            if write:
                df.to_csv(r'./data/' + fileName)
            all_data.append(pd.DataFrame(np.array(temp).T, columns=file.keys()))
        else:
            print(file)
            if fileName == 'Cold_Post_selfreport.csv':
                file = file.drop([1, 3], axis=0)
            else:
                file = file.drop([0, 1], axis=0)
            if fileName in ['Cold_Post_selfreport.csv', 'Hot_Post_selfreport.csv']:
                for j in file.keys()[17:-1]:
                    temp.append(file[j].values)
                df = pd.DataFrame(np.array(temp).T, columns=file.keys()[17:-1])
            else:
                for j in file.keys()[17:]:
                    temp.append(file[j].values)
                df = pd.DataFrame(np.array(temp).T, columns=file.keys()[17:])

            df.sort_values([file.keys()[17]], ascending=True, inplace=True)
            df.reset_index(drop=True, inplace=True)
            if write:
                df.to_csv(r'./data/'+fileName)

            if fileName in ['Cold_Post_selfreport.csv', 'Hot_Post_selfreport.csv']:
                all_data.append(pd.DataFrame(np.array(temp).T, columns=file.keys()[17:-1]))
            else:
                all_data.append(pd.DataFrame(np.array(temp).T, columns=file.keys()[17:]))
    #print(all_data)
    return all_data
