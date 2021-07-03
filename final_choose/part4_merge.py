import json

dis_select_id = [40, 44, 47, 50, 55, 63, 64, 80]

def get_raw():
    raw_file = json.load(open('../random_data/select_raw.json'))
    lost_after_qid_number = {}
    after_qid = []
    for i in range(4, -1, -1):
        lost_after_qid_number[i] = 18 - len([item for item in raw_file[i * 18: i * 18 + 18] if item['id'] not in dis_select_id])
    for i in range(len(raw_file)):
        if i not in dis_select_id:
            after_qid.append(raw_file[i])
    return raw_file, after_qid, lost_after_qid_number

a1 = json.load(open('../random_data/select_left.json'))
a2 = json.load(open('../random_data/select_raw.json'))
raw_file, after_qid, lost_after_qid_number = get_raw()
json.dump(a2 + a1, open('../random_data/select_90.json', 'w'))


