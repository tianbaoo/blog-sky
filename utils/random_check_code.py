import random
from PIL import Image,ImageFont,ImageDraw,ImageFilter
"""
图片验证码插件
"""
def rd_check_code(width=100, height=35, char_length=4, font_file='kumo.ttf', font_size=35):
    # width:图片宽度 height:图片高度 char_length:验证码个数 font_file:验证码字体文件路径 font_size:验证码字符大小
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母   
        :return:
        """
        res = [[chr(i) for i in range(ord('0'), ord('9') + 1)],  # 生成0到9
               [chr(i) for i in range(ord('a'), ord('z'))],      # 生成a到z
               [chr(i) for i in range(ord('A'), ord('Z'))]]      # 生成A到Z
        choice1=random.choice(res)
        choice2=random.choice(choice1)
        return choice2

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(10):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(10):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(3):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.DETAIL)  # 滤镜
    return img, ''.join(code)