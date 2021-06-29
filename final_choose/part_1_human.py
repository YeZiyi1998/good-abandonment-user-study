import json

input_dir_list = ['first_0', 'first_1', 'first_2']

base_path = '../user_data'

random_data_path = '../random_data'

def merge_dic():
    total_dic = {}
    first_json = json.load(open(random_data_path+'/'+'first_0.json'))
    out_json = {}
    for dir_name in input_dir_list:
        with open(base_path + '/' + dir_name + '/' + 'end_info.txt') as f:
            for line in f.readlines():
                line_list = line.strip().split('\t')
                if len(line_list) > 1 and line_list[0] != '-1':
                    qid = line_list[0]
                    end_info = json.loads(line_list[1])
                    total_dic[qid] = end_info

    for idx, item in enumerate(first_json):
        item['end_info'] = total_dic[str(idx+1)]
        out_json[item['id']] = item
        # for key in ['bad_ab_doc_list','good_ab_doc_list','other_doc_list']:
        #     del item[key]
    json.dump(out_json, open('human/human_all.vote.json','w'))

merge_dic()
