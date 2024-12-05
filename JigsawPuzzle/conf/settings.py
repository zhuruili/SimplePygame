from pygame.locals import * # 导入 Pygame 常量库

FPS = 60                  # 帧率
TITLE = "jigsaw puzzle"
INIT_ROW_NUM = 3          # 初始矩阵行数
INIT_COL_NUM = 3          # 初始矩阵列数
# 设置游戏难度系数
AUTO_RUN_STEP = 3000        # 自动移动步数
# 方向键常量
UP, RIGHT, BOTTOM, LEFT = 1, 2, 3, 4

# 游戏所要拼接的图片
PUZZLE_IMG = "static/img/game.png"
# 恭喜通关所要显示的图片
GOOD_IMG = "static/img/good.png"
# 主界面背景图片
BG_IMG = "static/img/bg.png"
# 结束页面背景图片
GRADE_IMG = "static/img/grade.png"
# 等级步数背景图片
CONTROL_IMG = "static/img/control.png"

# 游戏字体文件
FONT_FILE = "static/font/SourceHanSansSC-Bold.otf"

# 拼接图片的宽度,也为原始拼接图片的最小宽度
IMG_WIDTH = 700
# 背景颜色
BG_COLOR = (239, 239, 239)

