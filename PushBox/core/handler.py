import copy
import sys

import pygame
from pygame.locals import *


class Element(pygame.sprite.Sprite):
    """ 游戏页面图片精灵类 """

    bg = "img/bg.png"
    blank = "img/blank.png"        # 0
    block = "img/block.png"        # 1
    box = "img/box.png"            # 2
    goal = "img/goal.png"          # 4
    box_coss = "img/box_coss.png"  # 6
    # 3, 5
    per_up, up_g = "img/up.png", "img/up_g.png"
    per_right, right_g = "img/right.png", "img/right_g.png"
    per_bottom, bottom_g = "img/bottom.png", "img/bottom_g.png"
    per_left, left_g = "img/left.png", "img/left_g.png"
    good = "img/good.png"

    frame_ele = [blank, block, box, [per_up, per_right, per_bottom, per_left], \
                 goal, [up_g, right_g, bottom_g, left_g], box_coss]

    def __init__(self, path, position):
        super(Element, self).__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = position

    # 绘制函数
    def draw(self, screen):
        """ 绘制函数 """
        screen.blit(self.image, self.rect)


class Manager:
    """ 游戏管理类 """

    def __init__(self, screen_size, lev_obj, font):
        self.size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.center = self.screen.get_rect().center  # 屏幕中心点坐标
        self.font = font                             # pygame 字体对象
        self.game_level = 1                          # 游戏关卡等级
        self.lev_obj = lev_obj                       # 关卡对象
        self.lev_obj.level = self.game_level         # 设置游戏初始关卡等级
        self.frame = self.lev_obj.frame              # 矩阵元素列表
        self.row_num = len(self.frame)               # 矩阵行数
        self.col_num = len(self.frame[1])            # 矩阵列数
        self.frame_ele_len = 50                      # 矩阵元素边长
        self.ori_frame = copy.deepcopy(self.frame)   # 保存记录本关矩阵元素
        self.next_frame_switch = False               # 下一关卡开关

    # 游戏页面绘制初始化
    def init_page(self):
        """ 游戏页面绘制初始化 """
        Element(Element.bg, (0, 0)).draw(self.screen) # 绘制背景图片
        for row, li in enumerate(self.frame):
            for col, val in enumerate(li):
                if val == 9:
                    continue
                elif val in [3, 5]:
                    Element(Element.frame_ele[val][self.lev_obj.hero_dir], self.cell_xy(row, col)).draw(self.screen)
                else:
                    Element(Element.frame_ele[val], self.cell_xy(row, col)).draw(self.screen)
        self.font = pygame.font.Font("font/SourceHanSansSC-Bold.otf", 26)
        reset_font = self.font.render("Level: %d" % self.game_level, False, (0, 88, 77))
        self.screen.blit(reset_font, (35, 24))

        step_font = self.font.render(" Step: %d" % self.lev_obj.step, False, (0, 88, 77))
        self.screen.blit(step_font, (615, 24))

        # 判断下一关页面是否绘制
        self.next_frame_switch = self.lev_obj.is_success()
        if self.next_frame_switch:
            self.next_reset()

    # 事件监听
    def listen_event(self, event):
        """ 事件监听 """
        if not self.next_frame_switch:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                """ {上: 1,  右：2, 下：3, 左：4 } """
                if event.key in [K_UP, K_w, K_w - 62]:
                    self.lev_obj.operate(1)
                if event.key in [K_RIGHT, K_d, K_d - 62]:
                    self.lev_obj.operate(2)
                if event.key in [K_DOWN, K_s, K_s - 62]:
                    self.lev_obj.operate(3)
                if event.key in [K_LEFT, K_a, K_a - 62]:
                    self.lev_obj.operate(4)
                # 本关卡重置, 组合键(Ctrl + Enter)
                if event.key == K_KP_ENTER or event.key == K_RETURN:
                    self.start_head()
                # 撤销回退一步
                if event.key == K_BACKSPACE:
                    self.undo_one_step()
        else:
            self.next_reset(event)

    # 矩阵转坐标
    def cell_xy(self, row, col):
        """ 矩阵转坐标 """
        add_x = self.center[0] - self.col_num // 2 * self.frame_ele_len
        add_y = self.center[1] - self.row_num // 2 * self.frame_ele_len
        return (col * self.frame_ele_len + add_x, row * self.frame_ele_len + add_y)

    # 坐标转矩阵
    def xy_cell(self, x, y):
        """ 坐标转矩阵 """
        add_x = self.center[0] - self.col_num // 2 * self.frame_ele_len
        add_y = self.center[1] - self.row_num // 2 * self.frame_ele_len
        return (x - add_x / self.frame_ele_len, y - add_y / self.frame_ele_len)

    # 本关重置
    def start_head(self):
        """ 本关重置 """
        self.lev_obj.frame[:] = copy.deepcopy(self.ori_frame) # important
        self.lev_obj.step = 0            # 步数归零
        self.lev_obj.undo_stack.clear()  # 清空撤销回退栈

    # 下一关重置
    def next_reset(self, event = None):
        """ 游戏下一关数据重置 """
        # 绘制下一关提示页面
        if not event:
            Element(Element.good, (0, 0)).draw(self.screen)
        # 下一关页面事件监听
        else:
            if event.type == KEYDOWN:
                # 下一关, 组合键(Ctrl + n)
                if event.key in [K_n, K_n - 62]:
                    self.game_level += 1
                    self.lev_obj.level = self.game_level
                    self.frame = self.lev_obj.frame    # 矩阵元素列表
                    self.next_frame_switch = False
                    self.row_num = len(self.frame)     # 矩阵行数
                    self.col_num = len(self.frame[1])  # 矩阵列数
                    self.ori_frame = copy.deepcopy(self.frame)  # 保存记录本关矩阵元素
                    self.lev_obj.old_frame = copy.deepcopy(self.frame)  # 在移动之前记录关卡矩阵
                    self.font = pygame.font.Font("font/SourceHanSansSC-Bold.otf", 30)
                    self.lev_obj.step = 0              # 步数归零
                    self.lev_obj.undo_stack.clear()    # 清空撤销回退栈

                # 退出, 组合键(Ctrl + q)
                if event.key in [K_q, K_n - 62]:
                    sys.exit()

    # 撤销栈回退一步
    def undo_one_step(self):
        """ 撤销栈回退一步 """
        frame = self.lev_obj.undo_stack.pop()
        if frame:
            self.lev_obj.frame[:] = copy.deepcopy(frame) # important
            self.lev_obj.step -= 1
