from my_utils import *
from trigger_test import send_trigger
from psychopy import core, gui, visual, event
from datetime import datetime
import random
import sys


def pilot_study1(win, test_id, stu_list, n = 12):
    timer = core.Clock()
    stu_list_all = split_arr(stu_list, n)
    info = []
    text_ui = visual.TextStim(win, text = '', pos=(-TEXT_LEFT, 0), height = WORD_HEIGHT, color = (1,1,1), alignText='left')

    if test_id != 0:
        instruction_rest = visual.TextStim(win, text = '实验一阶段' + str(test_id) + '.休息,按下空格继续实验', pos=(-TEXT_LEFT, TEXT_HEIGHT), height = WORD_HEIGHT, color = (1,1,1), alignText='left')
        instruction_rest.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        core.wait(1.0)

    for idx, stu_list in enumerate(stu_list_all):   
        query_string = split_text(str(idx+1) + '.' + stu_list['query'])
        text_ui.setText(query_string)
        text_ui.draw()
        win.flip()
        send_trigger(100)
        for stu in stu_list['doc_list']:
            print(stu)
        

    return info
