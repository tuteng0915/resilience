"""
customize Json
"""
import json


def subdivision(filepath: str = './data/json/'):
    with open(filepath + 'simplified.json', encoding='utf8', mode='r') as f:
        raw = json.load(f)
    ch = dict()
    hc = dict()
    ac = dict()
    ah = dict()
    both = dict()
    for i in raw:
        print(i)
        entry = raw[i]
        if entry['User_Info']['Session_1'] == 'Cold':
            ac[i] = {
                'User_Info': entry['User_Info'],
                'Baseline': entry['Baseline'],
                'CognitiveData': entry['CognitiveData_Cold'],
                'Pre': entry['Pre_Cold'],
                'Post': entry['Post_Cold'],
                'Other': entry['Other_Cold'],
            }
            if entry['User_Info']['Session_2'] == 'Hot':
                ch[i] = entry
                both[i] = entry
        if entry['User_Info']['Session_1'] == 'Hot':
            ah[i] = {
                'User_Info': entry['User_Info'],
                'Baseline': entry['Baseline'],
                'CognitiveData': entry['CognitiveData_Hot'],
                'Pre': entry['Pre_Hot'],
                'Post': entry['Post_Hot'],
                'Other': entry['Other_Hot'],
            }
            if entry['User_Info']['Session_2'] == 'Cold':
                hc[i] = entry
                both[i] = entry
    print(len(ch), len(hc), len(ac), len(ah))
    with open(filepath + 'subdivision/cold-hot.json', encoding='utf8', mode='w') as f:
        json.dump(ch, f, indent=4)
    with open(filepath + 'subdivision/hot-cold.json', encoding='utf8', mode='w') as f:
        json.dump(hc, f, indent=4)
    with open(filepath + 'subdivision/cold-first.json', encoding='utf8', mode='w') as f:
        json.dump(ac, f, indent=4)
    with open(filepath + 'subdivision/hot-first.json', encoding='utf8', mode='w') as f:
        json.dump(ah, f, indent=4)
    with open(filepath + 'subdivision/both.json', encoding='utf8', mode='w') as f:
        json.dump(both, f, indent=4)


