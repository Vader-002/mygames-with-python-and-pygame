import pygame
import sys
import random

def resource_path(relative_path):
    """获取资源的绝对路径，兼容打包后的 exe"""
    try:
        # PyInstaller 打包后，临时解压目录存储在 sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # 未打包时，使用当前目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
FONT_PATH = resource_path("STXIHEI.TTF")

pygame.init()

clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600  #定义长宽
screen = pygame.display.set_mode((WIDTH,HEIGHT))  #窗口大小
pygame.display.set_caption("躲方块")  #窗口标题

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS=[
    (255,0,0),  #红
    (0,255,0),  #绿
    (0,0,255),  #蓝
    (255,255,0),  #黄
    (255,0,255),  #紫
    (0,255,255)  #青
]
#颜色库

player = pygame.Rect(
    WIDTH // 2 - 40,   # x：居中
    HEIGHT - 60,       # y：靠近底部
    80,                # 宽
    20                 # 高
)
PLAYER_SPEED = 8
#玩家

enemies=[]  #敌人群列表
ENEMY_SIZE = 40
ENEMY_SPEED= 2
SPAWN_ENEMY=pygame.USEREVENT+1  #生成敌人
pygame.time.set_timer(SPAWN_ENEMY,1000)  #800ms生成一个敌人
#敌人群

score=0
maxscore=0
#分数

game_over = False

over_font=pygame.font.Font(FONT_PATH, 36)
font = pygame.font.Font(FONT_PATH, 36)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                player.centerx=WIDTH//2  #重置玩家位置
                enemies.clear()
                if score>maxscore:
                    maxscore=score
                score=0
                #清除所有敌人
                game_over = False
                #游戏结束状态消除
        if event.type == SPAWN_ENEMY and not game_over:
            x=random.randint(0, WIDTH-ENEMY_SIZE)
            enemy_rect=pygame.Rect(x,-ENEMY_SIZE,ENEMY_SIZE,ENEMY_SIZE)
            enemy_color=random.choice(COLORS)
            enemies.append({"rect":enemy_rect,"color":enemy_color})
            #定时生成敌人
    if not game_over:

        keys = pygame.key.get_pressed()  # 获取当前所有按键状态

        # 左移
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        # 右移
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
        #上移
        if keys[pygame.K_UP]:
            player.y -= PLAYER_SPEED
        #下移
        if keys[pygame.K_DOWN]:
            player.y += PLAYER_SPEED


        #边界限制
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
        if player.top < 0:
            player.top=0
        if player.bottom > HEIGHT:
            player.bottom=HEIGHT


        for enemy in enemies[:]:
            enemy["rect"].y+=ENEMY_SIZE
            if enemy["rect"].top>HEIGHT:
                enemies.remove(enemy)
                score+=1
            #敌人掉出屏幕后处理

            if enemy["rect"].colliderect(player):
                game_over = True  #检测碰撞


    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    for enemy in enemies:
        pygame.draw.rect(screen,enemy["color"],enemy["rect"])
    score_text = font.render(f"分数：{score}", True, WHITE)
    maxscore_text = font.render(f"最高分数：{maxscore}", True, WHITE)
    screen.blit(score_text, (10, 50))
    screen.blit(maxscore_text, (10, 10))
        #绘制分数
    if game_over:
        text = over_font.render("游戏结束！按R重新开始", True, WHITE)
        #显示
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        #文字居中
    #绘制

    pygame.display.flip()

    clock.tick(60)







