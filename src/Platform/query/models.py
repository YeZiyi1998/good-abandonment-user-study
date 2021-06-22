from django.db import models
import random
import os
import json


class QueryModel:
    '''
    '''
    def __init__(self, ):
        self.user_data = {}

    def query_len(self, user_id):
        return len(self.user_data[user_id]['questions'])

    # 判断用户是否已存在
    def has_user(self, user_id):
        return self.user_data.get(user_id, None) != None

    # 返回已存在用户当前的问题序号
    def get_user_ques_id(self, user_id):
        return self.user_data[user_id]['curr_id']

    # 添加新用户，问卷结果初始值为-1，表示该问题未被回答
    def add_new_user(self, user_id):
        self.user_data[user_id] = {}
        self.user_data[user_id]['end_info'] = {}
        self.user_data[user_id]['curr_id'] = 0
        self.user_data[user_id]['action_list'] = []
        with open('../../random_data/' + str(user_id) + '.json', encoding='UTF-8') as f:
            self.user_data[user_id]['questions'] =  json.load(f)
    
    def add_action(self, user_id, action):
        self.user_data[user_id]['action_list'].append(action)
        with open('../../user_data/'+str(user_id)+'/action.txt','a') as f:
            f.write(str(action))
            f.write('\n')

    def add_info(self, user_id, question_id, end_info):
        self.user_data[user_id][question_id] = end_info
        with open('../../user_data/'+str(user_id)+'/end_info.txt','a') as f:
            f.write(str(question_id)+'\t'+end_info)
            f.write('\n')

    def get_question(self, user_id, question_id, doc_id):
        self.user_data[user_id]['curr_id'] = question_id
        if doc_id >= 0 and doc_id < len(self.user_data[user_id]['questions'][question_id]['doc_list']):
            return self.user_data[user_id]['questions'][question_id]['query'], self.user_data[user_id]['questions'][question_id]['doc_list'][doc_id][0]
        else:
            return self.user_data[user_id]['questions'][question_id]['query'], None

    def get_question_len(self, user_id, question_id):
        return len(self.user_data[user_id]['questions'][question_id]['doc_list'])

    def get_question_numbers(self, user_id,):
        return len(self.user_data[user_id]['questions'])

    def get_doc(self, user_id, question_id, doc_id):
        return self.user_data[user_id]['questions'][question_id]['doc_list'][doc_id][1]


# unit test
if __name__ == '__main__':
    m = QueryModel()
