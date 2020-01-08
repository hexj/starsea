import os


def is_pixel_equal(image1, image2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    pixel1 = image1.load()[x, y]
    pixel2 = image2.load()[x, y]
    threshold = 30
    if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
        return True
    else:
        return False


def get_move_distance(image1, image2):
    """
    基于极验的两张图片的像素点进行比较，计算方块需要移动的距离
    :param image1: 不带缺口图片
    :param image2: 带缺口图片
    :return: 滑动的距离
    """
    distance = 0
    for i in range(distance, image1.size[0]):
        for j in range(image1.size[1]):
            if not is_pixel_equal(image1, image2, i, j):
                distance = i
                return distance
    return distance


def init_data_directory(dir_name):
    """
    创建必要的的路径用来存储一些必要的数据，比如雪球破解登录的时候，本地需要保存两张图片; 还有生成的h5文件。
    :param dir_name:
    :return:
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
