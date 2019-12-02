#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import hmac
import hashlib
import base64
import urllib
import os
from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
# webhook = 'https://oapi.dingtalk.com/robot/send?access_token=XXXXXX&timestamp=XXX&sign=XXX'
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def getsign(msg):
    timestamp = int(round(time.time() * 1000))
    secret = os.getenv("secret")
    secret_enc = secret.encode('utf-8')


    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    # hmac_code = hmac.new(secret, string_to_sign, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(timestamp)
    print(sign)
    token = os.getenv("token")
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s&&timestamp=%s&sign=%s'
    weburl = url %(token,timestamp,sign)
    print(weburl)
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(weburl)
    # Text消息@所有人
    xiaoding.send_text(msg=msg, is_at_all=False)


# getsign(msg='现在钉钉机器人的接口安全性有提升，调用也更复杂了')
# getsign(msg='……\n有没有人提交代码，就剩我们机器人聊了？你是个克林贡人还是个智能程序？')

# getsign(msg='岁月其徂，年其逮耇~距离2020年元旦，只剩%d天~'%())
import datetime
target = datetime.datetime(2020, 1, 1)
diff = target - datetime.datetime.now()
msg = '岁月其徂，年其逮耇\n距离2020年元旦，还有%s' % (diff)
print(msg)
# getsign(msg=msg)
