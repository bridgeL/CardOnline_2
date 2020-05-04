class GAMEDEVICELIST:
    '''管理设备的设备列表, 专门写成一个类是为了便于实现自动分配设备号'''

    def __init__(self):
        self.dict = dict()
        self.cnt = 1

    def add(self, conn):
        num = self.cnt      # 这里可以生成随机的不重复随机码，以防恶意的客户端抢夺连接
        self.cnt = self.cnt + 1
        self.dict[num] = conn

        return num

# 跨文件全局变量


# 消息队列
msg_list = []

# 设备列表 <dev_num, conn>
dev = GAMEDEVICELIST()

# 昵称列表 <dev_num, name>
name_dict = dict()

# 座位列表 <site_num, dev_num>
site_dict = dict()

# 当前玩家的座位号
current_site_num = 0

# 玩家手牌列表 <site_num, card_dict>
player_card_dict = dict()

# 阵营列表 <site_num, group_num>
group_dict = dict()

# 游戏页
game_page = 1
'''
    1 游戏大厅页
    2 游戏业务页
'''
