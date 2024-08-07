from Engine import Engine,Label,ImageLoader,Images,Wall,Player,Bullet,Enemy
import pygame
import random as r
from math import sin


WIDTH=1280
HEIGH=720


img_loader=ImageLoader()   
eng = Engine()
fps=Label(0,0,120,40)
cords=Label(130,0,320,40)
hp=Label(500,0,320,40)
enemyss=Label(700,0,200,40)
bulets_rightnow=Label(900,0,250,40)
walls=[Wall((-1,0),1,HEIGH),
    Wall((WIDTH,0),1,HEIGH),
    Wall((0,-1),WIDTH,1),
    Wall((0,HEIGH),WIDTH,1)]
enemy_texture1=img_loader.load("enemy1.png",colorkey=[True,(255,255,255)])
enemy_texture2=img_loader.load("enemy2.png",colorkey=[True,(255,255,255)])
bullet_texture=img_loader.load("bullet.png")
bullet_texture_enemy=img_loader.load("bullet_enemy1.png",colorkey=[True,(255,255,255)])
player=Player((200,340),90,80)
#enemys=[Enemy((1000,r.randint(100,700)),140,110,enemy_texture1,125),Enemy((1000,r.randint(100,700)),170,90,enemy_texture2,125)]
enemys=[Enemy((1000,r.randint(100,700)),140,110,enemy_texture1,125) for i in range(100)]
player.speed=10
phone=Images(img_loader.load("phone2.png",colorkey=[True,(0,0,0)],scale=(0.9,1)))
hero=img_loader.load("hero.png",colorkey=[True,(255,255,255)])
bulets_player=[]
bulets_enemys=[]
for i in range(60):
    tmp=Bullet(width=6,height=3,speed=r.randint(18,37),texure_bullet=bullet_texture,damage=r.randint(2,4))
    tmp.player=True
    bulets_player.append(tmp)

for i in enemys:
    for j in range(15):
        tmp=Bullet(width=30,height=21,speed=r.randint(9,12),texure_bullet=bullet_texture,damage=r.randint(10,12))
        tmp.set_texture(bullet_texture_enemy)
        tmp.player=False
        bulets_enemys.append(tmp)
    i.add_bullets(bulets_enemys,eng)
    i.speed=2
    i.otdacha=2
    i.infbullets=True
    i.set_shoot_parms(30,170)
    bulets_enemys=[]

player.infbullets=True
player.add_bullets(bulets_player,eng)
player.set_shoot_parms(45,150)
# for i in range(5000):
#             tmp=Bullet(speed=r.randint(18,37),texure_bullet=bullet_texture,damage=r.randint(1,3))
#             eng.add_objects(tmp)


        
player.set_texture(hero)
eng.set_frame(61)
eng.set_res((WIDTH,HEIGH))


[eng.add_objects(i) for i in walls]
eng.add_objects(player)
eng.add_objects(phone)
[eng.add_objects(i) for i in enemys]



def sh():
    fps.show(eng.display,text=f"FPS - {int(eng.fps_now)}",isbackground=False)
    cords.show(eng.display,text=f"xy({player.x} {player.y})",isbackground=False)
    hp.show(eng.display,text=f"hp: {player.hp}",isbackground=False)
    enemyss.show(eng.display,text=f"enemys: {len(eng.objects["enemys"])}",isbackground=False)
    buls=len([i for i in eng.objects["bullets"] if i.isdraw])
    bulets_rightnow.show(eng.display,text=f"bullets: {buls}",isbackground=False)


    
        
        
eng.addCustomFunc("labelScroe",sh,True)


# left_button = Button(30, 660, 70, 40, text="Left",
#                      function=lambda: print("left"))
# right_button = Button(1200, 660, 70, 40, text="Right",a
#                       function=lambda: print("right"))

eng.run(showColision=0)

