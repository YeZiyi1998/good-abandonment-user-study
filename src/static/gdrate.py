import json
import demjson
user_name_list = list(range(0,8))
user_name_list = [str(item) for item in user_name_list]
# user_name_list.append('pilot')
# user_name_list.append('pilot2')


def load_end_info(user_name):
    q2end_info = {}
    with open('../../user_data/'+str(user_name)+'/end_info.txt', encoding='gbk') as f:
        for line in f.readlines():
            line_list = line.split('\t')
            if line_list[0] != '-1' and len(line_list) > 1:
                if 'pilot' in user_name:
                    q2end_info[int(line_list[0])-1] = json.loads(line_list[1])
                else:
                    q2end_info[int(line_list[0])] = json.loads(line_list[1])
    return q2end_info 

def add2dic(q_d_info, q, d, k, v):
    if q not in q_d_info.keys():
        q_d_info[q] = {}
    if d not in q_d_info[q].keys():
        q_d_info[q][d] = {}
    q_d_info[q][d][k] = v

# 有一些重合的去重 如果重合了返回true（二者除了time stamp都一样）
def compare(a,b):
    for key in a:
        if key != 'time_stamp':
            if a[key] != b[key]:
                return False
    return True

q_d_info = {}
double_rate = 0
for user_name in user_name_list:
    end_info = load_end_info(user_name)
    action_list = []
    print(user_name)
    with open('../../user_data/'+str(user_name)+'/action.txt', encoding='gbk') as f:
        for line in f.readlines():
            action_list.append(demjson.decode(line))
    for idx, action in enumerate(action_list[ : -1]):
        next_action = action_list[idx + 1]
        if action['ans'] == 6:
            if compare(action, next_action):
                double_rate += 1
                continue
            qid = action['quesion_id']
            did = action['doc_id']
            if next_action['ans'] == 5: # click
                if end_info[qid][str(did)] >= 4:
                    add2dic(q_d_info, qid, did, user_name, 'good click')
                elif end_info[qid][str(did)] <= 2 and end_info[qid][str(did)] >= 1:
                    add2dic(q_d_info, qid, did, user_name, 'bad click')
            else: # abandonment  
                if end_info[qid][str(did)] >= 4:
                    add2dic(q_d_info, qid, did, user_name, 'good abandonment')
                elif end_info[qid][str(did)] <= 2 and end_info[qid][str(did)] >= 1:
                    add2dic(q_d_info, qid, did, user_name, 'bad abandonment')

for user_name in user_name_list:
    total_dic = {'good click':0, 'bad click': 0, 'good abandonment': 0, 'bad abandonment': 0}
    for q in q_d_info.keys():
        for d in q_d_info[q].keys():
            if user_name in q_d_info[q][d].keys():
                total_dic[q_d_info[q][d][user_name]] += 1
    # print(user_name, ' ', total_dic)
    print(';'.join([str(v) for v in list(total_dic.values())]))

total_dic = {'good click':0, 'bad click': 0, 'good abandonment': 0, 'bad abandonment': 0}
for user_name in user_name_list:
    for q in q_d_info.keys():
        for d in q_d_info[q].keys():
            if user_name in q_d_info[q][d].keys():
                total_dic[q_d_info[q][d][user_name]] += 1
print('total', ' ', total_dic)
print(';'.join([str(v) for v in list(total_dic.values())]))
print('double rate', double_rate)

