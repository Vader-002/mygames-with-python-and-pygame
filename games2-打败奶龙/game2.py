import pygame
import random
import os
import sys
import json

SAVE_FILE="save.json"

def load_save():
    if not os.path.exists(SAVE_FILE):
        return {"maxscore": 0}
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)


def resource_path(relative_path):

    try:
        # PyInstaller 打包后，资源被解压到 sys._MEIPASS 目录
        base_path = sys._MEIPASS
    except AttributeError:
        # 未打包时，使用当前目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打败奶龙")

clock = pygame.time.Clock()
FPS = 60

Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)
RED = (255, 0, 0)


LINE_LENGTH=12 #准星线长
LINE_WIDTH=3  #准星线宽

mx =WIDTH//2
my =HEIGHT//2
Player_speed=10
#玩家参数


targets_images = []
for i in range(1,3):
    img=pygame.image.load(resource_path(f"pmilklung{i}.png"))
    img=pygame.transform.scale(img, (60,60))
    targets_images.append(img)
targets = []
for i in range(5):
    x=random.randint(0,WIDTH-60)
    y=random.randint(0,HEIGHT-60)
    img=random.choice(targets_images)
    targets.append({"rect":pygame.Rect(x,y,60,60),"img":img})
#敌人参数

score=0
maxscore=0
#计分

FONT_PATH=resource_path("STXIHEI.TTF")
font = pygame.font.Font(FONT_PATH, 30)

hit_sounds=[]
for i in range(1,6):
    sound=pygame.mixer.Sound(resource_path(f"{i}kill.wav"))
    hit_sounds.append(sound)
sound_index=0
game_over_sound=pygame.mixer.Sound(resource_path("gameover.wav"))
#音效

bg_img=pygame.image.load(resource_path("milklungbg.jpg"))
#背景图

level=1
kills=0
targets_kills=10
level_time=30
level_start_ticks=pygame.time.get_ticks()
state="menu"
#游戏状态


