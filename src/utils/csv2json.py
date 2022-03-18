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


def fromPreSelfReport(filepath: str = './data/Hot_Pre_selfreport.csv', mode: str = "Hot"):
    """
    Get a simplified json containing only the columns we care about
    [{
        'userId':,
        'VAS':,
        'STAI':{}
        'PSS':{}
    },]
    :param filepath
    :param mode: Cold or Hot
    :return: str(json), dict(userId: dict(..))
    """
    stai_label = ['calm', 'tense', 'upset', 'relaxed', 'content', 'worried']
    file = pd.read_csv(filepath)
    js = list(dict())
    dic = dict()
    for index, row in file.iterrows():
        entity = {"userId": int(row['Q1'])}
        if mode == "Cold":
            entity[str("VAS_Pre_" + mode)] = float(row['Q4_1']) / 100
        else:
            entity[str("VAS_Pre_" + mode)] = float(row['Q5_1']) / 100
        stai = dict()
        for i in range(6):
            stai[stai_label[i]] = (float(row['Q2_' + str(i + 1)]) - 1.0) / 4
        entity['STAI_Pre_' + mode] = stai.copy()
        pss = dict()
        for i in range(4):
            pss['PSS_' + str(i + 1)] = (float(row['Q3_' + str(i + 1)]) - 1.0) / 4
        entity['PSS_Pre_' + mode] = pss.copy()
        # print(entity)
        js.append(entity)
    with open('./data/json/Hot_Pre_selfreport.json', encoding='utf8', mode='w') as f:
        json.dump(js, f, indent=4)
    return js


def fromPostSelfReport(filepath: str = './data/Cold_Post_selfreport.csv', mode: str = "Cold"):
    """
    Get a simplified json containing only the columns we care about
    [{
        'userId':,
        'VAS':,
        'STAI':{}
        'PSS':{}
    },]
    :param filepath
    :param mode: Cold or Hot
    :return: str(json), dict(userId: dict(..))
    """
    stai_label = ['calm', 'tense', 'upset', 'relaxed', 'content', 'worried']
    file = pd.read_csv(filepath)
    js = list(dict())
    dic = dict()
    for index, row in file.iterrows():
        entity = {"userId": int(row['Q1'])}
        entity[str("VAS_Post_" + mode)] = float(row['Q13_1']) / 100
        stai = dict()
        for i in range(6):
            stai[stai_label[i]] = (float(row['Q2_' + str(i + 1)]) - 1.0) / 4
        entity['STAI_Post_' + mode] = stai.copy()
        pss = dict()
        for i in range(4):
            pss['PSS_' + str(i + 1)] = (float(row['Q3_' + str(i + 1)]) - 1.0) / 4
        entity['PSS_Post_' + mode] = pss.copy()

        entity['Threatening_' + mode] = (float(row['Q4_1']) - 1.0) / 4
        entity['Ability_' + mode] = (float(row['Q5_1']) - 1.0) / 4
        entity['Confident_' + mode] = 1.0 - (float(row['Q6_1']) - 1.0) / 10
        entity['Engagement_' + mode] = (float(row['Q9_1']) - 1.0) / 4
        entity['Excited_' + mode] = (float(row['Q10_1']) - 1.0) / 4
        entity['Difficulty_' + mode] = (float(row['Q11_1']) - 1.0) / 4

        # print(entity)
        js.append(entity)
    with open('./data/json/Cold_Post_selfreport.json', encoding='utf8', mode='w') as f:
        json.dump(js, f, indent=4)
    return js


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

        erq_ca = dict()
        erq_index = {1: 'Q12_1', 2: 'Q12_2', 3: 'Q12_3', 4: 'Q12_4', 5: 'Q12_5',
                     6: 'Q8_1', 7: 'Q8_2', 8: 'Q8_3', 9: 'Q8_4', 10: 'Q8_5'}
        for i in erq_index:
            erq_ca['ERQ_CA_Q' + str(i)] = (float(row[erq_index[i]]) - 1.0) / 4
        entity['EQR_CA'] = erq_ca.copy()

        smm = dict()
        for i in range(8):
            smm['SMM_G_' + str(i + 1)] = (float(row['Q9_' + str(i + 1)]) - 1.0) / 4
        entity['SMM_G'] = smm.copy()

        maas_a = dict()
        maas_index = {1: 'Q10_1', 2: 'Q10_2', 3: 'Q10_3', 4: 'Q10_4', 5: 'Q10_5',
             6: 'Q10_6', 7: 'Q10_7', 8: 'Q13_1', 9: 'Q13_2', 10: 'Q13_3',
             11: 'Q13_4', 12: 'Q10_5', 13: 'Q10_6', 14: 'Q10_7'}
        for i in maas_index:
            maas_a['MAAS_A_Q' + str(i)] = (float(row[maas_index[i]]) - 1.0) / 4
        entity['MAAS_A'] = maas_a.copy()

        entity['MA'] = (float(row['Q11_1']) - 1.0) / 4

        # print(entity)
        js.append(entity)
    with open('./data/json/Baseline_selfreport.json', encoding='utf8', mode='w') as f:
        json.dump(js, f, indent=4)
    return js


def formParticipant(filepath: str = './data/raw/SID participant name.csv'):
    file = pd.read_csv(filepath)
    js = list(dict())
    for index, row in file.iterrows():
        entity = {"userId": int(row['Subject ID']),
                  "gender": str(row['Gender']),
                  "session_1": str(row['Session 1']),
                  "session_2": str(row['Session 2'])}
        js.append(entity)
    with open('./data/json/participant.json', encoding='utf8', mode='w') as f:
        json.dump(js, f, indent=4)
    return js
