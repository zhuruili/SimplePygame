import copy

from core.stack import Stack

# 关卡
class Level:
    """ 关卡管理类 """

    # 关卡字典
    point = {
            1:[
                [9,9,1,1,1,9,9,9],
                [9,9,1,4,1,9,9,9],
                [9,9,1,0,1,1,1,1],
                [1,1,1,2,0,2,4,1],
                [1,4,0,2,3,1,1,1],
                [1,1,1,1,2,1,9,9],
                [9,9,9,1,4,1,9,9],
                [9,9,9,1,1,1,9,9]
            ],
        2: [
            [9, 9, 1, 1, 1, 1, 9, 9],
            [9, 9, 1, 4, 4, 1, 9, 9],
            [9, 1, 1, 0, 4, 1, 1, 9],
            [9, 1, 0, 0, 2, 4, 1, 9],
            [1, 1, 0, 2, 3, 0, 1, 1],
            [1, 0, 0, 1, 2, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ],
        3:[
            [9,9,1,1,1,1,9,9],
            [9,1,1,0,0,1,9,9],
            [9,1,3,2,0,1,9,9],
            [9,1,1,2,0,1,1,9],
            [9,1,1,0,2,0,1,9],
            [9,1,4,2,0,0,1,9],
            [9,1,4,4,6,4,1,9],
            [9,1,1,1,1,1,1,9]

        ],
        4:[

            [1,1,1,1,1,9,9,9,9],
            [1,0,0,0,1,1,1,1,1],
            [1,2,1,0,1,0,0,0,1],
            [1,0,0,0,0,0,2,0,1],
            [1,4,5,1,2,1,2,1,1],
            [1,4,2,0,0,0,0,1,9],
            [1,4,4,0,0,1,1,1,9],
            [1,1,1,1,1,1,9,9,9]

        ],

        5:[
            [9,1,1,1,1,1,9,9],
            [9,1,4,0,0,1,9,9],
            [9,1,0,1,2,1,9,9],
            [9,1,0,0,0,1,9,9],
            [9,1,0,1,0,1,1,1],
            [9,1,4,0,2,0,0,1],
            [9,1,0,0,5,2,0,1],
            [9,1,1,1,1,1,1,1]
        ],

        6:[
            [9,1,1,1,1,1,1,9,9],
            [9,1,0,0,0,0,1,1,9],
            [1,1,4,1,1,0,0,1,9],
            [1,0,6,5,0,0,0,1,9],
            [1,0,0,1,2,2,0,1,9],
            [1,0,0,0,0,1,1,1,9],
            [1,1,1,1,1,1,9,9,9],
            [9,9,9,9,9,9,9,9,9]

        ],
        7:[
            [9,1,1,1,1,1,9,9,9],
            [9,1,0,3,0,1,1,1,9],
            [1,1,0,1,2,0,0,1,9],
            [1,0,6,4,0,4,0,1,9],
            [1,0,0,2,2,0,1,1,9],
            [1,1,1,0,1,4,1,9,9],
            [9,9,1,0,0,0,1,9,9],
            [9,9,1,1,1,1,1,9,9]

        ],
        8:[
            [1,1,1,1,1,1,1,9],
            [1,4,4,2,4,4,1,9],
            [1,4,4,1,4,4,1,9],
            [1,0,2,2,2,0,1,9],
            [1,0,0,2,0,0,1,9],
            [1,0,2,2,2,0,1,9],
            [1,0,0,1,3,0,1,9],
            [1,1,1,1,1,1,1,9]


        ],
        9:[
            [1,1,1,1,1,1,9,9],
            [1,0,0,0,0,1,9,9],
            [1,0,4,6,0,1,1,1],
            [1,0,4,2,4,2,0,1],
            [1,1,0,2,0,0,0,1],
            [9,1,1,1,1,0,3,1],
            [9,9,9,9,1,1,1,1],
            [9,9,9,9,9,9,9,9]
        ],
        10:[
            [9,9,1,1,1,1,1,9,9],
            [9,1,1,0,3,0,1,1,9],
            [9,1,0,0,6,2,0,1,9],
            [9,1,2,0,4,0,2,1,9],
            [9,1,4,4,1,4,4,1,9],
            [1,1,2,0,6,0,0,1,1],
            [1,0,2,0,1,0,2,0,1],
            [1,0,0,0,1,0,0,0,1],
            [1,1,1,1,1,1,1,1,1]
        ]
    }
    # 矩阵元素
    CHAN, WALL, BOX, PERSON, GOAL, HOME, REPO = 0,1,2,3,4,5,6
    # 键盘方向键
    UP, RIGHT, BOTTOM, LEFT = 1, 2, 3, 4

    def __init__(self, screen):
        self.game_level = 1                        # 当前关卡等级
        self.frame = self.point[self.game_level]   # 当前关卡矩阵
        self.screen = screen           # 窗口Surface对象
        self.hero_dir = 2              # 玩家移动的方向索引

        self.old_frame = copy.deepcopy(self.frame) # 在移动之前记录关卡矩阵
        self.step = 0                  # 玩家移动步数
        self.undo_stack = Stack(5)     # 用于撤销的栈

    @property
    def level(self):
        return self.game_level

    @level.setter
    def level(self, lev):
        self.game_level = lev
        self.frame = self.point[self.game_level]  # important

    # 矩阵操作维护
    def operate(self, direction,):
        """ 矩阵操作维护 """
        self.hero_dir = direction - 1              # 改变玩家的方向
        self.old_frame = copy.deepcopy(self.frame) # 在移动之前记录矩阵
        if direction == self.UP:       # 上
            before = (self.person_posi[0] - 1, self.person_posi[1])
        elif direction == self.RIGHT:  # 右
            before = (self.person_posi[0], self.person_posi[1] + 1)
        elif direction == self.BOTTOM: # 下
            before = (self.person_posi[0] + 1, self.person_posi[1])
        elif direction == self.LEFT:   # 左
            before = (self.person_posi[0], self.person_posi[1] - 1)
        # 开始判断然后相应移动
        if self.get_before_val(direction) == self.WALL:     # 墙
            pass
        elif self.get_before_val(direction) == self.CHAN:   # 通道
            self.move_ele(direction)
        elif self.get_before_val(direction) == self.GOAL:   # 目的地
            self.move_ele(direction)
        elif self.get_before_val(direction) in [self.BOX, self.REPO]:  # 箱子和仓库
            if self.get_before_val(direction, before) == self.WALL:    # 墙
                pass
            elif self.get_before_val(direction, before) == self.CHAN:  # 通道
                self.move_ele(direction, before)
                self.move_ele(direction)
            elif self.get_before_val(direction, before) == self.GOAL:  # 目的地
                self.move_ele(direction, before)
                self.move_ele(direction)
        # 记录玩家移动步数
        self.add_step()
        # 记录玩家移动之前的矩阵数据进栈
        self.record_frame()

    # 移动矩阵元素
    def move_ele(self, direction, posi = None):
        """ 移动矩阵元素 """
        if not posi:
            posi = self.person_posi
        now = self.frame[posi[0]][posi[1]] # 当前值
        # 对前一个位置赋值
        if direction == self.UP:       # 上
            before = self.frame[posi[0] - 1][posi[1]]
            self.set_before_val(direction, now, before, posi)

        elif direction == self.RIGHT:  # 右
            before = self.frame[posi[0]][posi[1] + 1]
            self.set_before_val(direction, now, before, posi)

        elif direction == self.BOTTOM: # 下
            before = self.frame[posi[0] + 1][posi[1]]
            self.set_before_val(direction, now, before, posi)

        elif direction == self.LEFT:   # 左
            before = self.frame[posi[0]][posi[1] - 1]
            self.set_before_val(direction, now, before, posi)
        # 对原先的位置赋值
        if now == self.HOME or now == self.REPO:         # 人出目的地和箱子出目的地
            self.frame[posi[0]][posi[1]] = self.GOAL
        elif before == self.GOAL:                        # 人进目的地
            if now == self.HOME:                         # 从家进的
                self.frame[posi[0]][posi[1]] = self.GOAL
            else:
                self.frame[posi[0]][posi[1]] = self.CHAN
        elif before == self.GOAL:                        # 箱子进目的地
            if now == self.REPO:                         # 从仓库进的
                self.frame[posi[0]][posi[1]] = self.GOAL
            else:
                self.frame[posi[0]][posi[1]] = self.CHAN
        else:
            self.frame[posi[0]][posi[1]] = before        # 通道

    # 对某一元素对应方向之前的元素赋值
    def set_before_val(self, direction, now, before, posi):
        """ 对某一元素对应方向之前的元素赋值 """
        before_val = None
        if before == self.GOAL and now == self.PERSON:  # 人进目的地
            before_val = self.HOME
        elif before == self.GOAL and now == self.BOX:   # 箱子进目的地
            before_val = self.REPO
        elif now == self.HOME:                          # 人出目的地
            if before == self.GOAL:                     # 又进目的地
                before_val = self.HOME
            else:
                before_val = self.PERSON
        elif now == self.REPO:                          # 箱子出目的地
            if before == self.GOAL:                     # 又进目的地
                before_val = self.REPO
            else:
                before_val = self.BOX
        else:
            before_val = now

        if direction == self.UP:        # 上
            self.frame[posi[0] - 1][posi[1]] = before_val
        elif direction == self.RIGHT:   # 右
            self.frame[posi[0]][posi[1] + 1] = before_val
        elif direction == self.BOTTOM:  # 下
            self.frame[posi[0] + 1][posi[1]] = before_val
        elif direction == self.LEFT:    # 左
            self.frame[posi[0]][posi[1] - 1] = before_val

    # 获取某一元素对应方向之前的元素的值
    def get_before_val(self, direction, posi = None):
        """ 获取某一元素对应方向之前的元素的值 """
        if not posi:
            posi = self.person_posi
        if direction == self.UP:      # 上
            if posi[0] >= 1:
                return self.frame[posi[0] - 1][posi[1]]
        elif direction == self.RIGHT: # 右
            if posi[1] < len(self.frame[posi[0]]):
                return self.frame[posi[0]][posi[1] + 1]
        elif direction == self.BOTTOM: # 下
            if posi[0] < len(self.frame):
                return self.frame[posi[0] + 1][posi[1]]
        elif direction == self.LEFT:   # 左
            if posi[1] >= 1:
                return self.frame[posi[0]][posi[1] - 1]
        return None

    # 获取玩家位置
    @property
    def person_posi(self):
        """ 获取玩家位置 """
        for row, li in enumerate(self.point[self.game_level]):
            for col, val in enumerate(li):
                if val in [3, 5]:
                    return (row, col)

    # 检查是否通关
    def is_success(self):
        """ 检测是否通关 """
        for row, li in enumerate(self.point[self.game_level]):
            for col, val in enumerate(li):
                if val in [2, 4]:  # 存在目的地
                    return False
        return True

    # 检测是否移动
    def is_move(self):
        """ 检测是否移动 """
        if self.old_frame != self.frame:  # 比较值
            return True
        return False

    # 记录玩家移动步数
    def add_step(self):
        """ 记录玩家移动步数 """
        if self.is_move():
            self.step += 1

    # 记录玩家移动前的矩阵
    def record_frame(self):
        """ 记录玩家移动前的矩阵 """
        if self.is_move():
            self.undo_stack.push(copy.deepcopy(self.old_frame))
            # self.stack_push_switch = False