save_data=load_save()
oldmaxscore=save_data["maxscore"]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            if state=="menu":
                state="ready"
                level=1
                kills=0
                score=0
                targets_kills=10
                level_time=30
            #主菜单第一关准备的画面
            elif state=="ready":
                state="playing"
                level_start_ticks=pygame.time.get_ticks()
                targets.clear()
                for _ in range(5):
                    x=random.randint(80,WIDTH-100)
                    y=random.randint(50,HEIGHT-100)
                    img=random.choice(targets_images)
                    targets.append({"rect":pygame.Rect(x,y,60,60),"img":img})
            #点击开始
                mx,my = WIDTH//2, HEIGHT//2  #准星剧中



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and state=="game_over":
                state="menu"

            if event.key == pygame.K_j and state=="playing":
                if state=="playing":
                    for t in targets:
                        if t["rect"].collidepoint(mx,my):
                            targets.remove(t)  #移除靶子
                            score+=1  #加分
                            kills+=1
                            hit_sounds[sound_index].play()  #播放击杀音效
                            sound_index=(sound_index+1)%5  #循环

                            new_x=random.randint(80,WIDTH-100)
                            new_y=random.randint(50,HEIGHT-100)
                            new_img=random.choice(targets_images)
                            targets.append({"rect":pygame.Rect(new_x,new_y,60,60),"img":new_img})  #生成新靶子
                            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            if state=="menu":
                state="versioncheck"
            elif state=="versioncheck":
                state="menu"



    if state=="playing":
        keys = pygame.key.get_pressed()  # 获取当前所有按键状态

        # 左移
        if keys[pygame.K_a]:
            mx -= Player_speed
        # 右移
        if keys[pygame.K_d]:
            mx += Player_speed
        # 上移
        if keys[pygame.K_w]:
            my -= Player_speed
        # 下移
        if keys[pygame.K_s]:
            my += Player_speed

        # 边界限制
        if mx < 0:
          mx = 0
        if mx > WIDTH:
          mx = WIDTH
        if my < 0:
           my = 0
        if my > HEIGHT:
           my = HEIGHT
        elaspsed=(pygame.time.get_ticks()-level_start_ticks)//1000
        #已过去时间
        time_left=level_time-elaspsed

        if kills>=targets_kills:
            level+=1
            targets_kills=10+(level-1)*5
            level_time=30+(level-1)*15
            kills=0
            state="ready"
        #检查是否过关并设置下一关目标


        if time_left<=0 and kills<targets_kills :
            if state=="playing":
                game_over_sound.play()
            state="game_over"
            maxscore += score
    if state=="game_over":
        if maxscore>oldmaxscore:
            oldmaxscore=maxscore
            save_data["maxscore"]=oldmaxscore
        save_game(save_data)


    screen.blit(bg_img,(0,0))

    if state=="menu":
        title_font=pygame.font.Font(FONT_PATH,72)
        title_text=title_font.render("打败奶龙",True,White)
        title_rect=title_text.get_rect(center=(WIDTH//2,HEIGHT//3))
        screen.blit(title_text,title_rect)

        hint_font=pygame.font.Font(FONT_PATH,20)
        hint_text=hint_font.render("点击J开始",True,White)
        hint_rect=hint_text.get_rect(center=(WIDTH//2,HEIGHT//2))
        screen.blit(hint_text,hint_rect)

        check_font=pygame.font.Font(FONT_PATH,20)
        check_text=check_font.render("点击v查看历史版本更新记录",True,White)
        check_rect=check_text.get_rect(center=(WIDTH//2,HEIGHT//2+20))
        screen.blit(check_text,check_rect)
    elif state=="ready":
        ready_font=pygame.font.Font(FONT_PATH,48)
        level_text=ready_font.render(f"第{level}关",True,White)
        level_rect=level_text.get_rect(center=(WIDTH//2,HEIGHT//3))
        screen.blit(level_text,level_rect)

        info_font=pygame.font.Font(FONT_PATH,20)
        detail_text=info_font.render(f"目标击杀：{targets_kills}  时间：{level_time}秒",True,White)
        detail_rect=detail_text.get_rect(center=(WIDTH//2,HEIGHT//3+60))
        screen.blit(detail_text,detail_rect)

        click_font=pygame.font.Font(FONT_PATH,20)
        click_text=click_font.render("点击J开始",True,White)
        click_rect=click_text.get_rect(center=(WIDTH//2,HEIGHT//2+60))
        screen.blit(click_text,click_rect)
    elif state=="playing":
        for t in targets:
            screen.blit(t["img"],t["rect"])

        pygame.draw.line(screen, Green, (mx, my + 10), (mx, my - 10), LINE_WIDTH)
        pygame.draw.line(screen, Green, (mx + 10, my), (mx - 10, my), LINE_WIDTH)
        pygame.draw.circle(screen, RED, (mx, my), 3)

        elaspsed=(pygame.time.get_ticks()-level_start_ticks)//1000
        time_left=level_time-elaspsed
        info_text=font.render(f"目前在{level}关, 本关击杀了{kills}个奶龙  剩余：{time_left}秒",True,White)
        screen.blit(info_text,(10,10))
    elif state=="game_over":
        pygame.draw.line(screen, Green, (mx, my + 10), (mx, my), LINE_WIDTH)
        pygame.draw.line(screen, Green, (mx + 10, my), (mx, my), LINE_WIDTH)
        pygame.draw.circle(screen, RED, (mx, my), 3)

        over_font=pygame.font.Font(FONT_PATH,45)
        over_text=over_font.render(f"游戏结束！到达了第{level}关,在本关击杀了{kills}个奶龙,",True,White)
        over_rect=over_text.get_rect(center=(WIDTH//2,HEIGHT//2-30))
        screen.blit(over_text,over_rect)

        allkills_font=pygame.font.Font(FONT_PATH,45)
        allkills_text=allkills_font.render(f"总共击杀了{score}只奶龙,历史最好记录击杀了{oldmaxscore}只奶龙",True,RED)
        allkills_rect=allkills_text.get_rect(center=(WIDTH//2,HEIGHT//2+20))
        screen.blit(allkills_text,allkills_rect)

        restart_font=pygame.font.Font(FONT_PATH,20)
        restat_text=restart_font.render("按R返回主菜单",True,White)
        restart_rect=restat_text.get_rect(center=(WIDTH//2,HEIGHT//2+50))
        screen.blit(restat_text,restart_rect)
    elif state=="versioncheck":
        version1_font=pygame.font.Font(FONT_PATH,20)
        version1_text=version1_font.render(f"0.8.1更新",True,White)
        version1_rect=version1_text.get_rect(center=(WIDTH//2,HEIGHT//2-400))
        screen.blit(version1_text,version1_rect)
        version11_font=pygame.font.Font(FONT_PATH,20)
        version11_text=version11_font.render(f"支持历史版本更新查询和本地记录保存",True,White)
        version11_rect=version11_text.get_rect(center=(WIDTH//2,HEIGHT//2-370))
        screen.blit(version11_text,version11_rect)

        getback_font=pygame.font.Font(FONT_PATH,20)
        getback_text=getback_font.render("点击v返回主菜单",True,White)
        getback_rect=getback_text.get_rect(center=(WIDTH//2+500,HEIGHT//2-380))
        screen.blit(getback_text,getback_rect)


    maker_font=pygame.font.Font(FONT_PATH,15)
    maker_text=maker_font.render(f"Made by Vader with pygame",True,Green)
    maker_rect=maker_text.get_rect(center=(1090,25))
    screen.blit(maker_text,maker_rect)

    gametitle_font=pygame.font.Font(FONT_PATH,15)
    gametitle_text=gametitle_font.render(f"version 0.8.1,made on 2026.5.15",True,Green)
    gametitle_rect=gametitle_text.get_rect(center=(1090,40))
    screen.blit(gametitle_text,gametitle_rect)

    testlocationa_font=pygame.font.Font(FONT_PATH,50)
    testlocationa_text=testlocationa_font.render(f"",True,RED)
    testlocationa_rect=testlocationa_text.get_rect(center=(WIDTH-100,HEIGHT-100))
    screen.blit(testlocationa_text,testlocationa_rect)

    testlocationb_font = pygame.font.Font(FONT_PATH, 15)
    testlocationb_text = testlocationb_font.render(f"", True, RED)
    testlocationb_rect = testlocationb_text.get_rect(center=(WIDTH - 100, HEIGHT - 50))
    screen.blit(testlocationb_text, testlocationb_rect)
    #测试调整位置用，打包之前注意把这两行的内容清空


    pygame.display.flip()


    clock.tick(FPS)
