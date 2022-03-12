"""
Complete the conversion of csv to json for subsequent data processing
"""

import json
import pandas as pd
import numpy as np


def fromCognitiveData(filepath='./data/CognitiveData_Hot.csv'):
    """
    Get a simplified json of the user performance
    [{
        userId=,
        inhibition=,  1 - 0.01 * avg(Inhibition_RI_False_Alarms)
        shifting=,    avg(Shifting_Shifting_Incongruent_Accuracy)
        inversion=,   avg(Inversion_CogInhib_Incongruent_Accuracy)
        memory=,      avg(Memory_a_WM_Return_Efficiency)
    },]
    :param filepath
    :return: str(json), dict(userId: dict(..))
    """
    file = pd.read_csv(filepath)
    js = list(dict())
    dic = dict()
    for index, row in file.iterrows():

        inhibition = float(0)
        inhibition_rt = float(0)
        for i in ['1', '2', '3', '4', '5a', '6a', '7a', '8a']:
            inhibition += float(row['Inhibition_' + i + '_RI_False_Alarms'])
            inhibition_rt += float(row['Inhibition_' + i + '_RI_RT'])
        inhibition = 1 - 0.01 * inhibition / 8
        inhibition_rt = inhibition_rt / 8

        shifting = float(0)
        shifting_rt = float(0)
        for i in range(8):
            shifting += float(row['Shifting_' + str(i + 1) + '_Shifting_Congruent_Accuracy'])
            shifting += float(row['Shifting_' + str(i + 1) + '_Shifting_Incongruent_Accuracy'])
            shifting_rt += float(row['Shifting_' + str(i + 1) + '_Shifting_Congruent_RT'])
            shifting_rt += float(row['Shifting_' + str(i + 1) + '_Shifting_Incongruent_RT'])
        shifting = shifting / 16
        shifting_rt = shifting_rt / 16

        inversion = float(0)
        inversion_rt = float(0)
        for i in range(8):
            inversion += float(row['Inversion_' + str(i + 1) + '_CogInhib_Incongruent_Accuracy'])
            inversion_rt += float(row['Inversion_' + str(i + 1) + '_CogInhib_Incongruent_RT'])
        inversion = inversion / 8
        inversion_rt = inversion_rt / 8

        memory = float(0)
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'fg', 'g']:
            memory += float(row['Memory_' + i + '_WM_Return_Efficiency'])
        memory = memory / 8

        entity = {
            'userId': int(row['User']),
            'inhibition': inhibition,
            'inhibition_rt': inhibition_rt,
            'shifting': shifting,
            'shifting_rt': shifting_rt,
            'inversion': inversion,
            'inversion_rt': inversion_rt,
            'memory': memory,
        }
        # print(entity)
        js.append(entity)
        dic[int(row['User'])] = entity.copy()
    with open('./data/json/CognitiveData_Hot.json', encoding='utf8', mode='w') as f:
        json.dump(js, f, indent=4)
    print(dic)
    return dic


def fromPreSelfReport(filepath: str = './data/Cold_Pre_selfreport.csv'):
    """
    Get a simplified json containing only the columns we care about
    [{
        'VAS':,
        'STAI':[]
        'PSS':
    },]
    :param filepath
    :return: str(json), dict(userId: dict(..))
    """
    # load from csv

    # formJson


def fromPostSelfReport(filepath: str = './data/Cold_Post_selfreport.csv'):
    """
    Get a simplified json containing only the columns we care about
    [{


    },]
    :param filepath
    :return: str(json), dict(userId: dict(..))
    """
    # load from csv

    # formJson


def fromBaseline(filepath: str = './data/Baseline_selfreport.csv'):
    """
    Only Stress Mindset General included
    :param filepath
    :return:
    """
    file = pd.read_csv(filepath)
    js = list(dict())
    for index, row in file.iterrows():
        entity = {"firstName": str(row['Q2']),
                  "lastName": str(row['Q14']),
                  "age": int(float(row['Q3'])),
                  "gender": str(row['Q5'])}
        smm = dict()
        for i in range(8):
            smm['SMM_G_' + str(i + 1)] = (float(row['Q9_' + str(i + 1)]) - 1.0) / 4
        entity['SMM_G'] = smm.copy()
        # print(entity)
        js.append(entity)
    with open('./data/json/Baseline_selfreport.json', encoding='utf8', mode='w') as f:
        json.dump(js, f, indent=4)
    return js


