
import base64
import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont  # pip install pillow


def image_code():
    # 通过数字获取ascii表中的对应数字，大写字母，小写字母
    def get_char():
        """
        a-z：97-122

        A-Z：65-90

        0-9：48-57
        :return:
        """
        # return chr(random.choice([random.randint(48,57),random.randint(65,90),random.randint(97,122)]))
        return chr(random.choice([random.randint(48, 57)]))

    # 获取随机颜色
    def get_color(*args):
        if args == ():
            tuple_data = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            return tuple_data
        while True:
            text_color = get_color()
            aberration = 3 * (text_color[0] - args[0][0]) ** 2 + 4 * (text_color[0] - args[0][1]) ** 2 + 2 * (
                    text_color[0] - args[0][2]) ** 2
            # 设置字体颜色与背景色差，值越大，字体越清晰，机器人就更容易识别，相对应的代价就是需要随机更多次的RGB值。
            # 极端情况验证码字体背景rgb均为128，aberration最小的最大值为147456
            rgb2 = 100000
            if aberration > rgb2:
                return text_color

    # 创建图片对象
    img_back = get_color()
    image = Image.new(mode='RGB', size=(120, 50), color=(255, 255, 255))
    # 创建画笔对象
    draw = ImageDraw.Draw(image, mode='RGB')
    # 噪点 xy：基于图片的坐标，fill表示点颜色
    for i in range(50):
        draw.point([random.randint(0, 120), random.randint(0, 50)], fill=get_color())

    # 噪线 xy:(起点坐标，终点坐标) fill：颜色  width：线宽
    # draw.line((50, 30, 100, 60),fill='purple', width=5)
    for i in range(5):
        draw.line([random.randint(0, 120), random.randint(0, 50), random.randint(0, 120), random.randint(0, 50)],
                  fill=get_color())
    # 划圆或弧线
    for i in range(5):
        x = random.randint(0, 120)
        y = random.randint(0, 50)
        x2 = x + 4
        y2 = y + 4

        draw.arc((x, y, x2, y2), 0, 90, fill=get_color())

    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/fz_font.TTF"))
    font = ImageFont.truetype(font_path, 30)

    # 用来拼接验证码字符的
    char_list = []
    for i in range(4):
        char = get_char()
        char_list.append(char)
        height = random.randint(10, 15)
        draw.text([18 * (i + 1), height], char, get_color(img_back), font=font)

    char_code_a = ''.join(char_list)

    # 模糊效果和边缘增强效果
    # img = img.filter(ImageFilter.BLUR)
    # img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # img.save('../static/test.png')

    return image, char_code_a


def img_base64_encode():
    image, char_codes = image_code()
    output_buffers = BytesIO()
    image.save(output_buffers, format='PNG')
    byte_data_a = output_buffers.getvalue()
    base64_str_a = str(base64.b64encode(byte_data_a), 'utf-8')
    return base64_str_a, char_codes


if __name__ == '__main__':
    img, char_code = image_code()
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = str(base64.b64encode(byte_data), 'utf-8')
    # print(base64.b64encode(byte_data))
    print(base64_str)
    # print(image_code())
