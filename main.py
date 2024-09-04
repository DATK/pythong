from Engine.Engine import Engine,Button,Label,ImageLoader,Image,Wall,Player,Bullet,Enemy,Weapon,Box,Buf
import random as r
import json


with open("config.json","r",encoding="UTF-8") as f:
    data=json.load(f)



WIDTH=720
HEIGH=1280
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
boxHP=Box(pos=(700,500),player=player,height=100,width=120,hp=0)
boxSheild=Box(pos=(700,500),player=player,height=100,width=120,hp=0)
boxWeapon=Box(pos=(700,500),player=player,height=100,width=120,hp=0)
bufHP=Buf(hp=100)
bufDefense=Buf(defense=10)
boxHP.isdraw=False
boxSheild.isdraw=False
boxWeapon.isdraw=False
# left_button = Button(30, 660, 70, 40, text="Left",
#                      function=lambda: print("left"))

startButton=Button(WIDTH/2,HEIGH/2,100,50,function=lambda: eng.changeScene(),formenu=True)
startButton.isdraw=True


phone=Image(img_loader.load("phone2.png",colorkey=[True,(0,0,0)],scale=(1,1)),isphone=True,speed=-1.7,width=1280)
phone2=Image(img_loader.load("phone2.png",colorkey=[True,(0,0,0)],scale=(1,1)),isphone=True,pos=(WIDTH+5,0),speed=-1.7,width=1280)
hero=img_loader.load("hero.png",colorkey=[True,(255,255,255)])
box_texture_weapon=img_loader.load("weapon_box1.png")
box_texture_shield=img_loader.load("Shield_box1.png",colorkey=[True,(255,255,255)])
box_texture_hp=img_loader.load("Hp_box1.png",colorkey=[True,(255,255,255)])



boxHP.set_texture(box_texture_hp)
boxSheild.set_texture(box_texture_shield)
boxWeapon.set_texture(box_texture_weapon)
                     
fps=Label(0,0,120,40)
cords=Label(130,0,320,40)
hp=Label(500,0,320,40)
enemyss=Label(700,0,200,40)
bulets_rightnow=Label(900,0,250,40)

walls=[Wall((-1,0),1,HEIGH),
    Wall((WIDTH,0),1,HEIGH),
    Wall((0,-1),WIDTH,1),
    Wall((0,HEIGH),WIDTH,1),
    ]

enemy_texures=[img_loader.load("enemy1.png",colorkey=[True,(255,255,255)]),img_loader.load("enemy2.png",colorkey=[True,(255,255,255)])]
bullet_texture=img_loader.load("bullet.png",colorkey=[True,(255,255,255)])
bullet_texture_enemy=img_loader.load("bullet_enemy1.png",colorkey=[True,(255,255,255)])

enemys=[Enemy((WIDTH-230,r.randint(100,700)),140,110,r.choice(enemy_texures),125,-100) for i in range(kolvo_enemys)]
#enemys=[Enemy((1000,r.randint(100,700)),140,110,enemy_texures[0],125),Enemy((1000,r.randint(100,700)),170,90,enemy_texture2,125)]

player.speed=speed_player


def pistol_traek(x):
    return x*0.0017

        
pistol=Weapon(damage=10,vectorx=1,shoot_parms=(10,150),start_spread=(-2,2),permanent_spread=(0,0),trajectory=pistol_traek)
automat=Weapon(damage=5,vectorx=1,shoot_parms=(40,150),start_spread=(-3,3),permanent_spread=(-4,1))
pulemet=Weapon(damage=12,vectorx=1,shoot_parms=(50,150),start_spread=(-5,3),permanent_spread=(-4,4))
laser=Weapon(damage=12,vectorx=1,shoot_parms=(12,150),start_spread=(0,1),permanent_spread=(0,0))



pistol_bullets=[Bullet(bullet_texture,4,3,1,r.randint(9,12),True) for i in range(10)]
automat_bullets=[Bullet(bullet_texture,12,5,3,r.randint(16,18),True) for i in range(45)]
pulemet_bullets=[Bullet(bullet_texture,14,6,2,r.randint(21,24),True) for i in range(45)]
laser_bullets=[Bullet(bullet_texture,25,5,32,r.randint(16,18),True) for i in range(3)]



pistol.load_bullets(pistol_bullets,eng)
automat.load_bullets(automat_bullets,eng)
pulemet.load_bullets(pulemet_bullets,eng)
laser.load_bullets(laser_bullets,eng)

weapons=[automat,pulemet,laser]


player.get_weapon(pistol)

#player.get_weapon(automat)

for enem in enemys:
    pistol_enmy=Weapon(damage=2,vectorx=-1,shoot_parms=(10,150),start_spread=(-2,2),permanent_spread=(-6,6))
    pistol_bullets_enemy=[Bullet(bullet_texture_enemy,30,21,1,r.randint(6,9),False) for i in range(kolvo_bullets_enemys)]
    pistol_enmy.load_bullets(pistol_bullets_enemy,eng)
    enem.get_weapon(pistol_enmy)

player.set_texture(hero)
eng.set_frame(FPS)
eng.set_res((WIDTH,HEIGH))


[eng.add_objects(i) for i in walls]
eng.add_objects(player)
eng.add_objects(phone)
eng.add_objects(phone2)
eng.add_objects(boxHP)
eng.add_objects(boxWeapon)
eng.add_objects(boxSheild)
eng.add_objects(startButton)
[eng.add_objects(i) for i in enemys]




def debug():
    fps.show(eng.display,text=f"FPS - {int(eng.fps_now)}",isbackground=False)
    cords.show(eng.display,text=f"xy({player.x} {player.y})",isbackground=False)
    hp.show(eng.display,text=f"hp: {int(player.hp)}",isbackground=False)
    enemyss.show(eng.display,text=f"enemys: {len(eng.objects["enemys"])}",isbackground=False)
    buls=len([i for i in eng.objects["bullets"] if i.isdraw])
    bulets_rightnow.show(eng.display,text=f"bullets: {buls}",isbackground=False)



def gen_box():
    if boxHP.hp<=0 and not boxHP.isdraw:
        boxHP.set_pos((r.randint(500,WIDTH-120),r.randint(130,HEIGH-120)))
        bufHP.hp=r.randint(25,300)
        boxHP.set_obj(bufHP,type="Buf")
        if r.randint(-2000,200000)>199910:
            boxHP.hp=r.randint(20,100)
            boxHP.isdraw=True
    if boxSheild.hp<=0 and not boxSheild.isdraw:
        boxSheild.set_pos((r.randint(500,WIDTH-120),r.randint(130,HEIGH-120)))
        bufDefense.defense=r.randint(5,150)
        boxSheild.set_obj(bufDefense,type="Buf")
        if r.randint(-2000,200000)>199920:
            boxSheild.hp=r.randint(70,150)
            boxSheild.isdraw=True
    if boxWeapon.hp<=0 and not boxWeapon.isdraw:
        boxWeapon.set_pos((r.randint(500,WIDTH-120),r.randint(130,HEIGH-120)))
        boxWeapon.set_obj(r.choice(weapons),type="Weapon")
        if r.randint(-2000,200000)>199000:
            boxWeapon.hp=r.randint(150,300)
            boxWeapon.isdraw=True
        
  

        
        
eng.addCustomFunc("debug",debug,True)
eng.addCustomFunc("boxesGen",gen_box,True)



# left_button = Button(30, 660, 70, 40, text="Left",
#                      function=lambda: print("left"))
# right_button = Button(1200, 660, 70, 40, text="Right",a
#                       function=lambda: print("right"))

eng.run(showColision=0)

