import sys
# 导入pygame 及常量库
import pygame
from conf.settings import *

from core.handler import Manager
from core.level import Level


# 主函数
def main():

    # 标题
    title = TITLE
    # 颜色定义
    bg_color = BG_COLOR

    # 初始化
    pygame.init()
    # 创建管理时间对象
    clock = pygame.time.Clock()

    # 实例化游戏管理类对象
    level = Level()
    manager = Manager(level)
    level.frame_init(manager)

    # 屏幕尺寸（宽， 高）
    __screen_size = WIDTH, HEIGHT =  manager.screen_size
    # 创建游戏窗口
    screen = pygame.display.set_mode(__screen_size)
    # 设置窗口标题
    pygame.display.set_caption(title)
    # 创建字体对象
    font = pygame.font.Font(FONT_FILE, 26)

    # 程序运行主体死循环
    while manager.running:
        # 1. 清屏(窗口纯背景色画纸的绘制)
        screen.fill(bg_color)  # 先准备一块深灰色布
        # 2. 绘制
        manager.init_page()
        for event in pygame.event.get():  # 事件索取
            if event.type == QUIT:  # 判断点击窗口右上角“X”
                pygame.quit()       # 还原设备
                sys.exit()          # 程序退出

            # 监听游戏页面事件
            manager.listen_event(event)
        manager.button.cul_time()  # 计算时间
        # 3.刷新
        pygame.display.update()
        # 设置帧数
        clock.tick(FPS)
    # 循环结束后，退出游戏
    pygame.quit()

