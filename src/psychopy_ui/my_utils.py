FIRST_KEY = 'f'
NEXT_KEY = 'j'
BASE_IMG_PATH = '../../data/images_ziyi/'
HIGHT = 1080
WIDE = 1920
WIN_SIZE = [WIDE, HIGHT]
TEXT_LEFT = WIDE / 10
TEXT_HEIGHT = HIGHT / 10
WORD_HEIGHT = WIDE / 15
TWO_IMAGE_TEXT_HIGHT = HIGHT / 4
POS_LISt = [
    [-350, -210], [-100, -210], [150, -210], [-350, 10], [-100, 10], [150, 10]
]


def split_arr(stu_list, n):
    split_list = []
    for i in range(0, len(stu_list), n):
        split_list.append(stu_list[i:i+n])
    return split_list

def split_text(input_text):
    output_text = ''
    line_length = 15
    while(len(input_text)>line_length):
        output_text += input_text[:line_length] + '\n'
        input_text= input_text[line_length:]
    output_text += input_text
    return output_text