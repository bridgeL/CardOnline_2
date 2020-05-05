import globalvalue as gv
import communication as com


def answer_login(msg):
    '''
        10号消息
        客户端设备号，0，10
    '''
    div_flag = bytes([253])
    dev_num = msg.send
    bs = bytes(gv.dev.dict.keys()) + div_flag + \
        bytes(gv.name_dict.keys()) + div_flag
    for v in gv.name_dict.values():
        bs = bs + v.encode() + div_flag
    bs = bs + bytes(gv.site_list) + div_flag
    m = com.GAMEMSG(0, dev_num, -4, bs)
    com.send(m)


def answer_exit(msg):
    '''
        11号消息
        客户端设备号，0，11
    '''
    dev_num = msg.send
    del gv.dev.dict[dev_num]


def answer_name_set(msg):
    '''
        1号消息
        客户端设备号，0，1，名字
    '''
    bs = msg.MSG2BYTE()
    dev_num = msg.send

    if gv.game_page == 1:
        name = msg.msg.decode()

        m_all = com.GAMEMSG(0, 0, -2, bs)
        m_ans = com.GAMEMSG(0, dev_num, 0, bs)

        gv.name_dict[dev_num] = name

        com.send(m_ans)
        com.send(m_all)

    else:
        m_ans = com.GAMEMSG(0, dev_num, -1, bs)
        com.send(m_ans)


def answer_site_set(msg):
    '''
        2号消息
        客户端设备号，0，2，座位号
    '''

    dev_num = msg.send
    bs = msg.MSG2BYTE()
    site_num = msg.msg[0]

    if gv.game_page == 1 and site_num < 8 and gv.name_dict[dev_num] != '':

        # 非空座
        if gv.site_list[site_num] != 0:
            m_ans = com.GAMEMSG(0, dev_num, -1, bs)
            com.send(m_ans)

        # 空座
        else:
            if dev_num in gv.site_list:
                gv.site_list[gv.site_list.index(dev_num)] = 0

            gv.site_list[site_num] = dev_num
            print('site_list', gv.site_list)

            m_ans = com.GAMEMSG(0, dev_num, 0, bs)
            m_all = com.GAMEMSG(0, 0, -2, bs)
            com.send(m_ans)
            com.send(m_all)

    else:
        m_ans = com.GAMEMSG(0, dev_num, -1, bs)
        com.send(m_ans)


def answer_game_start(msg):
    '''
        3号消息
        客户端设备号，0，3，''
    '''
    dev_num = msg.send
    bs = msg.MSG2BYTE()

    if gv.game_page == 1:

        # 首位有人坐
        if gv.site_list[0] == dev_num:
            player_num = 0
            for s in gv.site_list:
                if s != 0:
                    player_num = player_num + 1

            if player_num >= 4:
                m_ans = com.GAMEMSG(0, dev_num, 0, bs)
                m_all = com.GAMEMSG(0, 0, -2, bs)
                com.send(m_ans)
                com.send(m_all)

                gv.player_num = player_num
                set_game_page(2)
                return

    m_ans = com.GAMEMSG(0, dev_num, -1, bs)
    com.send(m_ans)


def set_game_page(page):

    if(page == 2):
        # 游戏开始
        gv.game_page = 2

        # 重新生成紧密排列的座位表
        new_site_list = [0, 0, 0, 0, 0, 0, 0, 0]
        cnt = 0
        for s in gv.site_list:
            if s != 0:
                new_site_list[cnt] = s
                cnt = cnt + 1

        gv.site_list = new_site_list

        # 生成牌库，洗牌，发牌
        '''
            普通人 0
            不在场证明 1
            第一发现人 2
            共犯 3
            目击者 4
            谣言 5
            情报交换 6
            交易 7
            犯人 8
            侦探 9
            神犬 10
        '''
        card_deck = []
        player_num = gv.player_num
        card_num = player_num * 4
        for i in range(card_num):
            card_deck.append(0)

        # 洗牌

        # 发牌
        for i in range(player_num):
            gv.player_card_list[i] = []

        cnt = 0
        for c in card_deck:
            gv.player_card_list[cnt].append(c)
            cnt = cnt + 1
            if cnt >= player_num:
                cnt = 0

        for i in range(player_num):
            dev_num = new_site_list[i]
            bs = bytes([dev_num] + gv.player_card_list[i])
            m = com.GAMEMSG(0, dev_num, -3, bs)
            com.send(m)

        # 查找第一发现人
