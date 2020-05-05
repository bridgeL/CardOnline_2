import communication as com
import globalvalue as gv
import gamectrl

import threading


# 单文件全局变量

# 键盘输入
word = ''


def init():
    threading.Thread(target=keyboard_thread, args=()).start()
    com.init()


def keyboard_thread():
    '''为键盘输入设置一个线程'''
    global word
    while True:
        word = input('>')
        if word == '/exit':
            break


def deal():
    '''处理各类事件'''
    # 处理键盘事件
    if deal_keyboard():
        return 1

    # 处理消息事件
    deal_msg()

    return 0


def deal_keyboard():
    '''处理键盘输入的各种命令'''
    global word
    if word:
        if word[0] == '/':
            if word == '/exit':

                # 关闭通讯模块
                com.close()
                return 1

            elif word == '/close':
                word = ''
                com.close()

            # elif word == '/build deck':
            #     word = ''
            #     gamectrl.build_deck()

    return 0


def deal_msg():
    '''处理消息队列中的消息，丢给不同的模块的函数处理'''
    msg_list = gv.msg_list
    gv.msg_list = []

    for m in msg_list:
        t = m.type
        if t == 1:
            gamectrl.answer_name_set(m)
        elif t == 2:
            gamectrl.answer_site_set(m)
        elif t == 3:
            gamectrl.answer_game_start(m)
        elif t == 11:
            gamectrl.answer_exit(m)
        elif t == 10:
            gamectrl.answer_login(m)
