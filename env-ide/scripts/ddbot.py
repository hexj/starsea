#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=xxxx'
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook)
# Text消息@所有人
xiaoding.send_text(msg='测试一下 token是不是有效', is_at_all=False)
