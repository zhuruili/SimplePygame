import csv
import math
import os
import sys
import time

import pygame
from .button import Button
from conf.settings import *


class Manager:
    """ 游戏管理类 """

    def __init__(self, lev_obj):
        self.dir = os.path.abspath(os.path.dirname(__file__))
        self.clock = pygame.time.Clock()        # 时间管理对象
        self.running = True                     # 游戏运行开关
        self.img_init()                         # 图片初始化
        self.button = Button(self)
        self.lev_obj = lev_obj                  # 游戏等级类对象
        # {0: 终止状态, 1: "运行状态", 2: "暂停状态" }
        self.state = 0                          # 游戏状态
        self.success_switch = False             # 成功页面开关
        self.score_dict = {}                    # 得分字典
        self.high_score_dict = {}               # 最高得分字典

    def img_init(self):
        """ 全局设置 """
        self.image = pygame.image.load(PUZZLE_IMG)
        # 拼接图 Sur
        if self.image.get_width() >= IMG_WIDTH and self.image.get_height() > IMG_WIDTH * 0.5:
            self.game_img = pygame.transform.scale(self.image, \
                            (IMG_WIDTH, math.ceil(self.image.get_height() * (IMG_WIDTH / self.image.get_width()))))
            self.show_img = pygame.transform.scale(self.image, \
                                                   (math.ceil(IMG_WIDTH * 0.4), \
                                                    math.ceil(self.game_img.get_height() * 0.4)))
        else:
            raise("This picture is too small (W > " + str(IMG_WIDTH) + ", H > " + \
                  str(IMG_WIDTH * 0.5) + ")!  Please get me a bigger one .....")
        self.game_rect = self.game_img.get_rect()
        self.show_rect = self.show_img.get_rect()
        self.show_rect.topleft = (10, 100)
        self.game_rect.topleft = (self.show_rect.width + 20, 100)

        # 窗口 Sur
        self.screen_size = (self.game_rect.width + self.show_rect.width + 30, \
                            self.game_rect.height  + 110)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen_rect = self.screen.get_rect()
        # 主界面背景图Sur
        self.background_sur = pygame.image.load(BG_IMG)
        # 等级步数背景图Sur
        self.control_sur = pygame.image.load(CONTROL_IMG)

        # 通关图 Sur
        self.success_sur = pygame.image.load(GOOD_IMG)
        self.success_rec = self.success_sur.get_rect()
        self.success_rec.center = self.screen_rect.center
        # 结束页面背景图Sur
        self.over_sur = pygame.image.load(GRADE_IMG)

    def page_reset(self):
        """ 页面数据重置 """
        self.state = 0               # 设为游游戏为终止状态
        self.success_switch = True   # 打开成功拼图开关
        self.button.start_text = self.button.button_text["stop"]
        self.button.button_bg_color = "yellow"
        self.button.stop_time = pygame.time.get_ticks()
        self.record_grade()          # 记录得分

    # 游戏页面绘制初始化
    def init_page(self):
        """ 游戏页面绘制初始化 """

        # 拼图成功判断
        if not self.success_switch:
            if self.lev_obj.is_success():
                self.page_reset()
        # 绘制背景图
        self.screen.blit(self.background_sur, (0, 0))
        # 绘制等级步数背景图
        self.screen.blit(self.control_sur, (10, self.show_rect.bottom))
        # 绘制标题
        self.draw_text("简  易  拼  图  游  戏", 44, (0, 0, 0), \
                       self.screen_rect.width, 15, True)
        # 绘制参考图
        self.screen.blit(self.show_img, self.show_rect)
        # 绘制矩阵拼图 button_text
        for row, li in enumerate(self.lev_obj.frame):
            for col, val in enumerate(li):
                posi = (col * self.lev_obj.grid_width + self.game_rect[0], \
                        row * self.lev_obj.grid_height + self.game_rect[1])
                if val == -1:
                    if not self.success_switch:
                        pygame.draw.rect(self.screen, (255, 255, 255), \
                                (posi[0], posi[1], self.lev_obj.grid_width, \
                                          self.lev_obj.grid_height))
                    else:
                        self.lev_obj.frame[row][col] = self.lev_obj.blank[0] * \
                                                       self.lev_obj.col_num + \
                                                       self.lev_obj.blank[1]
                sub_row = self.lev_obj.frame[row][col] // self.lev_obj.col_num
                sub_col = self.lev_obj.frame[row][col] % self.lev_obj.col_num
                sub_posi = (sub_col * self.lev_obj.grid_width, sub_row * \
                            self.lev_obj.grid_height, self.lev_obj.grid_width, \
                            self.lev_obj.grid_height)
                self.screen.blit(self.game_img, posi, sub_posi)
        if not self.success_switch:
            # 绘制分隔线_横线
            for i in range(self.lev_obj.row_num + 1):
                start_pos = [self.game_rect[0], self.game_rect[1] + \
                             i * self.lev_obj.grid_height]
                end_pos = [self.game_rect[0] + self.game_rect.width, \
                           self.game_rect[1] + i * self.lev_obj.grid_height]
                pygame.draw.line(self.screen, (0, 0, 0.5), start_pos, end_pos, 1)
            # 绘制分隔线_竖线
            for i in range(self.lev_obj.col_num + 1):
                start_pos = [self.game_rect[0] + i * self.lev_obj.grid_width, \
                             self.game_rect[1]]
                end_pos = [self.game_rect[0] + i * self.lev_obj.grid_width, \
                           self.game_rect[1] +  self.game_rect.height]
                pygame.draw.line(self.screen, (0, 0, 0.5), start_pos, end_pos, 1)
        # 绘制等级
        self.draw_text("等 级：%d"% self.lev_obj.game_level, 26, (255, 255, 255), \
                       self.show_rect.width, self.show_rect.bottom + 32, True)
        # 绘制步数
        self.draw_text("步 数：%d"% self.lev_obj.step, 26, (255, 255, 255), \
                       self.show_rect.width, self.show_rect.bottom + 82, True)
        # 绘制时间
        self.draw_text("时 间：%d s"% round(self.button.running_time // 1000), \
                       26, (255, 255, 255), self.show_rect.width, \
                       self.show_rect.bottom + 132, True)
        pygame.draw.rect(self.screen, (255, 255, 255), \
                    (0, self.screen_rect.bottom - 10, self.screen_rect.width, 10))
        # 绘制按钮
        self.button.draw_button()
        # 绘制成功页面
        if self.success_switch:
            self.success_page()

    # 矩阵事件监听
    def listen_event(self, event):
        """ 事件监听 """
        if not self.success_switch:
            # 矩阵事件监听
            if self.state == 1:
                # 键盘事件
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    """ {上: 1,  右：2, 下：3, 左：4 } """
                    if event.key in [K_UP, K_w, K_w - 62]:
                        self.lev_obj.operate(1)
                    elif event.key in [K_RIGHT, K_d, K_d - 62]:
                        self.lev_obj.operate(2)
                    elif event.key in [K_DOWN, K_s, K_s - 62]:
                        self.lev_obj.operate(3)
                    elif event.key in [K_LEFT, K_a, K_a - 62]:
                        self.lev_obj.operate(4)
                # 鼠标按下事件
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    row = int(mouse_y - self.game_rect[1]) // self.lev_obj.grid_height
                    col = int(mouse_x - self.game_rect[0]) // self.lev_obj.grid_width
                    row_diff = row - self.lev_obj.blank[0]
                    col_diff = col - self.lev_obj.blank[1]
                    if  row_diff == 1 and col_diff == 0:
                        self.lev_obj.operate(1)
                    elif row_diff == -1 and col_diff == 0:
                        self.lev_obj.operate(3)
                    elif row_diff == 0 and col_diff == 1:
                        self.lev_obj.operate(4)
                    elif row_diff == 0 and col_diff == -1:
                        self.lev_obj.operate(2)
            # 按钮事件监听
            self.button.listen_event(event)
        else:
            # 监听成绩页面事件
            self.success_page(event)

    def success_page(self, event = False):
        """ 通关恭喜页面事件监听与绘制 """
        if event:
            if event.type == KEYDOWN:
                # 下一关, 组合键(Ctrl + n)
                if event.key in [K_n, K_n - 62]:
                    if event.mod in [KMOD_LCTRL, KMOD_RCTRL]:
                        self.lev_obj.reset()
                        self.success_switch = False
                # 退出, 进入成绩界面。组合键(Ctrl + q)
                if event.key in [K_q, K_n - 62]:
                    if event.mod in [KMOD_LCTRL, KMOD_RCTRL]:
                        self.show_quit_screen()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if (mouse_x - self.success_rec.left) in range(60, 320):
                    # 下一关
                    if (mouse_y - self.success_rec.top) in range(210, 260):
                        self.lev_obj.reset()
                        self.success_switch = False
                    # 退出
                    if  (mouse_y - self.success_rec.top) in range(260, 310):
                        self.show_quit_screen()
        # 页面绘制
        else:
            # 绘制恭喜通关图
            self.screen.blit(self.success_sur, self.success_rec)

    def draw_text(self, text, size, color, x, y, center = False):
        """ 文本绘制 """
        font = pygame.font.Font(FONT_FILE, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.topleft = (x // 2 - text_rect.width // 2, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def write_data(self, data):
        """ 向文件写入数据 """
        if type(data) != dict:
            raise(" 写入文件数据:", data, "类型不为字典.......")
        file_path = os.path.join(self.dir, "grade.csv")
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for lev, dic in data.items():
                writer.writerow([str(lev), str(dic["time"]), str(dic["step"])])

    def load_data(self):
        """ 加载数据 """
        file_path = os.path.join(self.dir, "grade.csv")
        res = {}
        if not os.path.exists(file_path):
            raise (file_path, "文件不存在， 读取数据失败！")
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for li in list(reader):
                res[int(li[0])] = {}
                res[int(li[0])]["time"] = int(li[1])
                res[int(li[0])]["step"] = int(li[2])
        return res

    def record_grade(self):
        """ 记录得分 """
        self.score_dict[self.lev_obj.game_level] = {}
        self.score_dict[self.lev_obj.game_level]["time"] = self.button.cul_time()
        self.score_dict[self.lev_obj.game_level]["step"] = self.lev_obj.step

    def show_quit_screen(self):
        """ 游戏退出页面 """
        self.screen.fill((54, 59, 64))
        # 绘制背景图
        self.screen.blit(self.over_sur, (0, 0))
        # 读取最高分文件数据
        self.high_score_dict = self.load_data()
        line = 1
        # 只展示最后 8 关的 有游戏数据
        if len(self.score_dict) > 8:
            for i in range(1, len(self.score_dict) - 8 + 1):
                self.score_dict.pop(i)
        # 绘制各关卡游戏数据
        for lev, dic in self.score_dict.items():
            now = dic["time"] * 0.4 + dic["step"] * 0.6
            try:
                ago = self.high_score_dict[lev]["time"] * 0.4 + self.high_score_dict[lev]["step"] * 0.6
            except Exception as e:
                ago = 0
                self.high_score_dict[lev] = {}
                self.high_score_dict[lev]["time"] = dic["time"]
                self.high_score_dict[lev]["step"] = dic["step"]
            time_list = time.ctime(round(dic["time"] / 1000)).split(" ")[4].split(":")
            time_list[0] = str(int(time_list[0]) - 8)
            time_str = ":".join(time_list).center(22)
            # 创造历史
            if now < ago or ago == 0:
                self.draw_text(str(lev).center(26) + time_str + str(dic["step"]).center(22) + "Yes".center(44), \
                               26, (255, 0, 0), 150, 155 + 40 * line)
                # 如果得分出现新记录，保存下来
                if ago != 0:
                    self.high_score_dict[lev]["time"] = dic["time"]
                    self.high_score_dict[lev]["step"] = dic["step"]
            else:
                self.draw_text(str(lev).center(26) + time_str + str(dic["step"]).center(22) + "No".center(44), \
                               26, (0, 0, 0), 150, 155 + 40 * line)
            line += 1
        # 将最好成绩记录文件
        self.write_data(self.high_score_dict)
        self.draw_text("Press a key to play again", 30, (255, 255, 255), self.screen_rect.width, \
                       self.screen_rect.bottom - 60, True)
        pygame.display.update()
        self.wait_for_key()

    def wait_for_key(self):
        """ 程序退出循环 """
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type in [KEYDOWN, QUIT]:
                    waiting = False
                    self.running = False

