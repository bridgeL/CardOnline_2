import globalvalue as gv
import communication as com


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

    if gv.game_page == 1:
        site_num = msg.msg[0]
        site_dict = gv.site_dict

        # 非空座
        if site_num in site_dict.keys():
            m_ans = com.GAMEMSG(0, dev_num, -1, bs)
            com.send(m_ans)

        # 空座
        else:
            # keys() 与 values() 一一对应，因此根据value查询values下标即可反推出keys中的key
            site_dict_k = list(site_dict.keys())
            site_dict_v = list(site_dict.values())
            site_num_old = -1
            if dev_num in site_dict_v:
                site_num_old = site_dict_k[site_dict_v.index(dev_num)]

            if site_num_old != -1:
                del gv.site_dict[site_num_old]

            gv.site_dict[site_num] = dev_num

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

        site_dict = gv.site_dict
        # 首位有人坐
        if 0 in site_dict.keys():
            if site_dict[0] == dev_num:
                player_num = site_dict.__len__()

                if player_num >= 4:
                    m_ans = com.GAMEMSG(0, dev_num, 0, bs)
                    m_all = com.GAMEMSG(0, 0, -2, bs)
                    com.send(m_ans)
                    com.send(m_all)

                    # 游戏开始
                    gv.game_page = 2

                    # 重新生成紧密排列的座位表

                    # 生成牌库，洗牌，发牌
                    # build_deck()

                    # 查找第一发现人
                    return
    m_ans = com.GAMEMSG(0, dev_num, -1, bs)
    com.send(m_ans)


# def build_deck():
#     '''
#         创建牌组，洗牌，并分配初始手牌

#         普通人 0
#         不在场证明 1
#         第一发现人 2
#         共犯 3
#         目击者 4
#         谣言 5
#         情报交换 6
#         交易 7
#         犯人 8
#         侦探 9
#         神犬 10

#         -12号消息
#         0，客户端设备号，消息号，1 + 2*卡牌个数，[自己/其他人设备号,[卡牌id,卡牌type],...]

#     '''
#     player_num = gv.site_dict.__len__()
#     card_num = player_num * 4

#     # <card_id, card_type>
#     deck = dict()

#     # 全部是普通人
#     for i in range(card_num):
#         deck[i] = 0

#     # 洗牌

#     # 发牌

#     site_order_list = gv.site_order_list
#     for site_num in site_order_list:
#         gv.player_card_dict[site_num] = dict()

#     for i in range(card_num):
#         site_num = site_order_list[i % player_num]
#         gv.player_card_dict[site_num][i] = deck[i]

#     site_dict = gv.site_dict
#     for site_num in site_order_list:
#         card_list = gv.player_card_dict[site_num]
#         dev_num = site_dict[site_num]
#         bs = bytes([])
#         for card_id in card_list.keys():
#             card_type = card_list[card_id]
#             bs = bs + bytes([card_id, card_type])
#         msg = com.GAMEMSG(0, dev_num, -12, 2*4+1,
#                           bytes([dev_num]) + bs)
#         com.send(msg)
