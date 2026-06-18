import ctypes
import pygame
import sys
import os
import time
import random
import json

def switch_ime_to_english():
    """模拟按一次 Shift，让中文输入法切换到英文模式"""
    try:
        # 获取 Pygame 窗口句柄
        hwnd = pygame.display.get_wm_info()['window']
        # 将窗口设为前台，确保模拟按键发送到游戏窗口
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.05)  # 等一下窗口获取焦点
        # 模拟按下 Shift
        ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)  # 0x10 是 Shift 的虚拟键码
        # 模拟释放 Shift
        ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)  # 2 表示释放
    except:
        pass

SAVE_FILE = "snake_save.json"

def load_save():
    if not os.path.exists(SAVE_FILE):
        return {"maxscore": 0}
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_game(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)






def resource_path(relative_path):

    try:
        # PyInstaller 打包后，资源被解压到 sys._MEIPASS 目录
        base_path = sys._MEIPASS
    except AttributeError:
        # 未打包时，使用当前目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()


WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")
switch_ime_to_english()
rangerect=pygame.Rect(0,0,1000,700)
rangerect.center=(WIDTH/2,HEIGHT/2)



clock = pygame.time.Clock()
FPS = 60

FONT_PATH=resource_path("STXIHEI.TTF")
font = pygame.font.Font(FONT_PATH, 30)

snack_head_x=WIDTH/2
snack_head_y=HEIGHT/2
snack_body_sise=10
snack_body_rect=pygame.Rect(0,0,snack_body_sise,snack_body_sise)

snack_head_rect=pygame.Rect(0,0,snack_body_sise,snack_body_sise)
snack_head_rect.center=(snack_head_x,snack_head_y)
snack_eye_rect=pygame.Rect(0,0,3,3)
snack_eye_rect.center=(snack_head_x+2,snack_head_y-2)
snack_moutha_rect=pygame.Rect(0,0,5,5)
snack_moutha_rect.center=(snack_head_x+3,snack_head_y+3)
snack_body_position=[(snack_head_x,snack_head_y)]
speed=3
direction="none"
snack_length=5


fruits=[]
fruits_sise=15  #注意这是直径
fruits_value=3


score=0
maxscore=0












Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)
Red = (255, 0, 0)

state = "menu"
gameover = False
self_collision_enabled = False   # 是否启用自碰检测
move_start_ticks = 0             # 第一次移动的开始时刻（毫秒）






