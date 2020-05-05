import globalvalue as gv
import communication as com


''' ''' ''' ''' ''' ''' ''' ''' ''' require ''' ''' ''' ''' ''' ''' ''' ''' '''


def require_login():
    com.connect()
    m = com.GAMEMSG(gv.dev_num, 0, 10, bytes([]))
    com.send(m)


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

        if gv.name == '':

            # 一些图形操作
            print('起名后才能选座')

        else:

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


def told_game_room(msg):
    gv.game_page = 1
    bs = msg.msg
    div_flag = bytes([253])
    bs_list = bs.split(div_flag)
    bs_list.pop()

    for dev_num in bs_list[0]:
        gv.dev_num_list.append(dev_num)

    cnt = 2
    for i in range(bs_list[1].__len__()):
        gv.name_dict[bs_list[1][i]] = bs_list[cnt].decode()
        cnt = cnt + 1

    for i in range(bs_list[cnt].__len__()):
        gv.site_list[i] = bs_list[cnt][i]

    print(gv.dev_num_list, gv.name_dict, gv.site_list)


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

        if dev_num in gv.site_list:
            gv.site_list[gv.site_list.index(dev_num)] = 0

        gv.site_list[site_num] = dev_num

        # 一些图形操作
        print(gv.name_dict[dev_num], ' 加入了 ', site_num, ' 号座位')
        print('site_list', gv.site_list)


def told_game_start():

    if gv.game_page == 1 and gv.site_num != -1:

        # 一些图像操纵
        print('游戏开始')

        gv.game_mode = 2

    # else:
    # 旁观模式仍在开发中
    #     # 一些图形操作
    #     print('本局游戏已经开始了，你可（zhi）以（neng）旁观')


def told_card_list(msg):
    '''
        -3号消息
        0，自己设备号，-3，[自己/他人的设备号,[手牌类别号,...]]
    '''
    bs = msg.msg
    dev_num = bs[0]
    card_list = []
    for i in range(bs.__len__()-1):
        card_list.append(bs[i+1])

    if dev_num == gv.dev_num:
        gv.card_list = card_list

        # 一些图形操作
        print('初始手牌: ', card_list)

    else:

        # 一些图形操作
        name = gv.name_dict[dev_num]
        print(name, '的手牌: ', card_list)


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

        if(gv.site_num != -1):
            gv.site_list[gv.site_num] = 0

        gv.site_num = site_num
        gv.site_list[site_num] = gv.dev_num

        # 一些图形操作
        print('你加入', site_num, '号座位成功')
        print('site_list', gv.site_list)

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
