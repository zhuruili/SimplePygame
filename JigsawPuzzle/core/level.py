import copy
import math
import random

from conf.settings import *

class Level:
    """ 游戏等级类 """

    def __init__(self,):
        self.frame = []                  # 游戏矩阵列表
        self.game_level = 1              # 游戏等级
        self.row_num = INIT_ROW_NUM      # 行数
        self.col_num = INIT_COL_NUM      # 列数
        self.grid_num = 0                # 矩阵方格数
        self.grid_width = 0              # 方格宽
        self.grid_height = 0             # 方格高
        self.blank = []                  # 空白方格初始矩阵行列索引
        self.step = 0                    # 交换次数
        self.old_frame = self.frame      # 记录矩阵

    def frame_init(self, manager):
        """ 矩阵初始化 """
        self.manager = manager
        self.grid_num = self.row_num * self.col_num
        self.frame = [[(i + j * self.col_num) for i in range(self.col_num)] for j in range(self.row_num)]
        self.grid_width = manager.game_rect.width // self.col_num
        self.grid_height = manager.game_rect.height // self.row_num
        # 初始空白方格位置
        self.blank = [random.randint(0, self.row_num - 1), random.randint(0, self.col_num - 1)]
        self.frame[self.blank[0]][self.blank[1]] = -1
        self.auto_run() # 自动交换

    def exchange(self, one, two):
        """ 方格交换 """
        self.frame[one[0]][one[1]], self.frame[two[0]][two[1]] = \
            self.frame[two[0]][two[1]], self.frame[one[0]][one[1]]

    def operate(self, direction, manual = True):
        """ 矩阵操作维护 """
        # 记录矩阵
        if manual:
            self.old_frame = copy.deepcopy(self.frame)
        if direction == BOTTOM:
            if self.blank[0] >= 1:
                self.exchange(self.blank, (self.blank[0] - 1, self.blank[1]))
                self.blank[0] -= 1
        elif direction == LEFT:
            if self.blank[1] <= self.col_num - 2:
                self.exchange(self.blank, [self.blank[0], self.blank[1] + 1])
                self.blank[1] += 1
        elif direction == UP:
            if self.blank[0] <= self.row_num - 2:
                self.exchange(self.blank, (self.blank[0] + 1, self.blank[1]))
                self.blank[0] += 1
        elif direction == RIGHT:
            if self.blank[1] >= 1:
                self.exchange(self.blank, (self.blank[0], self.blank[1] - 1))
                self.blank[1] -= 1
        if manual:
            # 记录玩家移动步数
            self.add_step()

    def auto_run(self):
        """ 图形方格随机移动算法 """
        # li = [i % 5 for i in range(AUTO_RUN_STEP * self.game_level) if i % 5 != 0]
        li = [i % 5 for i in range(AUTO_RUN_STEP) if i % 5 != 0]
        random.shuffle(li)
        for i in li:
            self.operate(i, False)

    def is_success(self):
        """ 拼图成功判断 """
        self.ori_frame = [[(i + j * self.col_num) for i in range(self.col_num)] for j in range(self.row_num)]
        self.ori_frame[self.blank[0]][self.blank[1]] = -1
        if self.frame == self.ori_frame:
            return True
        return False

    # 检测是否移动
    def is_move(self):
        """ 检测是否移动 """
        if self.manager.state == 1:
            if self.old_frame != self.frame:  # 比较值
                return True
        return False

    def reset(self):
        """ 矩阵重置 """
        self.game_level += 1
        self.row_num += 1
        self.col_num += 1
        self.frame_init(self.manager)
        self.step = 0
        self.manager.button.button_bg_color = "green"
        self.manager.button.start_text = self.manager.button.button_text["start"]

    # 记录玩家移动步数
    def add_step(self):
        """ 记录玩家移动步数 """
        if self.is_move():
            self.step += 1