save_data = load_save()
maxscore = save_data["maxscore"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            if state=="menu":
                state="ready"
            elif state=="ready":
                state="playing"

        if state=="playing" and event.type==pygame.KEYDOWN and event.key==pygame.K_a and not direction=="right":
            direction="left"
        elif state=="playing" and event.type==pygame.KEYDOWN and event.key==pygame.K_d and not direction=="left":
            direction="right"
        elif state=="playing" and event.type==pygame.KEYDOWN and event.key==pygame.K_w and not direction=="down":
            direction="up"
        elif state=="playing" and event.type==pygame.KEYDOWN and event.key==pygame.K_s and not direction=="up":
            direction="down"

        if state =="playing" and event.type==pygame.KEYDOWN and not event.key==pygame.K_k:
            if event.key==pygame.K_j:speed=6
        if state =="playing" and event.type==pygame.KEYDOWN and not event.key==pygame.K_j:
            if event.key==pygame.K_k:speed=2

        if state=="playing" and event.type==pygame.KEYUP and not event.key==pygame.K_k:
            if event.key==pygame.K_j:speed=3
        if state=="playing" and event.type==pygame.KEYUP and not event.key==pygame.K_j:
            if event.key==pygame.K_k:speed=3

        if event.type==pygame.KEYDOWN and state=="gameover" and event.key==pygame.K_r:
            snack_head_x=WIDTH/2
            snack_head_y=HEIGHT/2
            snack_body_position = [(snack_head_x, snack_head_y)]
            snack_length = 5
            direction="none"
            state="menu"
            snack_head_rect.center=(snack_head_x,snack_head_y)
            snack_eye_rect.center=(snack_head_x+2,snack_head_y-2)
            snack_moutha_rect.center=(snack_head_x+3,snack_head_y+3)
            fruits.clear()














    screen.fill(Black)  # 清屏

    if state == "playing":
        prev_head_pos=snack_head_rect.center


        if direction=="left":
            snack_head_x-=speed
        elif direction=="right":
            snack_head_x+=speed
        elif direction=="up":
            snack_head_y-=speed
        elif direction=="down":
            snack_head_y+=speed


        if snack_head_x>WIDTH-107:
            snack_head_x=WIDTH-107
            state="gameover"
        if snack_head_x<105:
            snack_head_x=105
            state="gameover"
        if snack_head_y>HEIGHT-107:
            snack_head_y=HEIGHT-107
            state="gameover"
        if snack_head_y<107:
            snack_head_y=107
            state="gameover"

        snack_head_rect.center=(snack_head_x,snack_head_y)

        if len(snack_body_position)>5:
            for pos in snack_body_position[4:]:
                body_rect = pygame.Rect(0, 0, snack_body_sise, snack_body_sise)
                body_rect.center = pos
                if snack_eye_rect.colliderect(body_rect) and snack_moutha_rect.colliderect(body_rect):
                    state = "gameover"
                    break

        if direction != "none":  # 只有蛇确实在移动时，才更新身体长度
            snack_body_position.insert(0, prev_head_pos)
            while len(snack_body_position) > snack_length:
                snack_body_position.pop()










        snack_head_rect.center = (snack_head_x, snack_head_y)
        if direction=="right":
            snack_eye_rect.center = (snack_head_x + 2, snack_head_y - 2)
            snack_moutha_rect.center = (snack_head_x + 3, snack_head_y + 3)
        elif direction=="left":
            snack_eye_rect.center=(snack_head_x - 2, snack_head_y - 2)
            snack_moutha_rect.center=(snack_head_x - 3, snack_head_y + 3)
        elif direction=="up":
            snack_eye_rect.center = (snack_head_x + 2, snack_head_y - 2)
            snack_moutha_rect.center = (snack_head_x - 3, snack_head_y - 3)
        elif direction=="down":
            snack_eye_rect.center = (snack_head_x + 2, snack_head_y + 2)
            snack_moutha_rect.center = (snack_head_x - 3, snack_head_y + 3)

        for pos in snack_body_position[1:]:
            segement_rect=pygame.Rect(0,0,snack_body_sise,snack_body_sise)
            segement_rect.center=pos
            pygame.draw.rect(screen,White,segement_rect)

        if len(fruits) == 0:
            xfruits = random.randint(1, 3)
            for _ in range(1, xfruits + 1):
                fruit_x = random.randint(105, WIDTH - 107)
                fruit_y = random.randint(107, HEIGHT - 107)
                fruit_rect = pygame.Rect(0,0, fruits_sise, fruits_sise)
                fruit_rect.center=(fruit_x,fruit_y)
                fruits.append({"rect": fruit_rect})

        for t in fruits:
            if t['rect'].colliderect(snack_head_rect):
                fruits.remove(t)
                if speed==3:score+=1
                elif speed==2:score+=0.5
                elif speed==6:score+=2
                snack_length+=5





        pygame.draw.rect(screen,White,snack_head_rect)
        pygame.draw.rect(screen,Black,snack_moutha_rect)
        pygame.draw.rect(screen,Red,snack_eye_rect)
        for t in fruits:
            pygame.draw.rect(screen,White,t['rect'])


        scores_font = pygame.font.Font(FONT_PATH,25)
        scores_text = scores_font.render("得分："+str(score), True, White)
        scores_text_rect = scores_text.get_rect(center=(60,30))
        screen.blit(scores_text,scores_text_rect)

        maxscore_font = pygame.font.Font(FONT_PATH,25)
        maxscore_text=maxscore_font.render("最高得分："+str(maxscore), True, White)
        maxscore_text_rect = maxscore_text.get_rect(center=(85,55))
        screen.blit(maxscore_text,maxscore_text_rect)

        tips1_font = pygame.font.Font(FONT_PATH,25)
        tips1_text=tips1_font.render("按住J加速得分且翻倍，按住K减速但得分减半",True,White)
        tips1_text_rect = tips1_text.get_rect(center=(WIDTH//2,55))
        screen.blit(tips1_text,tips1_text_rect)

    if state=="gameover":

        if score > maxscore:
            maxscore = score
            save_data["maxscore"] = maxscore
            save_game(save_data)

        over_font=pygame.font.Font(FONT_PATH,20)
        text = over_font.render("游戏结束！按R重新开始", True, Green)
        # 显示
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        scores_font = pygame.font.Font(FONT_PATH, 25)
        final_text = scores_font.render("本局得分：" + str(score), True, White)
        final_rect = final_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(final_text, final_rect)

        maxscore_text = scores_font.render("最高得分：" + str(maxscore), True, White)
        maxscore_rect = maxscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        screen.blit(maxscore_text, maxscore_rect)

        for pos in snack_body_position[1:]:
            segement_rect=pygame.Rect(0,0,snack_body_sise,snack_body_sise)
            segement_rect.center=pos
            pygame.draw.rect(screen,White,segement_rect)

        for t in fruits:
            pygame.draw.rect(screen, White, t["rect"])




        pygame.draw.rect(screen,White,snack_head_rect)
        pygame.draw.rect(screen,Black,snack_moutha_rect)
        pygame.draw.rect(screen,Red,snack_eye_rect)







    if state=="menu":
        menu1_font=pygame.font.Font(FONT_PATH,40)
        menu1_text=menu1_font.render("贪吃蛇",True,Green)
        menu1_rect=menu1_text.get_rect(center=(WIDTH/2,HEIGHT/2-100))
        screen.blit(menu1_text,menu1_rect)

        menu2_font=pygame.font.Font(FONT_PATH,20)
        menu2_text=menu2_font.render("点击J准备",True,Green)
        menu2_rect=menu2_text.get_rect(center=(WIDTH/2,HEIGHT/2-60))
        screen.blit(menu2_text,menu2_rect)

    if state=="ready":
        score=0


        menu2_font=pygame.font.Font(FONT_PATH,28)
        menu2_text=menu2_font.render("准备好了吗？按J进入游戏",True,Green)
        menu2_rect=menu2_text.get_rect(center=(WIDTH/2,HEIGHT/2-100))
        screen.blit(menu2_text,menu2_rect)






    pygame.draw.rect(screen,White,rangerect,1)





    maker_font=pygame.font.Font(FONT_PATH,15)
    maker_text=maker_font.render(f"Made by Vader with pygame",True,Green)
    maker_rect=maker_text.get_rect(center=(1090,25))
    screen.blit(maker_text,maker_rect)

    version_font=pygame.font.Font(FONT_PATH,15)
    version_text=version_font.render("Version 1.0",True,Green)
    version_rect=version_text.get_rect(center=(1150,55))
    screen.blit(version_text,version_rect)

    pygame.display.flip()       # 翻页显示

    clock.tick(FPS)             # 控制帧率