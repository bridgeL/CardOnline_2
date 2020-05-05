import globalvalue as gv

from socket import *
import threading

# 单文件全局变量

# 消息尾标
msg_end_flag = bytes([254])

# 连接许可通过，这个关闭connect函数
connect_permission = 1

# type base
type_base = 70


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
        return bytes([self.send, self.rec, self.type + type_base]) + self.msg

    def BYTE2MSG(self, bs):
        '''转换BYTE信息为消息类，便于使用'''
        self.send = bs[0]
        self.rec = bs[1]
        self.type = bs[2] - type_base
        self.msg = bs[3:]


def listen_thread(conn, addr):
    '''为每个客户端都建立一份监听线程'''

    print('...connnecting from:', addr)

    dev_num = gv.dev.add(conn)
    conn.send(bytes([dev_num]))

    print('give dev_num = ', dev_num)

    flag = True
    while flag:
        bs = conn.recv(1024)

        # 根据信息尾标，进行信息分割
        bs_list = bs.split(msg_end_flag)
        # print(bs_list)
        for b in bs_list:
            if b.__len__() > 0:
                msg = GAMEMSG(0, 0, 0, bytes([]))
                msg.BYTE2MSG(b)
                gv.msg_list.append(msg)
                print(['recv:', msg.MSG2BYTE()])

                if msg.type == 11:
                    m = GAMEMSG(0, msg.send, 11, bytes([]))
                    send(m)
                    flag = False
                    break

    conn.close()
    print('...connnection close:', addr)


def init():
    threading.Thread(target=connect, args=()).start()


def connect():
    HOST = ''
    PORT = 21567
    ADDR = (HOST, PORT)

    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDR)
    server.listen(10)  # 最大连接数10

    print('waiting for connection...')
    while True:
        conn, addr = server.accept()
        threading.Thread(target=listen_thread, args=(conn, addr)).start()

        global connect_permission
        if not connect_permission:
            break

    server.close()
    print('server connect permission close')


def close():
    global connect_permission
    if connect_permission:
        connect_permission = 0

        # 新建一个虚拟客户端连接
        fakeClient = socket(AF_INET, SOCK_STREAM)

        HOST = '127.0.0.1'  # or 'localhost'
        PORT = 21567
        ADDR = (HOST, PORT)

        fakeClient.connect(ADDR)
        bs = fakeClient.recv(1024)
        m = GAMEMSG(bs[0], 0, 11, bytes([]))
        fakeClient.send(m.MSG2BYTE() + msg_end_flag)
        fakeClient.recv(1024)
        fakeClient.close()


def send(msg):

    dev_num = msg.rec
    dev_dict = gv.dev.dict
    if dev_num == 0:
        # 广播告知所有设备
        for conn in dev_dict.values():

            # 添加信息尾标，用于信息分割
            bs = msg.MSG2BYTE() + msg_end_flag
            conn.send(bs)
            print(['send:', bs])

    else:
        # 仅发送此设备
        if dev_num in dev_dict.keys():

            conn = dev_dict[dev_num]

            # 添加信息尾标，用于信息分割
            bs = msg.MSG2BYTE() + msg_end_flag
            conn.send(bs)
            print(['send:', bs])
