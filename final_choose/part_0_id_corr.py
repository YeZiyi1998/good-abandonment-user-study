import json
from kappa import fleiss_kappa
import numpy as np

with open('id/id_all.json','r') as f:
    lines = f.readlines()
    user_name2user_id = json.loads(lines[0])
    user_id2info = json.loads(lines[1])

def vote3(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                return arr[i]
    return np.median(arr[i])

def changed(user_id2info):
    total_dic = {}
    for user_id in user_id2info.keys():
        for item in user_id2info[user_id]:
            if item['id'] not in total_dic.keys():
                total_dic[item['id']] = []
            total_dic[item['id']].append(item)
    merge_dic = {}
    for qid in total_dic.keys():
        merge_dic[qid] = {}
        for key in total_dic[qid][0].keys():
            if key != 'end_info':
                merge_dic[qid][key] = total_dic[qid][0][key]
        merge_dic[qid]['end_info'] = {'rel':{}, 'nes':{}, 'type':{}}
        for k2 in total_dic[qid][0]['end_info']['rel'].keys():
            merge_dic[qid]['end_info']['rel'][k2] = [total_dic[qid][i]['end_info']['rel'][k2] for i in range(3)]
        for k2 in total_dic[qid][0]['end_info']['nes'].keys():
            merge_dic[qid]['end_info']['nes'][k2] = [total_dic[qid][i]['end_info']['nes'][k2] for i in range(3)]
        for k2 in total_dic[qid][0]['end_info']['type'].keys():
            merge_dic[qid]['end_info']['type'][k2] = [total_dic[qid][i]['end_info']['type'][k2] for i in range(3)]
    json.dump(merge_dic, open('id/id_all.merged.json','w'))

def vote(user_id2info, if_sorted=True):
    total_dic = {}
    for user_id in user_id2info.keys():
        for item in user_id2info[user_id]:
            if item['id'] not in total_dic.keys():
                total_dic[item['id']] = []
            total_dic[item['id']].append(item)
    merge_dic = {}
    for qid in total_dic.keys():
        merge_dic[qid] = {}
        for key in total_dic[qid][0].keys():
            if key != 'end_info' and key not in ['bad_ab_doc_list','good_ab_doc_list','other_doc_list']:
                merge_dic[qid][key] = total_dic[qid][0][key]
        merge_dic[qid]['end_info'] = {'rel':{}, 'nes':{}, 'type':{}}
        for k2 in total_dic[qid][0]['end_info']['rel'].keys():
            merge_dic[qid]['end_info']['rel'][k2] = np.mean([total_dic[qid][i]['end_info']['rel'][k2] for i in range(3)])
        for k2 in total_dic[qid][0]['end_info']['nes'].keys():
            merge_dic[qid]['end_info']['nes'][k2] = vote3([total_dic[qid][i]['end_info']['nes'][k2] for i in range(3)])
        for k2 in total_dic[qid][0]['end_info']['type'].keys():
            merge_dic[qid]['end_info']['type'][k2] = vote3([total_dic[qid][i]['end_info']['type'][k2] for i in range(3)])
        # change sort
        if if_sorted:
            merge_dic[qid]['doc_list'] = [item + [idx] for idx, item in enumerate(merge_dic[qid]['doc_list'])]
            merge_dic[qid]['doc_list'] = sorted(merge_dic[qid]['doc_list'], key=lambda t:t[-2])
            reflect_dic = {}
            for idx,item in enumerate(merge_dic[qid]['doc_list']):
                reflect_dic[item[-1]] = idx
            merge_dic[qid]['doc_list'] = [item[:-1] for idx, item in enumerate(merge_dic[qid]['doc_list'])]
            for end_info_key in merge_dic[qid]['end_info'].keys():
                tmp = merge_dic[qid]['end_info'][end_info_key].copy()
                for tmp_key in tmp.keys():
                    if tmp[tmp_key] != 0:
                        merge_dic[qid]['end_info'][end_info_key][str(reflect_dic[int(tmp_key)])] = tmp[tmp_key]

    if if_sorted:
        json.dump(merge_dic, open('id/id_all.vote.'+'sorted.'+'json','w'))
    else:
        json.dump(merge_dic, open('id/id_all.vote.'+'json','w'))


def static():
    merge_dic = json.load(open('id/id_all.merged.json'))
    data = {'rel':[],  'nes':[], 'type':[]}
    for key in data.keys():
        for qid in merge_dic.keys():
            for item in merge_dic[qid]['end_info'][key].values():
                if key != 'nes':
                    data[key].append([0 for i in range(5)])
                else:
                    data[key].append([0 for i in range(2)])
                for index in item:
                    data[key][-1][index-1] += 1
    for key in data.keys():
        print(key, fleiss_kappa(data[key], len(data[key]), len(data[key][0]), 3))
# def difference():

static()
# changed(user_id2info)
# vote(user_id2info)

