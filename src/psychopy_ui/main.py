from pilot_study import *
import json

def main_fucntion(total_arr, fw):
    # basic unit
    win = visual.Window(WIN_SIZE, fullscr = False, allowGUI =True, units = "pix", color = (-1,-1,-1))
    # win = visual.Window(MIN_SIZE, fullscr = True, allowGUI =True, units = "pix", color = (-1,-1,-1))

    instruction_start = visual.TextStim(win, text = '请仔细阅读实验说明, 按下空格开始实验训练', pos=(-TEXT_LEFT, TEXT_HEIGHT), height = WORD_HEIGHT,color = (1,1,1), alignText='center')
    instruction_end = visual.TextStim(win, text = '实验结束,请联系主试', pos=(-TEXT_LEFT, TEXT_HEIGHT), height = WORD_HEIGHT,color = (1,1,1), alignText='left')
    instruction_test = visual.TextStim(win, text = '按空格键，开始正式实验', pos=(-TEXT_LEFT, TEXT_HEIGHT), height = WORD_HEIGHT,color = (1,1,1), alignText='left')
    
    # instruction
    instruction_start.draw()
    win.flip()         
    event.waitKeys(keyList=['space'])
    core.wait(1.0)  

    # pilot_study1 training
    pilot_study1(win, total_arr[:2])
    instruction_test.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    core.wait(1.0) 

    # pilot_study1 main study
    info1 = pilot_study1(win, total_arr[2:])
    fw.write(str(info1) + '\t')

    # end
    instruction_end.draw()
    win.flip()         
    event.waitKeys(keyList=['space'])

def load_random_info(uid):
    with open('../../random_data/' + str(uid) + '.json', encoding='UTF-8') as f:
        return json.load(f)

if __name__ == '__main__':
    uid = int(sys.argv[1])
    total_arr = load_random_info(uid)
    main_fucntion(total_arr, open('../../user_data/' + str(uid) + '.txt', 'w'))

