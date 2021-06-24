import json
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
import random
import os

base_path = '../../user_data'
input_dir_list = ['first_0', 'first_1', 'first_2']

output_dir = 'first'

dis_select = [82]

def merge_dic():
    total_dic = {}
    for dir_name in input_dir_list:
        with open(base_path + '/' + dir_name + '/' + 'end_info.txt') as f:
            for line in f.readlines():
                line_list = line.strip().split('\t')
                if len(line_list) > 1:
                    qid = line_list[0]
                    end_info = json.loads(line_list[1])
                    total_dic[qid] = end_info
    with open(base_path + '/' + output_dir + '/' + 'end_info.json','w') as f:
        f.write(json.dumps(total_dic))
        f.write('\n')

def analysis_dic():
    with open(base_path + '/' + output_dir + '/' + 'end_info.json','r') as f:
        total_dic = json.loads(f.readlines()[0])
    name2grade = {
        'rel': ['1','2','3','4','5'],
        'type':['答案框+图片','答案框','文本链接','文本链接+图片','其他'],
        'nes': ['必要', '不必要'],
        'spec': ['1','2','3','4','5'],
        'total': ['很差','差','一般','好','很好']
    }
    name2y = {
        'rel': [0, 0, 0, 0, 0],
        'type':[0, 0, 0, 0, 0],
        'nes': [0, 0],
        'spec': [0, 0, 0, 0, 0],
        'total': [0, 0, 0, 0, 0]
    }
    for qid in total_dic.keys():
        for key in total_dic[qid].keys():
            for k, v in total_dic[qid][key].items():
                if v > 0: 
                    name2y[key][v-1] += 1
    for key in name2grade.keys():
        plt.bar(name2grade[key], name2y[key])
        plt.savefig(base_path + '/' + output_dir + '/' + key+'.png')
        plt.cla()                  

def choose_test():
    with open(base_path + '/' + output_dir + '/' + 'end_info.json','r') as f:
        total_dic = json.loads(f.readlines()[0])
    fine_qid = []
    fine_qid_2 = []
    total_good_ab = 0
    total_bad_ab = 0
    for qid in total_dic.keys():
        good_ab = 0
        bad_ab = 0
        for i in range(20):
            if total_dic[qid]['rel'][str(i)] > 3 and total_dic[qid]['nes'][str(i)] == 2:
                good_ab += 1
            elif total_dic[qid]['rel'][str(i)] <= 3 and total_dic[qid]['nes'][str(i)] == 2:
                bad_ab += 1
        total_bad_ab += bad_ab
        total_good_ab += good_ab
        if good_ab >= 1 and bad_ab >= 1:
            fine_qid.append(qid)
        if good_ab >= 1 or bad_ab >= 1:
            fine_qid.append(qid)
    with open('select_list.txt','w') as fw:
        for qid in fine_qid:
            fw.write(str(qid)+'\n')
    print(fine_qid)
    print('len(fine_qid): ',len(fine_qid))
    print("bad_ab", total_bad_ab)
    print("good_ab", total_good_ab)
    return 

def pilot_choose():
    queries = {}
    with open('../platform_annotation/query/static/query/mobile_data/query.txt') as f:
        for idx, line in enumerate(f.readlines()):
            queries[idx] = line.strip()
    with open(base_path + '/' + output_dir + '/' + 'end_info.json','r') as f:
        total_dic = json.loads(f.readlines()[0])

    pilot_json = []
    fine_qid = []
    for qid in total_dic.keys():
        if qid == '82':
            continue
        if total_dic[qid]['total'] in [1,2]:
            continue
        good_ab = []
        bad_ab = []
        for i in range(20):
            if total_dic[qid]['rel'][str(i)] >= 3 and total_dic[qid]['nes'][str(i)] == 2:
                good_ab.append(i)
            elif total_dic[qid]['rel'][str(i)] < 3 and total_dic[qid]['nes'][str(i)] == 2:
                bad_ab.append(i)
        if (len(good_ab) >= 1 and len(bad_ab) >= 1):
            # choose this one
            bad_ab_num = random.randint(0, min(5, len(bad_ab)))
            good_ab_num = random.randint(1, min(2, len(good_ab)))
            tmp_pilot_json = {
                'id': int(qid),
                'query': queries[int(qid)],
                'good_ab_doc_list': [],
                'bad_ab_doc_list': [],
                'other_doc_list':[],
                'doc_list': [],
            }
            select_num = []
            select_num_id = {}
            tmp_idx = 0
            for i in range(20):
                png_name = str(qid)+'_'+str(i)+'.png'
                if os.path.exists('../platform_annotation/query/static/query/mobile_data/'+'crop/'+png_name) and os.path.exists('../platform_annotation/query/static/query/mobile_data/'+'landing_page/'+png_name):
                    select_num.append(['crop/'+png_name, 'landing_page/'+png_name, i])
                    select_num_id[select_num[-1][-1]] = tmp_idx
                    tmp_idx += 1
                elif i == 0 and os.path.exists('../platform_annotation/query/static/query/mobile_data/'+'crop/'+png_name):
                    select_num.append(['crop/'+png_name, 'crop/'+png_name, i])
                    select_num_id[select_num[-1][-1]] = tmp_idx
                    tmp_idx += 1
            if len(select_num) < 6:
                continue
            for i in range(len(good_ab)):
                if good_ab[i] in select_num_id.keys():
                    tmp_pilot_json['good_ab_doc_list'].append(select_num_id[good_ab[i]])
            for i in range(len(bad_ab)):
                if bad_ab[i] in select_num_id:
                    tmp_pilot_json['bad_ab_doc_list'].append(select_num_id[bad_ab[i]])
            for i in range(len(select_num)):
                if select_num[i][-1] not in good_ab and select_num[i][-1] not in bad_ab:
                    tmp_pilot_json['other_doc_list'].append(i)
            if (len(tmp_pilot_json['good_ab_doc_list']) < 1 or len(tmp_pilot_json['bad_ab_doc_list']) < 1):
                continue
            random.shuffle(tmp_pilot_json['good_ab_doc_list'])
            random.shuffle(tmp_pilot_json['bad_ab_doc_list'])
            tmp_pilot_json['other_doc_list'] += tmp_pilot_json['bad_ab_doc_list'][bad_ab_num:]
            tmp_pilot_json['other_doc_list'] += tmp_pilot_json['good_ab_doc_list'][1:]
            random.shuffle(tmp_pilot_json['other_doc_list'])
            tmp_pilot_json['doc_list'] = tmp_pilot_json['bad_ab_doc_list'][:bad_ab_num] + tmp_pilot_json['good_ab_doc_list'][:1] + tmp_pilot_json['other_doc_list']
            print(tmp_pilot_json)
            tmp_pilot_json['doc_list'] = [select_num[item] for item in tmp_pilot_json['doc_list']]
            pilot_json.append(tmp_pilot_json)
    print('len(pilot_json) ', len(pilot_json))
    with open('../../random_data/pilot.json','w') as fw:
        fw.write(json.dumps(pilot_json))      
    

# analysis_dic()
# merge_dic()
# choose_test()
pilot_choose()

