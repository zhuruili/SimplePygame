import sys

# 导入pygame以及常量库
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = 640, 480
FPS = 60

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Simple Template")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60, )

running = True
# 主循环
while running:
    # 1. 清屏
    screen.fill((0, 0, 0))
    # 2. 绘制
    pass

    # 事件索取
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # 3. 刷新
    pygame.display.update()
    clock.tick(FPS)


# 循环结束后，退出游戏
pygame.quit()