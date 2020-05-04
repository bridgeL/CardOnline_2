import globalvalue as gv
import communication as com

''' ''' ''' ''' ''' ''' ''' ''' ''' require ''' ''' ''' ''' ''' ''' ''' ''' '''


def require_name_set(name):
    '''
        1号消息
        自己设备号，0，1，名字
    '''

    if gv.game_page == 1:

        if gv.name == '':

            # 一些图形操作
            print('命名请求中')

            m = com.GAMEMSG(gv.dev_num, 0, 1, name.encode())
            com.send(m)

        else:

            # 一些图形操作
            print('你已经起过名字了')


def require_site_set(site_num):
    '''
        2号消息
        自己设备号，0，2，座位号
    '''

    if gv.game_page == 1:

        m = com.GAMEMSG(gv.dev_num, 0, 2, bytes([site_num]))
        com.send(m)

        if gv.site_num == -1:

            # 一些图形操作
            print('锁定座位中')

        else:

            # 一些图形操作
            print('尝试换位中')


def require_game_start():
    '''
        3号消息
        自己设备号，0，3，''
    '''

    if gv.game_page == 1:

        if gv.site_num == 0:

            # 一些图形操作
            print('正在请求开始游戏')

            m = com.GAMEMSG(gv.dev_num, 0, 3, bytes([]))
            com.send(m)

        else:

            # 一些图形操作
            print('你不能开始游戏，只有0号位玩家可以宣布开始游戏')


# def require_play_card(card_id):
#     '''
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
#     '''
#     card_dict = gv.card_dict

#     if card_id in card_dict.keys():

#         gv.card_id_will_play = card_id

#         card_type = card_dict[card_id]

#         # 普通人
#         if card_type == 0:
#             card.play_normal_person()

#         # 不在场证明
#         elif card_type == 1:
#             card.play_alibi()


''' ''' ''' ''' ''' ''' ''' ''' ''' told ''' ''' ''' ''' ''' ''' ''' ''' '''


def told_name_set(msg):
    '''
        被转发的1号消息
        他人的设备号，0，1，名字
    '''
    if gv.game_page == 1:

        dev_num = msg.send
        name = msg.msg.decode()
        gv.name_dict[dev_num] = name

        # 一些图形操作
        print('匿名用户[', dev_num, ']更名为', name)


def told_site_set(msg):
    '''
        被转发的2号消息
        他人的设备号，0，2，座位号
    '''
    if gv.game_page == 1:

        dev_num = msg.send
        site_num = msg.msg[0]

        site_dict = gv.site_dict
        # keys() 与 values() 一一对应，因此根据value查询values下标即可反推出keys中的key
        site_dict_k = list(site_dict.keys())
        site_dict_v = list(site_dict.values())
        site_num_old = -1
        if dev_num in site_dict_v:
            site_num_old = site_dict_k[site_dict_v.index(dev_num)]

        if site_num_old != -1:
            del gv.site_dict[site_num_old]

        gv.site_dict[site_num] = dev_num

        # 一些图形操作
        print(gv.name_dict[dev_num], ' 加入了 ', site_num, ' 号座位')


def told_game_start():

    if gv.game_page == 1 and gv.site_num != -1:

        # 一些图像操纵
        print('游戏开始')

        gv.game_mode = 2

    # else:
    # 旁观模式仍在开发中
    #     # 一些图形操作
    #     print('本局游戏已经开始了，你可（zhi）以（neng）旁观')


# def told_card_dict(msg):
#     '''
#         -12号消息
#         0，自己设备号，消息号，1 + 手牌个数，[自己/其他人设备号,[手牌id,手牌类别号],...]
#     '''
#     bs = msg.msg
#     len0 = int((msg.len - 1) / 2)
#     dev_num = bs[0]

#     card_dict = defaultdict(list)
#     for i in range(len0):
#         card_id = bs[1+i*2]
#         card_type = bs[2+i*2]
#         card_dict[card_id] = card_type

#     if dev_num == gv.dev_num:
#         gv.card_dict = card_dict

#         # 一些图形操作
#         print('初始手牌: ')
#         for card_id in card_dict.keys():
#             print('ID,Type', card_id, card_dict[card_id])

#     else:

#         # 一些图形操作
#         name = gv.name_dict[dev_num]
#         print(name, '的手牌: ')
#         for card_id in card_dict.keys():
#             print('ID,Type', card_id, card_dict[card_id])


''' ''' ''' ''' ''' ''' ''' ''' ''' answer ''' ''' ''' ''' ''' ''' ''' ''' '''


def answer_name_set(ok, msg):
    '''
        缓存的1号消息
        自己设备号，0，1，昵称
    '''
    if ok:
        name = msg.msg.decode()
        gv.name = name
        gv.name_dict[gv.dev_num] = name

        # 一些图形操作
        print('你成功命名为', name)

    else:

        # 一些图形操作
        print('你命名失败')


def answer_site_set(ok, msg):
    '''
        缓存的2号消息
        自己设备号，0，2，座位号
    '''

    site_num = msg.msg[0]

    if ok:
        gv.site_num = site_num
        gv.site_dict[site_num] = gv.dev_num

        # 一些图形操作
        print('你加入', site_num, '号座位成功')

    else:

        # 一些图形操作
        print('你加入', site_num, '号座位失败')


def answer_game_start(ok):

    if ok:

        told_game_start()

        # 一些图形操作
        print('开始游戏成功')

    else:

        # 一些图形操作
        print('开始游戏失败')
