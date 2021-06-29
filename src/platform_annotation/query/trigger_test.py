import time
trigger_dic = {
    'query_id_show' : 'qid',
    'doc_id_show': 'did',
    'click' : 5,
    'abandon': 6,
    'end': 7,
    'start': 9,
    'back': 8
}
chinese_trigger_dic = {
    '结束搜索':7,
    '下一个结果':6,
    '进入结果页':5,
    '返回': 8,
}

def send_trigger(code):
    print("send trigger", code)

def test():
    t = range(1,200)
    for i in range(1000):
        send_trigger(t[i%200])
        time.sleep(0.5)

if __name__ == '__main__':
    test()