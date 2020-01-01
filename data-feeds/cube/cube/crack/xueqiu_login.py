import time
from io import BytesIO
from PIL import Image
import base64
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import numpy as np
import os

from cube.config.cube_settings import *

BORDER = 6
INIT_LEFT = 60
TEMP_DATA = 'tmp_data'
DB_DATA = 'db_data'


class CrackXueQiu(object):
    def __init__(self):
        CrackXueQiu.init_data_directory(TEMP_DATA)
        CrackXueQiu.init_data_directory(DB_DATA)

        self.url = 'https://xueqiu.com'
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--start-maximized')
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
        self.max_retry_cnt = 3
        self.retried_cnt = 0

    @staticmethod
    def init_data_directory(dir_name):
        """
        创建必要的的路径用来存储一些必要的数据，比如雪球破解登录的时候，本地需要保存两张图片; 还有生成的h5文件。
        :param dir_name:
        :return:
        """
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    '''
    浏览器打开网址，并且填入账号密码，然后点击登录按钮，出现图形验证码
    '''

    def prepare_for_login(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        login_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Header_nav__login__btn_1YU')))
        login_btn.click()
        user_name = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password = self.wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        user_name.send_keys(XUEQIU_ACCT)
        password.send_keys(XUEQIU_PASSWD)
        real_login_btn = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'Loginmodal_modal__login__btn_uk7')))
        real_login_btn.click()

    '''
    导出canvas到png图片中
    '''

    def save_captcha_img(self, img_name, class_name):
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.browser.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

    '''
    基于极验的两张图片，计算两张图片该移动的距离
    :param image1: 不带缺口图片
    :param image2: 带缺口图片
    '''

    def get_move_distance(self, image1, image2):
        left = 0
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """

    def is_pixel_equal(self, image1, image2, x, y):
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 30
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    """
    根据偏移量获取移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """

    def get_track(self, distance):
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 3 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        # 矫正最后一个长度，如果current > 超过 distance，则需要最后一个数组减掉多滑的距离，
        # 否则需要加上少滑动的距离。
        total_distance = np.sum(track)
        print(total_distance)
        print(track)
        track[len(track) - 1] -= (total_distance - distance)
        print(track)
        return track

    import math
    def ease_out_quad(self, x):
        return 1 - (1 - x) * (1 - x)

    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    def ease_out_expo(self, x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    def get_tracks(self, distance, seconds, ease_func):
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            ease = getattr(self, ease_func)
            offset = round(ease(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        return offsets, tracks

    """
    拖动滑块到缺口处
    :param slider: 滑块
    :param track: 轨迹
    :return:
    """
    import time;
    def start_to_move(self, track):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            print(f'-----------------------> time start at {time.asctime(time.localtime(time.time()))}')
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            print(f'-----------------------> time end at {time.asctime(time.localtime(time.time()))}')
        ActionChains(self.browser).release().perform()

    def crack(self, reset_status=True):
        # 访问网站并且输入用户名和密码，然后点击验证码按钮
        if reset_status:
            self.prepare_for_login()
        # 保存图片
        # image1 = self.get_geetest_image()
        self.save_captcha_img('tmp_data/captcha1.png', 'geetest_canvas_fullbg')
        self.save_captcha_img('tmp_data/captcha2.png', 'geetest_canvas_bg')

        # 计算移动距离
        img1 = Image.open('tmp_data/captcha1.png')
        img2 = Image.open('tmp_data/captcha2.png')
        move_distance = self.get_move_distance(img1, img2)
        # print('need move move_distance:' + str(move_distance))

        move_distance -= BORDER
        print(f'------------------------------->{str(move_distance)}')
        # 获取轨迹
        # track = self.get_track(move_distance)
        offset, track = self.get_tracks(move_distance, 3, 'ease_out_quad')
        print('-------------------------------->' + str(track))
        # 开始移动
        self.start_to_move(track)

        ## geetest_fail,geetest_success
        try:
            WebDriverWait(self.browser, 5, 0.2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'geetest_success')))

        except TimeoutException:
            print("验证失败")

            try:
                btn_error_and_retry = WebDriverWait(self.browser, 1, 0.2).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_panel_error_content')))
                btn_error_and_retry.click()
            except:
                print('没有出现超时错误，忽略')

            # 失败之后，继续第二次校验，最多校验3次
            if self.retried_cnt < self.max_retry_cnt:
                self.crack(True)
                self.retried_cnt += 1
            else:
                return False
        else:
            print("验证成功")
            time.sleep(3)
            self.retried_cnt = 0
            # 登录成功之后，写入到cookie到本地文件
            cookie = self.browser.get_cookies()
            import json
            jsonCookies = json.dumps(cookie)
            with open('tmp_data/xueqiu_cookie.json', 'w') as f:
                print(f'将cookies写入到文件: {jsonCookies}')
                f.write(jsonCookies)
                f.close()
            self.browser.quit()
            return True


if __name__ == '__main__':
    crack = CrackXueqiu()
    # crack.crack()