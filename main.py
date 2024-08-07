from Engine import Engine,Label,ImageLoader,Images,Wall,Player,Bullet,Enemy,Weapon
import pygame
import random as r
import json


with open("config.json","r",encoding="UTF-8") as f:
    data=json.load(f)



WIDTH=1280
HEIGH=720
kolvo_enemys=data['kolvo_enemys']
kolvo_bullets_player=data['kolvo_bullets_player']
kolvo_bullets_enemys=data['kolvo_bullets_enemys']
otdacha_enemy=data['otdacha_enemy']
speed_enemys=data['speed_enemys']
speed_player=data['speed_player']
enemys_speed_shoot=data['enemys_speed_shoot']
FPS=data['FPS_MAX']


eng = Engine()
img_loader=ImageLoader() 
player=Player((200,340),90,80)


phone=Images(img_loader.load("phone2.png",colorkey=[True,(0,0,0)],scale=(1,1)),isphone=True,speed=-1.7,width=1280)
phone2=Images(img_loader.load("phone2.png",colorkey=[True,(0,0,0)],scale=(1,1)),isphone=True,pos=(WIDTH+5,0),speed=-1.7,width=1280)
hero=img_loader.load("hero.png",colorkey=[True,(255,255,255)])
                     
fps=Label(0,0,120,40)
cords=Label(130,0,320,40)
hp=Label(500,0,320,40)
enemyss=Label(700,0,200,40)
bulets_rightnow=Label(900,0,250,40)

walls=[Wall((-1,0),1,HEIGH),
    Wall((WIDTH,0),1,HEIGH),
    Wall((0,-1),WIDTH,1),
    Wall((0,HEIGH),WIDTH,1)]

enemy_texures=[img_loader.load("enemy1.png",colorkey=[True,(255,255,255)]),img_loader.load("enemy2.png",colorkey=[True,(255,255,255)])]
bullet_texture=img_loader.load("bullet.png")
bullet_texture_enemy=img_loader.load("bullet_enemy1.png",colorkey=[True,(255,255,255)])

enemys=[Enemy((1000,r.randint(100,700)),140,110,enemy_texures[0],125,800) for i in range(kolvo_enemys)]
#enemys=[Enemy((1000,r.randint(100,700)),140,110,enemy_texures[0],125),Enemy((1000,r.randint(100,700)),170,90,enemy_texture2,125)]

player.speed=speed_player


def pistol_traek(x):
    return x*0.0017


pistol=Weapon(damage=10,vectorx=1,shoot_parms=(10,150),start_spread=(-2,2),permanent_spread=(0,0),trajectory=pistol_traek)
automat=Weapon(damage=5,vectorx=1,shoot_parms=(40,150),start_spread=(-3,3),permanent_spread=(-4,1))


pistol_bullets=[Bullet(bullet_texture,4,3,1,r.randint(9,12),True) for i in range(10)]
automat_bullets=[Bullet(bullet_texture,12,5,3,r.randint(16,18),True) for i in range(45)]


pistol.load_bullets(pistol_bullets,eng)
automat.load_bullets(automat_bullets,eng)



player.get_weapon(pistol)
player.get_weapon(automat)

for enem in enemys:
    pistol_enmy=Weapon(damage=5,vectorx=-1,shoot_parms=(10,150),start_spread=(-2,2),permanent_spread=(-6,6))
    pistol_bullets_enemy=[Bullet(bullet_texture_enemy,30,21,1,r.randint(8,11),False) for i in range(10)]
    pistol_enmy.load_bullets(pistol_bullets_enemy,eng)
    enem.get_weapon(pistol_enmy)

player.set_texture(hero)
eng.set_frame(FPS)
eng.set_res((WIDTH,HEIGH))


[eng.add_objects(i) for i in walls]
eng.add_objects(player)
eng.add_objects(phone)
eng.add_objects(phone2)
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

