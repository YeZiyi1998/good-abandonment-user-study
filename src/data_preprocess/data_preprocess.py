import random
import os
import json
import numpy as np

def get_query_info():
    query_dic = {}
    with open('../../mobile_data/query.txt', encoding="utf8") as f:
        for idx, line in enumerate(f.readlines()):
            query_dic[idx] = line
    return query_dic, idx + 1

def generate_file(out_file):
    global query_dic
    global query_num
    info_json = []
    query_id_list = [i for i in range(0, query_num)]
    random.shuffle(query_id_list)
    for id_num in query_id_list:
        tmp_info = {'id': id_num, 'query': query_dic[id_num].strip()}
        select_num = []
        for i in range(20):
            png_name = str(id_num)+'_'+str(i)+'.png'
            if os.path.exists('../../mobile_data/'+'crop/'+png_name) and os.path.exists('../../mobile_data/'+'landing_page/'+png_name):
                select_num.append(['crop/'+png_name, 'landing_page/'+png_name])
            if len(select_num) == 10:
                break
        random.shuffle(select_num)
        tmp_info['doc_list'] = select_num
        info_json.append(tmp_info)
    print("average doc num: ", np.mean([len(item['doc_list']) for item in info_json]))
    with open('tmp.txt','w', encoding="utf8") as fw:
        fw.write(str([item['id'] for item in info_json if len(item['doc_list']) < 10]))
    print([len(item['doc_list']) for item in info_json])
    info_json = [item for item in info_json if len(item['doc_list']) >= 6]
    json.dump(info_json, open(out_file, 'w'))

out_path = '../../random_data/'
query_dic, query_num = get_query_info()
for i in range(0, 33):
    random.seed(i)
    generate_file(out_path + str(i) + '.json')

