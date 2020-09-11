#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2018-06-12 21:23
# @desc   : 使用pillow模块实例

from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random


def handle_image(path):
    im = Image.open(path)
    # 获取图片尺寸
    (w, h) = im.size
    print("图片尺寸：%sx%s" % (w, h))
    # 缩放图片
    im.thumbnail((w/2, h/2))
    # 应用模糊滤镜
    im = im.filter(ImageFilter.BLUR)
    # 保存新的图片
    im.save('C:\\Users\\Administrator\\Desktop\\new.jpg', 'jpeg')


def rnd_char():
    """随机生成大小写字母或数字"""
    map = {
        1: chr(random.randint(65, 90)),
        2: chr(random.randint(48, 57)),
        3: chr(random.randint(97, 122))
    }
    return map[random.randint(1, 3)]


def rnd_color():
    """随机生成颜色(0~255之间的三色组成),用来填充背景像素"""
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)


# 随机颜色2:
def rnd_color2():
    """随机生成颜色(0~255之间的三色组成),用来填充字符"""
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


def verify_code(path):
    # size:240 x 60:
    w = 60 * 4
    h = 60
    image = Image.new('RGB', (w, h), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(w):
        for y in range(h):
            draw.point((x, y), fill=rnd_color())
    # 输出文字:
    for t in range(4):
        draw.text((60 * t + 10, 10), rnd_char(), font=font, fill=rnd_color2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save('C:\\Users\\Administrator\\Desktop\\code.jpg', 'jpeg')


if __name__ == '__main__':
    # HANDLE_IMAGE, GEN_VERIFY_CODE
    main = 'GEN_VERIFY_CODE'
    path = "C:\\Users\\Administrator\\Desktop\\IMG_7375.JPG"

    exe = dict(HANDLE_IMAGE=handle_image, GEN_VERIFY_CODE=verify_code)

    exe[main].__call__(path)
