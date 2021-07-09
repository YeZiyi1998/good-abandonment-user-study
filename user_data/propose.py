import pandas as pd
import json
import demjson

user_id_list = ['0','1','2','3','4','5','6','7','8','pilot','pilot2']
for user_id in user_id_list:
    random_file = json.load(open('../random_data/'+str(user_id)+'.json'))

    end_info = {}
    with open(str(user_id)+'/end_info.txt','r',encoding='gbk') as f:
        for line in f.readlines():
            line_list = line.split('\t')
            if line_list[0] != '-1' and len(line_list) > 1:
                if 'pilot' in str(user_id):
                    end_info[str(int(line_list[0])-1)] = json.loads(line_list[1])
                else:
                    end_info[str(line_list[0])] = json.loads(line_list[1])

    action = {}
    with open(str(user_id)+'/action.txt','r',encoding='gbk') as f:
        lines = list(f.readlines())
        for idx, line in enumerate(lines[:-1]):
            next_action = demjson.decode(lines[idx + 1])
            tmp_action = demjson.decode(line)
            if tmp_action['ans'] != 6:
                continue
            if tmp_action['quesion_id'] not in action.keys():
                action[tmp_action['quesion_id']] = {}
            action[tmp_action['quesion_id']][tmp_action['doc_id']] = float(next_action['time_stamp']) - float(tmp_action['time_stamp']) - 1.5

    for idx, item in enumerate(random_file):
        if str(idx) in end_info.keys():
            item['end_info'] = end_info[str(idx)]
            item['end_info']['time_stamp'] = action[int(idx)]
        else:
            item['end_info'] = {}

    json.dump(random_file, open(str(user_id)+'/end_info.merged.json','w'))



