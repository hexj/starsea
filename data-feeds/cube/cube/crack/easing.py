# 各种平滑动作的类，具体可以参考 https://easings.net/
# 以及jquery的实现 https://github.com/gdsmith/jquery.easing/blob/master/jquery.easing.js
import numpy as np


def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_out_quart(x):
    return 1 - pow(1 - x, 4)


def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)


def get_tracks(distance, seconds, ease_func):
    """
    获取移动的路径
    :param obj: 破解类对象
    :param distance: 移动的记录
    :param seconds: 需要的时间
    :param ease_func: 平滑函数的名字，通过这个名字在obj对象中，通过getattr方法获取到方法，并且执行
    :return: 路径的数组
    """
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = globals()[ease_func]
        offset = round(ease(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return tracks
