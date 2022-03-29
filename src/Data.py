import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow import keras
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
from collections import Counter

def readData(url):
    with open(url, encoding='utf8', mode='r') as f:
        data = json.load(f)
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

def data_mapping(data,keys,key_word):
    find_data = []
    for i in range(len(keys)):
        if key_word in keys[i]:
            find_data.append(data[:,i])
    return np.array(find_data)

def ML_train_test_data(data,keys):
    temp_c = data_mapping(data,keys,"Cold")
    temp_h = data_mapping(data,keys,"Hot")
    temp_l = len(data)
    X = np.vstack((temp_c.T,temp_h.T))
    Y = np.hstack((np.zeros(temp_l),np.ones(temp_l)))
    y = keras.utils.to_categorical(np.hstack((np.zeros(temp_l),np.ones(temp_l))))
    X_train, X_test, y_train, y_test = train_test_split(X,y,shuffle=True)
    # print(X.shape,y.shape)
    return X_train, X_test, y_train, y_test,X,Y


data_both,data_both_keys = readData(r'C:\Users\Mingshuyue\Downloads\Track 3 and 4_AquaPressure\resilience\data\json\subdivision\both.json')
data_mapping(data_both,data_both_keys,"Baseline")