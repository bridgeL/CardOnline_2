import communication as com
import globalvalue as gv
import gamectrl

import threading

# 单文件全局变量

# 按键输入
word = ''


def init():
    threading.Thread(target=keyboard_thread, args=()).start()
    com.connect()


def keyboard_thread():
    '''为键盘输入设置一个线程'''
    global word
    while True:
        word = input('>')
        if word == '/exit':
            break


def deal():
    '''处理各类事件'''
    # 处理鼠标事件
    if deal_mouse():
        return 1

    # 处理键盘事件
    if deal_keyboard():
        return 1

    # 处理消息事件
    deal_msg()

    return 0


def deal_mouse():
    '''处理点击卡片/座位等操作，以及关闭窗口等操作'''

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

            else:
                # 命令分解
                cmd_list = word.split()
                word = ''

                # 进入游戏大厅
                if cmd_list[0] == '/login':
                    gv.game_page = 1

                # 修改昵称
                elif cmd_list[0] == '/name':
                    gamectrl.require_name_set(cmd_list[1])

                # 修改座位
                elif cmd_list[0] == '/sit':
                    gamectrl.require_site_set(int(cmd_list[1]))

                # 开始游戏
                elif cmd_list[0] == '/start':
                    gamectrl.require_game_start()

#                 # 打牌
#                 elif cmd_list[0] == '/play':
#                     gamectrl.require_play_card(int(cmd_list[1]))

                # 测试
                elif cmd_list[0] == '/test':

                    # # 测试 多信息密集发送 是否能做到 接收端 自动 分割
                    # if cmd_list[1] == 'msgs':
                    #     msg = com.GAMEMSG(gv.dev_num, 0, 0, 1, bytes([99]))
                    #     com.send(msg)
                    #     com.send(msg)
                    #     com.send(msg)

                    # 方便测试，自动输入加入房间后的各类指令
                    if cmd_list[1] == '0':
                        gv.game_page = 1
                        gamectrl.require_name_set('a')
                        gamectrl.require_site_set(0)
                    elif cmd_list[1] == '1':
                        gv.game_page = 1
                        gamectrl.require_name_set('b')
                        gamectrl.require_site_set(1)
                    elif cmd_list[1] == '2':
                        gv.game_page = 1
                        gamectrl.require_name_set('c')
                        gamectrl.require_site_set(2)
                    elif cmd_list[1] == '3':
                        gv.game_page = 1
                        gamectrl.require_name_set('d')
                        gamectrl.require_site_set(3)

    return 0


def deal_msg():
    '''处理消息队列中的消息，丢给不同的模块的函数处理'''
    msg_list = gv.msg_list
    gv.msg_list = []

    for m in msg_list:
        mm = com.GAMEMSG(0, 0, 0,  bytes([]))
        mm.BYTE2MSG(m.msg)
        dev_num = mm.send
        t = m.type
        if t == 0 or t == -1:
            if dev_num == gv.dev_num:
                tt = mm.type
                if tt == 1:
                    gamectrl.answer_name_set(t + 1, mm)
                elif tt == 2:
                    gamectrl.answer_site_set(t + 1, mm)
                elif tt == 3:
                    gamectrl.answer_game_start(t + 1)
        elif t == -2:
            if dev_num != gv.dev_num:
                t = mm.type
                if t == 1:
                    gamectrl.told_name_set(mm)
                elif t == 2:
                    gamectrl.told_site_set(mm)
                elif t == 3:
                    gamectrl.told_game_start()
