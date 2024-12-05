import pygame
from conf.settings import *


class Button:

    button_text = {"start": "开始游戏", "stop": "游戏结束", \
                   False: "暂停游戏", True: "继续游戏" }
    # {0: 终止状态, 1: "运行状态", 2: "暂停状态" }

    def __init__(self, manager):
        self.manager = manager
        self.button_bg_switch = False                 # 按钮背景色开关
        self.button_bg_color = "green"                # 按钮背景色
        self.start_text = self.button_text["start"]   # 按钮显示文本
        self.is_down = False                          # 按钮触发开关
        self.start_time =  0                          # 游戏关卡开始时间
        self.delay_time = 0                           # 游戏关卡延迟时间
        self.running_time = 0                         # 游戏关卡运行时间
        self.stop_time = 0                            # 游戏关卡通关时间

    def draw_button(self):
        """ 按钮绘制 """
        if self.manager.state in [1, 2]:
            self.start_text = self.button_text[self.manager.state - 1]
        font = pygame.font.Font(FONT_FILE, 36)
        self.start_font = font.render(self.start_text, True, (0, 0, 0))
        self.start_font_rect = self.start_font.get_rect()
        if self.button_bg_switch:
            self.color_change()
        # 绘制按钮图
        self.button_sur = pygame.image.load("static/img/" + self.button_bg_color + ".png").convert_alpha()
        self.button_rect = self.button_sur.get_rect()
        # 按钮图缩小
        self.button_sur02 = pygame.transform.scale(self.button_sur, \
                            (self.button_rect.width - 6, self.button_rect.height - 3))
        self.button_rect02 = self.button_sur02.get_rect()
        self.button_rect.centerx = self.manager.show_rect.centerx
        self.button_rect.centery = self.manager.screen_rect.bottom - 65
        self.button_rect02.centerx = self.manager.show_rect.centerx
        self.button_rect02.centery = self.manager.screen_rect.bottom - 65 + 3
        if not self.is_down:
            self.manager.screen.blit(self.button_sur, self.button_rect)
        else:
            self.manager.screen.blit(self.button_sur02, self.button_rect02)
        # 绘制文本
        self.manager.screen.blit(self.start_font, \
                                 (self.button_rect.centerx - self.start_font_rect.width // 2, \
                                  self.manager.screen_rect.bottom - 85))

    def listen_event(self, event):
        """ 事件监听 """
        # 键盘按下
        if event.type == KEYDOWN:
            # 强制游戏退出
            if event.key == K_ESCAPE:
                self.manager.running = False
            # 改变按钮状态
            if event.key == K_KP_ENTER or event.key == K_RETURN:
                if event.mod in [KMOD_LCTRL, KMOD_RCTRL]:
                    self.state_change()
                    self.color_change()
            # 退出, 进入成绩界面。组合键(Ctrl + q)
            if event.key in [K_q, K_n - 62]:
                if event.mod in [KMOD_LCTRL, KMOD_RCTRL]:
                    self.manager.show_quit_screen()
        # 鼠标按下
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            # 改变按钮状态
            if self.button_bg_switch:
                self.is_down = True
                self.state_change()
        # 鼠标释放
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if self.button_bg_switch:
                self.is_down = False
        # 鼠标移动事件
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.button_rect.left < mouse_x < self.button_rect.right and \
                    self.button_rect.top < mouse_y < self.button_rect.bottom:
                self.button_bg_switch = True
            else:
                self.button_bg_switch = False

    def state_change(self):
        """ 游戏状态改变 """
        if self.manager.state == 0:  # 终止——>运行
            self.start_time = pygame.time.get_ticks()
            self.manager.state = 1
        elif self.manager.state == 1:  # 运行——>暂停
            self.delay_time = pygame.time.get_ticks()
            self.manager.state = 2
        elif self.manager.state == 2:  # 暂停——>运行
            self.button_bg_color = "gray"
            self.manager.state = 1
            self.start_time += (pygame.time.get_ticks() - self.delay_time)
            self.delay_time = 0

    def color_change(self):
        """ 按钮图片的改变 """
        if self.manager.state == 1:
            self.button_bg_color = "red"
        elif self.manager.state == 2:
            self.button_bg_color = "gray"
        else:
            self.button_bg_color = "green"

    def cul_time(self):
        """ 时间计算 """
        if self.manager.state == 2:
            self.running_time = self.delay_time - self.start_time
        elif self.manager.state == 1:
            self.running_time = pygame.time.get_ticks() - self.start_time
        elif self.manager.state == 0:
            # 在出现拼图成功页面时
            if self.manager.success_switch:
                # 在点击"开始游戏"按钮之后瞬间，游戏就显示了拼图成功页面，
                #    表示此关游戏二维矩阵的打乱拼图操作无效。
                if self.manager.lev_obj.step == 0:
                    self.running_time = 0
                # 正常情况下，通过拼图操作显示了拼图成功页面，但还没点击"下一关"按钮
                else:
                    self.running_time = self.stop_time - self.start_time
            # 在点击了拼图成功页面上的"下一关"按钮之后， 但还没点击"开始游戏"按钮
            else:
                self.running_time = 0
        return self.running_time
