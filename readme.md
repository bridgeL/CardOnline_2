- 总述
  - 客户端
    - 命令行界面交互逻辑，提供API
    - 图形界面交互逻辑，提供API
    - 游戏逻辑，调用API
  - 服务器端
    - 命令行界面交互逻辑，提供API
    - 游戏逻辑，调用API
- 通用框架
  - 命令行界面/图形界面受到激发产生消息，放入界面消息池
  - 通讯模块受到消息，放入游戏消息池
  - 主循环读取界面/游戏消息池，处理内容
    - 处理内容时需要产生界面变化时，调用界面模块提供的API
- 通讯消息
  - 通讯消息类
    - send dev num
    - rec dev num
    - msg type
    - msg bytes
    - 消息尾标
  - 消息类型
    - 客户端
      - 1 设置昵称 bytes长度?（昵称）
      - 2 设置座位 bytes长度1（座位码）
      - 3 开始游戏 bytes长度0
      - 4 发送表情 1（表情码）
      - 5 摸牌 0
      - 6 打牌 1+？（卡牌类别码+卡牌要求的特殊效果：例如指定几位玩家等）
      - 7 抽牌 1（抽取对象的座位码）
      - 8 给牌 1+1（给予对象的座位码+卡牌类别码）
      - 9 看牌 1（查看对象的座位码）
    - 服务器端
      - 答复
        - 0 成功 ？（答复的请求）
        - -1 失败 ？（答复的请求）
      - 通知
        - 普通请求
          - -2 消息转发 ？（合理的请求消息的编码）
        - 特殊请求
          - -3 通知手牌 1+？（目标对象的座位码+卡牌类别码）
- 卡牌
  - 类别码
  - 生成打牌消息
  - 处理打牌消息（调用图形界面API）
- 客户端
  - 处理消息
    - 生成请求消息
    - 处理答复消息
    - 处理通知消息