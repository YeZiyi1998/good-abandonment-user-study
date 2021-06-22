from os import TMP_MAX
from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponse, HttpResponseRedirect, Http404
from .models import QueryModel
from .trigger_test import send_trigger, trigger_dic, chinese_trigger_dic
import time

# 数据集和结果保存路径
IMG_PATH = 'query/mobile_data/'
SAVE_PATH = 'query/results/'
MOD = 1007
REST_PERIOD = 15

model = QueryModel()

# homepage
def homepage(request):
    if request.POST.get('user_name'):
        user_id = str(request.POST['user_id'])
        user_name = request.POST['user_name']
        model.add_new_user(user_id)
        return HttpResponseRedirect(reverse('query:questions', args=(-1 + MOD, 15, user_name, user_id)))
    else:
        return render(request, 'query/homepage.html')

# process function
def process_question_post(request, question_id, doc_id, user_name, user_id):
    # grade为标注类别，1~8
    if question_id == MOD - 1:
        question_id = -1
    ans = trigger_dic['start']
    if request.POST.get('grade') != None:
        ans = request.POST.get('grade')
        if ans in chinese_trigger_dic.keys():
            ans = chinese_trigger_dic[ans]
        else:
            ans = int(ans)
    if question_id == model.get_question_numbers(user_id):
        return None
    
    rest = False
    if ans == trigger_dic['start']:
        question_id = question_id + 1
        doc_id = 15
        # 每15个问题休息
        if question_id % REST_PERIOD == 0 and question_id != 0:
            rest = True
    elif ans == trigger_dic['resume']:  # 从休息页面返回
        question_id = question_id
        doc_id = 15
    elif ans == trigger_dic['click'] or ans == trigger_dic['back']:
        question_id = question_id 
        doc_id = doc_id
    elif ans == trigger_dic['abandon']:
        question_id = question_id
        doc_id = (doc_id + 1) % 16  
    elif ans == trigger_dic['end']:
        question_id = question_id
        doc_id = doc_id

    print('question_id')
    time.sleep(0.1)
    send_trigger(question_id+50)
    print('doc_id')
    time.sleep(0.1)
    send_trigger(doc_id+10)
    
    model.add_action(user_id, {"quesion_id":question_id,"doc_id":doc_id,"ans":ans,"time_stamp":time.time()})
    
    if question_id == model.get_question_numbers(user_id):
        print("ans")
        time.sleep(0.1)
        send_trigger(ans)
        return None, question_id, doc_id

    if request.POST.get('endinfo') != None:
        end_info = request.POST.get('endinfo')
        model.add_info(user_id, question_id, end_info)
        print("end_info", end_info)

    # 返回下一个问题的名字，图片文件名，图片描述 
    query, img1 = model.get_question(user_id, question_id, doc_id)
    content = {
        'query': query,
        'img1': IMG_PATH,
        'ans': ans,
        'question_id': question_id,
        'user_name': user_name,
        'user_id': user_id,
        'doc_id': doc_id,
        'show_abandon': 1,
        'show_cross': 1,
        'rest': rest
    }
    if doc_id == model.get_question_len(user_id, question_id) - 1:
        content['show_abandon'] = 0
    if ans == trigger_dic['back']:
        content['show_cross'] = 0
    if ans == trigger_dic['click']:
        img1 = model.get_doc(user_id, question_id, doc_id)
    elif ans == trigger_dic['end']:
        img_list = []
        for tmp_doc_id in range(0, min(doc_id + 1, model.get_question_len(user_id, question_id))):
            tmp_query, tmp_img = model.get_question(user_id, question_id, tmp_doc_id)
            img_list.append(IMG_PATH + tmp_img)
        content['img_list'] = img_list
    if img1 != None:
        content['img1'] += img1
    print("ans ", ans)
    time.sleep(0.1)
    send_trigger(ans)
    return content, question_id, doc_id

def questions(request, question_id, doc_id, user_name, user_id):
    if not model.has_user(user_id):
        raise Http404("User does not exist!")
    if (question_id < 0 or question_id > model.get_question_numbers(user_id)) and question_id < MOD / 2:
        raise Http404("Question does not exist!")

    content, question_id, doc_id = process_question_post(request, question_id, doc_id, user_name, user_id)
    if content == None:
        model.add_info(user_id, -1, str(model.user_data[user_id]['action_list']))
        return HttpResponseRedirect(reverse('query:thanks'))
    elif content['rest']:
        return render(request, 'query/rest.html', content)
    elif content['ans'] == trigger_dic['start'] or content['ans'] == trigger_dic['resume']:
        return render(request, 'query/start.html', content)
    elif content['ans'] == trigger_dic['click']:
        return render(request, 'query/item.html', content)
    elif content['ans'] == trigger_dic['end']:
        return render(request, 'query/end.html', content)
    elif content['ans'] == trigger_dic['abandon'] or content['ans'] == trigger_dic['back']:
        return render(request, 'query/crop.html', content)
    raise Http404("ERROR!")

# final page
def thanks(request):
    return render(request, 'query/thanks.html', {})


# save audio
def save_audio(request):
    print(request)
    return HttpResponse('上传成功！')