def simplifyJson(filepath: str = './data/json/'):
    """
    :param filepath
    :return: dict(userId: dict(..))
    """
    with open(filepath + 'merged.json', encoding='utf8', mode='r') as f:
        raw = json.load(f)

    simplified = dict()
    for i in raw:
        entry = raw[i]
        if ('firstName' not in entry) or \
                (('VAS_Pre_Cold' not in entry or 'VAS_Post_Cold' not in entry or 'cognitiveData_Cold' not in entry)
                 and ('VAS_Pre_Hot' not in entry or 'VAS_Post_Hot' not in entry or 'cognitiveData_Hot' not in entry)):
            continue
        # 合并rt
        try:
            cold = entry["cognitiveData_Cold"]
            cold_ = dict()
            cold_['Reaction'] = (cold['inhibition_rt'] + cold['shifting_rt'] + cold['inversion_rt']) / 3
            cold_['Inhibition'] = cold['inhibition']
            cold_['Shifting'] = cold['shifting']
            cold_['Inversion'] = cold['inversion']
            cold_['Memory'] = cold['memory']
            entry["cognitiveData_Cold"] = cold_.copy()
        except:
            pass
        try:
            hot = entry["cognitiveData_Hot"]
            hot_ = dict()
            hot_['Reaction'] = (hot['inhibition_rt'] + hot['shifting_rt'] + hot['inversion_rt']) / 3
            hot_['Inhibition'] = hot['inhibition']
            hot_['Shifting'] = hot['shifting']
            hot_['Inversion'] = hot['inversion']
            hot_['Memory'] = hot['memory']
            entry["cognitiveData_Hot"] = hot_.copy()
        except:
            pass
        # smm_g
        try:
            smm_g = entry['SMM_G']
            entry['SMM_G'] = (smm_g['SMM_G_2'] + smm_g['SMM_G_4'] + smm_g['SMM_G_6'] + smm_g['SMM_G_8'] + 4.0
                              - smm_g['SMM_G_1'] - smm_g['SMM_G_3'] - smm_g['SMM_G_5'] - smm_g['SMM_G_7']) / 8
        except:
            pass
        # PSS
        try:
            e = entry['PSS_Pre_Cold']
            entry['PSS_Pre_Cold'] = (e['PSS_1'] - e['PSS_2'] - e['PSS_3'] + e['PSS_4'] + 2) / 4
            e = entry['PSS_Post_Cold']
            entry['PSS_Post_Cold'] = (e['PSS_1'] - e['PSS_2'] - e['PSS_3'] + e['PSS_4'] + 2) / 4
        except:
            pass
        try:
            e = entry['PSS_Pre_Hot']
            entry['PSS_Pre_Hot'] = (e['PSS_1'] - e['PSS_2'] - e['PSS_3'] + e['PSS_4'] + 2) / 4
            e = entry['PSS_Post_Hot']
            entry['PSS_Post_Hot'] = (e['PSS_1'] - e['PSS_2'] - e['PSS_3'] + e['PSS_4'] + 2) / 4
        except:
            pass
        # maa
        try:
            maa = 0.0
            for j in range(1, 15, 1):
                maa += entry['MAAS_A']['MAAS_A_Q' + str(j)]
            maa = maa / 14.0 * 4.0 / 5.0
            entry['MAAS_A'] = maa
        except:
            pass
        # stai
        try:
            e = entry['STAI_Pre_Cold']
            entry['STAI_Pre_Cold'] = (e['tense'] + e['upset'] + e['worried'] + 3
                                      - e['calm'] - e['relaxed'] - e['content']) / 6
            e = entry['STAI_Post_Cold']
            entry['STAI_Post_Cold'] = (e['tense'] + e['upset'] + e['worried'] + 3
                                       - e['calm'] - e['relaxed'] - e['content']) / 6
        except:
            pass
        try:
            e = entry['STAI_Pre_Hot']
            entry['STAI_Pre_Hot'] = (e['tense'] + e['upset'] + e['worried'] + 3
                                     - e['calm'] - e['relaxed'] - e['content']) / 6
            e = entry['STAI_Post_Hot']
            entry['STAI_Post_Hot'] = (e['tense'] + e['upset'] + e['worried'] + 3
                                      - e['calm'] - e['relaxed'] - e['content']) / 6
        except:
            pass
        # erq
        try:
            e = entry['EQR_CA']
            cr_index = [1, 3, 5, 7, 8, 10]
            cr = 0.0
            es_index = [2, 4, 6, 9]
            es = 0.0
            for j in cr_index:
                cr += e['ERQ_CA_Q' + str(j)]
            for j in es_index:
                es += e['ERQ_CA_Q' + str(j)]
            entry['ERQ_Cognitive_Reappraisal'] = cr / 6
            entry['ERQ_Expressive_Suppression'] = es / 4
        except:
            pass

        if 'cognitiveData_Cold' not in entry or 'VAS_Post_Cold' not in entry or 'VAS_Pre_Cold' not in entry:
            if entry['session_1'] == 'Cold':
                entry['session_1'] = entry['session_2']
            entry['session_2'] = 'NULL'
        elif 'cognitiveData_Hot' not in entry or 'VAS_Post_Hot' not in entry or 'VAS_Pre_Hot' not in entry:
            if entry['session_1'] == 'Hot':
                entry['session_1'] = entry['session_2']
            entry['session_2'] = 'NULL'

        entry_ = {
            'User_Info': {
                'FirstName': entry['firstName'],
                'LastName': entry['lastName'],
                'Age': entry['age'],
                'Gender': entry['gender'],
                "Session_1": entry['session_1'],
                "Session_2": entry['session_2'],
            },
            'Baseline': {
                'ERQ_Cognitive_Reappraisal': entry['ERQ_Cognitive_Reappraisal'],
                'ERQ_Expressive_Suppression': entry['ERQ_Expressive_Suppression'],
                'SMM_G': entry['SMM_G'],
                'MAAS': entry['MAAS_A'],
                'Math_Anxiety': entry['MA'],
            },
        }
        try:
            entry_['CognitiveData_Cold'] = entry['cognitiveData_Cold']
            entry_['Pre_Cold'] = {
                'VAS': entry['VAS_Pre_Cold'],
                'STAI': entry['STAI_Pre_Cold'],
                'PSS': entry['PSS_Pre_Cold'],
            }
            entry_['Post_Cold'] = {
                'VAS': entry['VAS_Post_Cold'],
                'STAI': entry['STAI_Post_Cold'],
                'PSS': entry['PSS_Post_Cold'],

            }
            entry_['Other_Cold'] = {
                'Threatening': entry['Threatening_Cold'],
                'Ability': entry['Ability_Cold'],
                'Confident': entry['Confident_Cold'],
                'Engagement': entry['Engagement_Cold'],
                'Excited': entry['Excited_Cold'],
                'Difficulty': entry['Difficulty_Cold'],
            }
        except:
            pass
        try:
            entry_['CognitiveData_Hot'] = entry['cognitiveData_Hot']
            entry_['Pre_Hot'] = {
                'VAS': entry['VAS_Pre_Hot'],
                'STAI': entry['STAI_Pre_Hot'],
                'PSS': entry['PSS_Pre_Hot'],
            }
            entry_['Post_Hot'] = {
                'VAS': entry['VAS_Post_Hot'],
                'STAI': entry['STAI_Post_Hot'],
                'PSS': entry['PSS_Post_Hot'],
            }
            entry_['Other_Hot'] = {
                'Threatening': entry['Threatening_Hot'],
                'Ability': entry['Ability_Hot'],
                'Confident': entry['Confident_Hot'],
                'Engagement': entry['Engagement_Hot'],
                'Excited': entry['Excited_Hot'],
                'Difficulty': entry['Difficulty_Hot'],
            }
        except:
            pass
        simplified[i] = entry_.copy()
    with open(filepath + 'simplified.json', encoding='utf8', mode='w') as f:
        json.dump(simplified, f, indent=4)
