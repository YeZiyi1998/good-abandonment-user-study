from os import TMP_MAX
from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponse, HttpResponseRedirect, Http404
from .models import QueryModel
from .trigger_test import send_trigger, trigger_dic, chinese_trigger_dic

# 数据集和结果保存路径
IMG_PATH = 'query/mobile_data/'
SAVE_PATH = 'query/results/'
MOD = 1007

model = QueryModel()

# homepage
def homepage(request):
    if request.POST.get('user_name'):
        user_id = str(request.POST['user_id'])
        user_name = request.POST['user_name']
        if model.has_user(user_id):
            return HttpResponseRedirect(reverse('query:questions', args=(model.get_user_ques_id(user_id), user_name, user_id)))
        else:
            model.add_new_user(user_id, user_name)
            return HttpResponseRedirect(reverse('query:questions', args=(0, user_name, user_id)))
    else:
        return render(request, 'query/homepage.html')

# process function
def process_question_post(request, question_id, user_name, user_id):
    print('question_id', question_id)
    
    if request.POST.get('endinfo') != None:
        end_info = request.POST.get('endinfo')
        model.add_info(user_id, question_id, end_info)
        print("end_info", end_info)
    else:
        print("not end_info")
    
    if question_id == model.get_question_numbers(user_id):
        return None

    # 返回下一个问题的名字，图片文件名，图片描述 
    query = model.get_question(user_id, question_id)
    content = {
        'query': query,
        'question_id': question_id + 1,
        'user_name': user_name,
        'user_id': user_id,
    }
    img_list = []
    for tmp_doc_id in range(0, model.get_question_len(user_id, question_id)):
        tmp_img = model.get_question_doc(user_id, question_id, tmp_doc_id)
        img_list.append(IMG_PATH + tmp_img)
    content['img_list'] = img_list
    return content

def questions(request, question_id, user_name, user_id):
    if not model.has_user(user_id):
        raise Http404("User does not exist!")
    if (question_id < 0 or question_id > model.get_question_numbers(user_id)) and question_id < MOD / 2:
        raise Http404("Question does not exist!")

    content = process_question_post(request, question_id, user_name, user_id)
    if content == None:
        return HttpResponseRedirect(reverse('query:thanks'))
    else:
        return render(request, 'query/end.html', content)

# final page
def thanks(request):
    return render(request, 'query/thanks.html', {})

