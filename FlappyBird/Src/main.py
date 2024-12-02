import sys
import random

import pygame

class Bird(object):
    """Class representing the bird."""
    def __init__(self):
        """初始化"""
        self.birdRect = pygame.Rect(65, 50, 50, 50) # 鸟的矩形
        # 鸟的三种状态
        self.birdStatus = [pygame.image.load("FlappyBird\Assets\\0.png"),
                           pygame.image.load("FlappyBird\Assets\\1.png"),
                           pygame.image.load("FlappyBird\Assets\\dead.png")]
        self.status = 0 # 默认飞行状态
        self.birdX = 180
        self.birdY = 150
        self.jump = False # 默认是往下掉的
        self.jumpSpeed = 12 # 跳跃
        self.gravity = 3.5 # 重力
        self.dead = False # 活的

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1 # 速度递减，上升越来越慢
            if self.jumpSpeed < 0:
                self.jump = False
            self.birdY -= self.jumpSpeed # 鸟的Y坐标减小，鸟上升
        else:
            if self.gravity < 7:
                self.gravity += 0.2
            self.birdY += self.gravity
        
        self.birdRect[1] = self.birdY # 更新鸟的位置
        

class Pipeline(object):
    """Class representing a pipeline."""
    def __init__(self):
        """初始化"""
        self.wallx = 650 # 管道初始位置
        self.pineUp = pygame.image.load("FlappyBird\Assets\\top.png") # 加载上管道
        self.pineDown = pygame.image.load("FlappyBird\Assets\\bottom.png")

    def pipelineUpdate(self):
        self.wallx -= 5 # 管道向左移动
        if self.wallx < -80:
            global score
            score += 1
            self.wallx = 650


def createMap():
    """创建地图"""
    screen.fill((255,255,255)) # 定义该函数时虽然未定义screen，但是在程序调用该函数时已经在全局作用域定义了screen所以不会报错
    screen.blit(background, (0, 0))

    # 绘制管道
    screen.blit(pipeline.pineUp, (pipeline.wallx, -320))
    screen.blit(pipeline.pineDown, (pipeline.wallx, 350))
    pipeline.pipelineUpdate() # 管道移动

    # 绘制小鸟
    if bird.dead:
        bird.status = 2
    elif bird.jump:
        bird.status = 1
    screen.blit(bird.birdStatus[bird.status], (bird.birdX, bird.birdY))
    bird.birdUpdate() # 鸟移动

    # 显示分数
    screen.blit(font.render('Score: ' + str(score), -1, (255, 255, 255)), (100, 50))

    pygame.display.update()

def checkDead():
    """检测小鸟是否死亡"""
    # 判断小鸟是否碰到地面
    if bird.birdRect[1] == 920:
        bird.dead = True
    # 判断小鸟是否撞到管道
    upRect = pygame.Rect(pipeline.wallx-98, -320, 98, 495)  # 这两行的参数设置有BUG，但是不影响游戏整体逻辑
    downRect = pygame.Rect(pipeline.wallx-98, 350, 98, 495)
    if upRect.colliderect(bird.birdRect) or downRect.colliderect(bird.birdRect):
        bird.dead = True
    return bird.dead

def getResult():
    """如果游戏结束"""
    final_text1 = "Game Over"
    final_text2 = "Your final score is:  " + str(score)
    ft1_font = pygame.font.SysFont(None, 70)
    ft1_surf = font.render(final_text1, 1, (242, 3, 36))
    ft2_font = pygame.font.SysFont(None, 50)
    ft2_surf = font.render(final_text2, 1, (253, 177, 6))

    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])
    screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])

    pygame.display.flip()


if __name__ == '__main__':
    """主程序"""
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont(None, 50)
    size = width, height = 1916*0.5,920*0.5
    screen = pygame.display.set_mode(size=size)
    clock = pygame.time.Clock()
    FPS = 60

    pipeline = Pipeline()
    bird = Bird()

    score = 0 # 得分

    # 主循环
    while True:
        clock.tick(FPS)
        # 轮询事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not bird.dead:
                bird.jump = True # 按键盘或者鼠标点击时，小鸟往上飞
                bird.gravity = 3.5
                bird.jumpSpeed = 12 # 每次触发跳跃将跳跃速度恢复到12，不然会继承之前衰减过的速度

        background = pygame.image.load("FlappyBird\Assets\\background.jpg") # 加载背景图片
        background = pygame.transform.scale(background,(1916*0.5,920*0.5))

        if checkDead():
            getResult() # 游戏结束
        else:
            createMap() # 绘制地图

    pygame.quit()