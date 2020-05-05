# 跨文件全局变量

# 消息队列
msg_list = []

# 被分配的设备号
dev_num = 0

# 游戏页
game_page = 0
'''
    0 游戏启动页
    1 游戏大厅页
    2 游戏业务页
'''

# 自己的昵称
name = ''

# 昵称列表 <dev_num, name>
name_dict = dict()

# 自己的座位号
site_num = -1

# 座位列表 [dev_num,...] 最多8人
site_list = [0, 0, 0, 0, 0, 0, 0, 0]

# 自己在游戏中的阵营
group = 0

# 自己的手牌 [type,...]
card_list = []

# 暂时选中的牌的type
card_choose_type = -1
