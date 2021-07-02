import json
import random
random.seed(2021)
manual_90 = json.load(open('../../random_data/manual_90.json'))
for i in range(32):
    random.shuffle(manual_90)
    json.dump(manual_90, open('../../random_data/'+str(i)+'.json', 'w'))








