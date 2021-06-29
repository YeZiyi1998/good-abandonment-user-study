import json
import os
import random
random.seed(2021)
# 90 均匀分布在前6，也就是各15个
base_file = ['id/id_all.vote.sorted.json', 'human/human_all.vote.sorted.json']
total_dic = json.load(open(base_file[0]))
add_dic = json.load(open(base_file[1]))
for k,v in add_dic.items():
    if k not in total_dic.keys():
        total_dic[k] = v

def clean(total_dic):
    wrong_img = ['28_20' ,'39_16', '48_20', '48_21', '59_17', '61_15', '67_20', '68_18', '77_21', '95_17', '95_18', '95_19', '123_18', '131_13', '131_14', '131_15', '131_16', '131_17', '131_18', '132_15']
    for qid in total_dic.keys():
        flag=False
        for idx, item in enumerate(total_dic[qid]['doc_list']):
            for img in wrong_img:
                if img in item[0]:
                    lost_num = idx
                    flag = True
                    break
            if flag:
                break
        if flag:
            print('clean')
            total_dic[qid]['doc_list'] = total_dic[qid]['doc_list'][:lost_num]

def pilot_choose(total_dic):
    find_queries = {0:[],1:[],2:[],3:[],4:[]}
    find_queries_soft = {0:[],1:[],2:[],3:[],4:[]}
    for qid in total_dic.keys():
        if qid in ['82','19','76']:
            continue
        good_ab = []
        bad_ab = []
        for i in range(len(total_dic[qid]['doc_list'])):
            if total_dic[qid]['end_info']['rel'][str(i)] >= 4 and total_dic[qid]['end_info']['nes'][str(i)] >= 1.4:
                good_ab.append(i)
            elif total_dic[qid]['end_info']['rel'][str(i)] <= 2 and total_dic[qid]['end_info']['nes'][str(i)] >= 1.4:
                bad_ab.append(i)
        if len(bad_ab) < 5 and len(good_ab) >= 2:
            find_queries[len(bad_ab)].append(qid)
        elif len(bad_ab) >= 5 and len(good_ab) >= 2:
            find_queries[4].append(qid)
        if len(bad_ab) < 5 and len(good_ab) >= 1:
            find_queries_soft[len(bad_ab)].append(qid)
        elif len(bad_ab) >= 5 and len(good_ab) >= 1:
            find_queries_soft[4].append(qid)  
    for key in find_queries.keys():
        random.shuffle(find_queries[key])
        random.shuffle(find_queries_soft[key])
    for key in find_queries.keys():
        print(key, len(find_queries[key]))

    out_qid = {}   
    out_qid_set = set()
    for i in range(4,-1,-1):
        out_qid[i] = []
        print('select '+str(i), end=',')
        previous_len = len(out_qid_set)
        for num in range(18):
            flag=False
            for j in range(4,-1,-1):
                if j >= i:
                    for item in find_queries[j]:
                        if item not in out_qid_set:
                            out_qid[i].append(item)
                            out_qid_set.add(item)
                            flag = True
                            break
                if flag:
                    break
        for num in range(18 - len(out_qid[i])):
            flag=False
            for j in range(4,-1,-1):
                if j >= i:
                    for item in find_queries_soft[j]:
                        if item not in out_qid_set:
                            out_qid[i].append(item)
                            out_qid_set.add(item)
                            flag = True
                            break
                if flag:
                    break

        print(len(out_qid_set)-previous_len)
    after_qid = []
    fw = open('bad_len.txt','w')
    for bad_len in out_qid.keys():
        for qid in out_qid[bad_len]:
            good_ab = []
            bad_ab = []
            for i in range(len(total_dic[qid]['doc_list'])):
                if total_dic[qid]['end_info']['rel'][str(i)] >= 4 and total_dic[qid]['end_info']['nes'][str(i)] >= 1.4:
                    good_ab.append(i)
                elif total_dic[qid]['end_info']['rel'][str(i)] <= 2 and total_dic[qid]['end_info']['nes'][str(i)] >= 1.4:
                    bad_ab.append(i)
            select_i = []
            tmp_doc_list = []
            random.shuffle(bad_ab)
            random.shuffle(good_ab)
            for i in range(bad_len):
                tmp_doc_list.append(total_dic[qid]['doc_list'][bad_ab[i]])
                select_i.append(bad_ab[i])
            tmp_doc_list.append(total_dic[qid]['doc_list'][good_ab[0]])
            select_i.append(good_ab[0])
            left_i = [i  for i in range(len(total_dic[qid]['doc_list'])) if i not in select_i]
            random.shuffle(left_i)
            for i in range(len(left_i)):
                tmp_doc_list.append(total_dic[qid]['doc_list'][left_i[i]])
            total_dic[qid]['doc_list'] = tmp_doc_list
            total_dic[qid]['bad_len'] = bad_len
            fw.write(str(bad_len))
            fw.write('\n')
            after_qid.append(total_dic[qid])
    fw.close()
    json.dump(list(after_qid), open('../random_data/raw_90.json','w'))


clean(total_dic)
pilot_choose(total_dic)

