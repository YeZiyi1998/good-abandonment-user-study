import json
# pilot = json.load(open('pilot.json'))
# with open('pilot.tsv','w') as f:
#     for item in pilot:
#         del item['doc_list']
#         f.write(str(item))
#         f.write('\n')
# pilot2 = json.load(open('pilot2.json'))
# pilot2_ids = []
# with open('pilot2.tsv','w') as f:
#     for item in pilot2:
#         del item['doc_list']
#         f.write(str(item))
#         f.write('\n')
#         pilot2_ids.append(item['id'])

# pilot3 = json.load(open('pilot3.json'))
# first_0 = json.load(open('../random_data/first_0.json'))
# with open('pilot3.tsv','w') as f:
#     for item in pilot3:
#         del item['doc_list']
#         if item['id'] not in pilot2_ids:
#             f.write(str(item))
#             f.write('\n')


# sessions = {'bad':0, 'good': 0}
# for file in ['pilot', 'pilot2']:
#     with open(file + '/' + 'end_info.txt', encoding='gbk') as f:
#         for line in f.readlines():
#             line_list = line.strip().split('\t')
#             if len(line_list) >= 2 and line_list[0] != '-1':
#                 if json.loads(line_list[1])['total'] <= 4:
#                     sessions['bad'] += 1
#                 else:
#                     sessions['good'] += 1

# print(sessions)
# out_json = []    
# with open('pilot2.tsv') as f:
#     for line in f.readlines():
#         tmp_id = demjson.decode(line)['id']
#         for item in  pilot3:
#             if item['id'] == tmp_id:
#                 out_json.append(item)
#                 break
# json.dump(out_json, open('id_all.json','w'))


id_all = json.load(open('id_all.json'))


for i in range(18):
    tmp_i = i % 6
    tmp_id = id_all[tmp_i*15:tmp_i*15+15]
    json.dump(tmp_id, open('../random_data/id_'+str(i)+'.json','w'))
