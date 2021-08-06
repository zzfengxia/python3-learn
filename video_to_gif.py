#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2021-07-23 10:28
# @desc   : 视频处理，转gif等

import moviepy.editor as mpy
import imageio
import cv2 as cv

"""
moviepy文档：https://doc.moviepy.com.cn/index.html#document-index
"""


def to_gif_with_moviepy(v_file, out_file):
    clip = mpy.VideoFileClip(v_file)

    # 截取视频，时长：分、秒
    # content = clip.subclip((0, 5), (0, 30))
    clip.write_gif(out_file, fps=3)


def to_gif_with_imageio(v_file, out_file):
    cap = cv.VideoCapture(v_file)
    gif = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        gif.append(frame)
    imageio.mimsave(out_file, gif, 'GIF', duration=0.1)


if __name__ == '__main__':
    path = "C:\\Users\\Administrator\\Desktop\\pic"
    to_gif_with_moviepy(f'{path}\\dog.mp4', f'{path}\\dog.gif')
