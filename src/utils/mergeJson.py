"""
Combine the user performance and report from the four questionnaires
"""
import json


def mergeJson(filepath: str = './data/json/'):
    """
    :param filepath
    :return: dict(userId: dict(..))
    """
    merged_dict = dict()
    with open(filepath + 'Baseline_selfreport.json', encoding='utf8', mode='r') as f:
        baseline = json.load(f)
    with open(filepath + 'CognitiveData_Cold.json', encoding='utf8', mode='r') as f:
        cog_cold = json.load(f)
    with open(filepath + 'CognitiveData_Hot.json', encoding='utf8', mode='r') as f:
        cog_hot = json.load(f)
    with open(filepath + 'Cold_Pre_selfreport.json', encoding='utf8', mode='r') as f:
        cold_pre = json.load(f)
    with open(filepath + 'Cold_Post_selfreport.json', encoding='utf8', mode='r') as f:
        cold_post = json.load(f)
    with open(filepath + 'Hot_Pre_selfreport.json', encoding='utf8', mode='r') as f:
        hot_pre = json.load(f)
    with open(filepath + 'Hot_Post_selfreport.json', encoding='utf8', mode='r') as f:
        hot_post = json.load(f)
    with open(filepath + 'participant.json', encoding='utf8', mode='r') as f:
        participant = json.load(f)

    for entity in cog_cold:
        userId = int(entity['userId'])
        entity.pop('userId')
        merged_dict[userId] = {'cognitiveData_Cold': entity.copy()}
    for entity in cog_hot:
        userId = int(entity['userId'])
        entity.pop('userId')
        if userId in merged_dict:
            merged_dict[userId]['cognitiveData_Hot'] = entity.copy()
        else:
            merged_dict[userId] = {'cognitiveData_Hot': entity.copy()}
    for q in [baseline, participant, cold_pre, cold_post, hot_pre, hot_post]:
        for entity in q:
            userId = int(entity['userId'])
            if q is baseline:
                entity.pop('gender')
            entity.pop('userId')
            if userId in merged_dict:
                merged_dict[userId] = dict(merged_dict[userId], **entity)
            else:
                merged_dict[userId] = entity.copy()
    merged_dict = dict(sorted(merged_dict.items(), key=lambda d: d[0]))
    with open('./data/json/merged.json', encoding='utf8', mode='w') as f:
        json.dump(merged_dict, f, indent=4)
    print('{} total entities'.format(len(merged_dict)))

    closure = merged_dict.copy()
    for userId in merged_dict:
        entity = merged_dict[userId]
        if not (('cognitiveData_Cold' in entity) and ('cognitiveData_Hot') in entity
                and ('VAS_Post_Cold' in entity) and ('VAS_Post_Hot' in entity)
                and ('VAS_Pre_Cold' in entity) and ('VAS_Pre_Hot' in entity) and ('SMM_G' in entity)):
            closure.pop(userId)
    closure = dict(sorted(closure.items(), key=lambda d: d[0]))
    with open('./data/json/closure.json', encoding='utf8', mode='w') as f:
        json.dump(closure, f, indent=4)
    print('{} total entities'.format(len(closure)))
    return merged_dict






