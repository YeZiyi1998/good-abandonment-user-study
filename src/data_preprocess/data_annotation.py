import random
import os
import json
import numpy as np

def get_query_info():
    query_dic = {}
    with open('../platform_annotation/query/static/query/mobile_data/query.txt', encoding="utf8") as f:
        for idx, line in enumerate(f.readlines()):
            query_dic[idx] = line
    return query_dic, idx + 1

def generate_file(out_file):
    global query_dic
    global query_num
    global dis_select_list
    info_json = []
    query_id_list = [i for i in range(0, query_num) if i not in dis_select_list]
    for id_num in query_id_list:
        tmp_info = {'id': id_num, 'query': query_dic[id_num].strip()}
        select_num = []
        for i in range(20):
            png_name = str(id_num)+'_'+str(i)+'.png'
            if os.path.exists('../platform_annotation/query/static/query/mobile_data/'+'crop/'+png_name) and os.path.exists('../platform_annotation/query/static/query/mobile_data/'+'landing_page/'+png_name):
                select_num.append(['crop/'+png_name, 'landing_page/'+png_name, i])
            elif i == 0 and os.path.exists('../platform_annotation/query/static/query/mobile_data/'+'crop/'+png_name):
                select_num.append(['crop/'+png_name, '', i])
            if len(select_num) == 15:
                break
        tmp_info['doc_list'] = select_num
        info_json.append(tmp_info)
    with open('tmp.txt','w', encoding="utf8") as fw:
        fw.write(str([item['id'] for item in info_json if len(item['doc_list']) < 10]))
    print([len(item['doc_list']) for item in info_json])
    info_json = [item for item in info_json if len(item['doc_list']) >= 6]
    json.dump(info_json, open(out_file, 'w'))

out_path = '../../random_data/'
query_dic, query_num = get_query_info()
dis_select_list = []
with open('dis_select.txt') as f:
    for line in f.readlines():
        dis_select_list.append(int(line.strip()))

for i in range(2, 3):
    generate_file(out_path + 'first_' + str(i) + '.json')
