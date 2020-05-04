import globalvalue as gv

from socket import *
import threading


# 单文件全局变量

# TCP连接
conn = socket(AF_INET, SOCK_STREAM)

# 消息尾标
msg_end_flag = bytes([254])

# 关闭连接标志
com_exit_flag = bytes([255])


class GAMEMSG:
    '''游戏消息类'''

    def __init__(self, send, rec, type0, msg):
        ''' 
            int 发信人设备号
            int 收信人设备号
            int 消息类型
            bytes 消息数组
        '''
        self.send = send
        self.rec = rec
        self.type = type0
        self.msg = msg

    def MSG2BYTE(self):
        '''转换消息类为BYTE信息，便于传输'''
        return bytes([self.send, self.rec, self.type + 30]) + self.msg

    def BYTE2MSG(self, bs):
        '''转换BYTE信息为消息类，便于使用'''
        self.send = bs[0]
        self.rec = bs[1]
        self.type = bs[2] - 30
        self.msg = bs[3:]


def connect():
    HOST = '127.0.0.1'  # or 'localhost'
    PORT = 21567
    ADDR = (HOST, PORT)

    global conn
    conn.connect(ADDR)

    bs = conn.recv(1024)

    gv.dev_num = bs[0]
    print('dev_num = ', gv.dev_num)

    threading.Thread(target=listen_thread, args=()).start()


def listen_thread():

    global conn
    while True:

        bs = conn.recv(1024)

        if bs == com_exit_flag:
            conn.close()
            break

        # 根据信息尾标，进行信息分割
        bs_list = bs.split(msg_end_flag)
        # print(bs_list)
        for b in bs_list:
            if b.__len__() > 0:
                msg = GAMEMSG(0, 0, 0, bytes([]))
                msg.BYTE2MSG(b)
                gv.msg_list.append(msg)
                # print(['debug recv:', msg.MSG2BYTE()])


def send(msg):

    # 添加信息尾标254，用于信息分割
    bs = msg.MSG2BYTE() + msg_end_flag

    global conn
    conn.send(bs)
    # print(['debug send:', bs])


def close():
    global conn
    conn.send(com_exit_flag)
