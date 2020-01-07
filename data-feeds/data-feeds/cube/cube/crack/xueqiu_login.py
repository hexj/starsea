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

from cube.config.cube_settings import *
from cube.crack.crack_helper import *
from cube.crack.easing import *

BORDER = 6
INIT_LEFT = 60
TEMP_DATA = 'tmp_data'
DB_DATA = 'db_data'


class CrackXueQiu(object):
    def __init__(self):
        init_data_directory(TEMP_DATA)
        init_data_directory(DB_DATA)

        self.url = 'https://xueqiu.com'
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
        self.max_retry_cnt = 3
        self.retried_cnt = 0

    def prepare_for_login(self):
        """
        浏览器打开网址，并且填入账号密码，然后点击登录按钮，出现图形验证码
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

    def save_captcha_img(self, img_name, class_name):
        """
        导出canvas到png图片中, 并且保存到本地文件夹
        :param img_name: 图片的名称
        :param class_name: 元素class名字
        :return:
        """
        get_img_js = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.browser.execute_script(get_img_js)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

    """
    拖动滑块到缺口处
    :param slider: 滑块
    :param track: 轨迹
    :return:
    """

    def start_to_move(self, track):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        ActionChains(self.browser).release().perform()

    def crack(self, reset_status=True):
        # 访问网站并且输入用户名和密码，然后点击验证码按钮
        if reset_status:
            self.prepare_for_login()
        # 保存图片
        # image1 = self.get_geetest_image()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_bg')))
        self.save_captcha_img('tmp_data/captcha1.png', 'geetest_canvas_fullbg')
        self.save_captcha_img('tmp_data/captcha2.png', 'geetest_canvas_bg')

        # 计算移动距离
        img1 = Image.open('tmp_data/captcha1.png')
        img2 = Image.open('tmp_data/captcha2.png')
        move_distance = get_move_distance(img1, img2)
        # print('need move move_distance:' + str(move_distance))

        move_distance -= BORDER
        # 获取轨迹
        # track = self.get_track(move_distance)
        tracks = get_tracks(move_distance, 3, 'ease_out_quad')
        # 开始移动
        self.start_to_move(tracks)

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
            json_cookies = json.dumps(cookie)
            with open('tmp_data/xueqiu_cookie.json', 'w') as f:
                print(f'将cookies写入到文件: {json_cookies}')
                f.write(json_cookies)
                f.close()
            self.browser.quit()
            return True


if __name__ == '__main__':
    crack = CrackXueQiu()
    crack.crack()
