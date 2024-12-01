import os

import pygame
from pygame.locals import *
from pygame.math import Vector2

SIZE = WIDTH, HEIGHT = 640, 396
FPS = 60

def draw_text(font, text, color=(255,255,255)):
    """
    绘制文本  
    @param font: 字体对象  
    @param text: 字符串  
    @param color: 颜色  
    在这里用于绘制游戏结束时的GAME OVER字样
    """
    sur = font.render(text, True, color)
    rec = sur.get_rect()
    screen = pygame.display.get_surface() # 获取屏幕对象
    rec.center = screen.get_rect().center
    screen.blit(sur, rec)


pygame.init() # 初始化pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # 窗口居中
screen = pygame.display.set_mode(SIZE) # 设置窗口
pygame.display.set_caption("Bouncing Ball") # 设置标题
clock = pygame.time.Clock() # 设置时钟
font = pygame.font.Font(None, 60) # 设置字体
ball = pygame.image.load("BouncingBall/Assets/ball.png").convert_alpha() # 加载小球图片
ball = pygame.transform.scale(ball, (62, 62)) # 缩放小球图片
ball_pos, ball_w, ball_h = Vector2(100, 0), 62, 62 # 小球位置和大小
speed = Vector2(3, 3)
platform = pygame.Surface((126, 26)) # 创建挡板
platform.fill((0, 0, 0)) # 填充黑色
platform_pos, platform_w, platform_h = Vector2(WIDTH//2, HEIGHT-26), 126, 26 # 挡板位置和大小

# 游戏主循环
while True:
    screen.fill((0, 163, 150)) # 填充背景色

    if pygame.event.peek(QUIT): exit() # 检测队列中是否有退出事件

    keys = pygame.key.get_pressed() # 获取按键状态
    if keys[K_ESCAPE]: exit() # 按下ESC退出

    # 按下左右键移动挡板
    dir = [keys[K_LEFT], keys[K_RIGHT], (-5, 0), (5, 0)]
    for k, v in enumerate(dir[0:2]): # k是索引，v是按键状态
        if v:
            platform_pos += dir[k + 2] # dir[k + 2]其实就是(-5, 0)或(5, 0)
            if platform_pos.x < 0: platform_pos.x = 0 # 到达左边界
            if platform_pos.x + platform_w > WIDTH: platform_pos.x = WIDTH - platform_w # 到达右边界
            break

    # 小球与窗体左、右、上边界碰撞检测
    if ball_pos.x < 0 or ball_pos.x + ball_w > WIDTH:
        speed.x *= -1
    if ball_pos.y < 0:
        speed.y *= -1

    # 小球与窗体底部碰撞检测（即没接住小球，游戏结束）
    if ball_pos.y + ball_h > HEIGHT:
        pygame.event.clear() # 清空事件队列
        draw_text(font, "G A M E   O V E R")
        pygame.display.update() # 更新屏幕
        break # 退出游戏循环

    # 小球与挡板碰撞检测
    elif (ball_pos.x + ball_w // 2) in range(int(platform_pos.x), int(platform_pos.x + platform_w)):
        if ball_pos.y + ball_h >= platform_pos.y:
            speed.y *= -1
            # 防止小球卡在挡板上
            if ball_pos.y + ball_h > platform_pos.y:
                # ball_pos.y = platform_pos.y - ball_h
                speed.y = -abs(speed.y)

    screen.blit(ball, ball_pos) # 绘制小球
    ball_pos += speed # 更新小球位置
    screen.blit(platform, platform_pos) # 绘制挡板

    pygame.display.update() # 更新屏幕
    clock.tick(FPS) # 控制帧率

# 程序结束循环
while True:
    if pygame.event.wait().type in [QUIT, KEYDOWN]:
        exit()
