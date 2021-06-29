import json

def load_end_info(file_name):
    line_id2end_info = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split('\t')
            if line_list[0] != '-1' and len(line_list) > 1:
                line_id2end_info[line_list[0]] = json.loads(line_list[1])
    return line_id2end_info

user_name2user_id = {}
user_id2info = {}
for id_num in range(18):
    if int(id_num / 2) not in user_name2user_id.keys():
        user_name2user_id[int(id_num / 2)] = []
    user_name2user_id[int(id_num / 2)].append(id_num)

    user_id = 'id_' + str(id_num)
    tmp_simulation = json.load(open('id/' + user_id + '.json'))
    tmp_end_info = load_end_info('id/'+ user_id + '/end_info.txt')
    for idx, item in enumerate(tmp_simulation):
        item['end_info'] = tmp_end_info[str(idx+1)]
    user_id2info[id_num] = tmp_simulation

with open('id/id_all.json', 'w') as f:
    f.write(json.dumps(user_name2user_id))
    f.write('\n')
    f.write(json.dumps(user_id2info))




