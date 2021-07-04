import pandas as pd
import json

user_id = 2
random_file = json.load(open('../random_data/'+str(user_id)+'.json'))

end_info = {}
with open(str(user_id)+'/end_info.txt','r',encoding='gbk') as f:
    for line in f.readlines():
        line_list = line.split('\t')
        if line_list[0] != '-1' and len(line_list) >= 2:
            end_info[line_list[0]] = json.loads(line_list[1])

for idx, item in enumerate(random_file):
    if str(idx) in end_info.keys():
        item['end_info'] = end_info[str(idx)]
    else:
        item['end_info'] = {}

json.dump(random_file, open(str(user_id)+'/end_info.merged.json','w'))







