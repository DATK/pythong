from Engine.Engine import Engine,Button,Label,ImageLoader,Image,Wall,Player,Bullet,Enemy,Weapon,Box,Buf,Scene
import random as r
import json
import sys

with open("config.json","r",encoding="UTF-8") as f:
    data=json.load(f)
kolvo_enemys=data['kolvo_enemys']
kolvo_bullets_enemys=data['kolvo_bullets_enemys']
speed_enemys=data['speed_enemys']
speed_player=data['speed_player']
FPS=data['FPS_MAX']



eng = Engine()
img_loader=ImageLoader() 

ButtonX,ButtonY=180,70

mainMenu=Scene()
Game_play=Scene()

WIDTH,HEIGH=eng.set_fuclscreen()

player=Player((WIDTH*0.08,HEIGH*0.075),90,80)

hero=img_loader.load("hero.png",colorkey=[True,(255,255,255)])
box_texture_weapon=img_loader.load("weapon_box1.png")
box_texture_shield=img_loader.load("Shield_box1.png",colorkey=[True,(255,255,255)])
box_texture_hp=img_loader.load("Hp_box1.png",colorkey=[True,(255,255,255)])
enemy_texures=[img_loader.load("enemy1.png",colorkey=[True,(255,255,255)]),img_loader.load("enemy2.png",colorkey=[True,(255,255,255)])]
bullet_texture=img_loader.load("bullet.png",colorkey=[True,(255,255,255)])
bullet_texture_enemy=img_loader.load("bullet_enemy1.png",colorkey=[True,(255,255,255)])

playbutton1=img_loader.load("playbutton1.png")
playbutton2=img_loader.load("playbutton2.png")

settingsbutton1=img_loader.load("settingsbutton1.png")
settingsbutton2=img_loader.load("settingsbutton2.png")

menubutton1=img_loader.load("buttonmenu1.png")
menubutton2=img_loader.load("buttonmenu2.png")

exitbutton1=img_loader.load("exitbutton1.png")
exitbutton2=img_loader.load("exitbutton1.png")

phone=Image(img_loader.load("phone.png",colorkey=[True,(0,0,0)],scale=(1,1)),dynamic=True,speed=-1.7,width=WIDTH,hieght=HEIGH)
phone2=Image(img_loader.load("phone.png",colorkey=[True,(0,0,0)],scale=(1,1)),dynamic=True,pos=(WIDTH,0),speed=-1.7,width=WIDTH,hieght=HEIGH)
phone_menu=Image(img_loader.load("phone3.png",colorkey=[False,(0,0,0)],scale=(1,1)),dynamic=False,pos=(0,0),width=WIDTH,hieght=HEIGH)

def settings():
    if setingsButton.isdraw:
        startButton.isdraw=False
        exitButon.isdraw=False
        debugButton.isdraw=False
        setingsButton.isdraw=False
        FpsLock60.isdraw=True
        settingsTwo.isdraw=True
        settingsThree.isdraw=True
        settingsBackToMenu.isdraw=True
        
    else:
        FpsLock60.isdraw=False
        settingsTwo.isdraw=False
        settingsThree.isdraw=False
        settingsBackToMenu.isdraw=False
        startButton.isdraw=True
        exitButon.isdraw=True
        debugButton.isdraw=True
        setingsButton.isdraw=True

def fpsLock():
    if eng.fps==60:
        eng.set_frame(1000)
    else:
        eng.set_frame(60)
    if eng.fps==60:
        FpsLock60.set_parms(40,aligin=(20,20),color_backgroud=ButtnOn)
    else:
        FpsLock60.set_parms(40,aligin=(20,20),color_backgroud=ButtnOff)            

def change_scene(scene):
    eng.load_scene(scene)
    eng.change_work_func("boxesGen")
    
    
# 6-10


ButtnOn=((255,255,255),(0,200,0))
ButtnOff=((255,255,255),(100,0,0))
startButton=Button(WIDTH*0.4,HEIGH*0.2,ButtonX,ButtonY,textures=(playbutton1,playbutton2),function=lambda: change_scene(Game_play))
startButton.text="Играть"
startButton.set_parms(40,aligin=(40,20),color_backgroud=((255,255,255),(150,150,150)))

stopButton=Button(WIDTH-200,0,ButtonX,ButtonY,textures=(menubutton1,menubutton2),function=lambda: change_scene(mainMenu))
stopButton.text="В меню"
stopButton.set_parms(40,aligin=(40,20),color_backgroud=((255,255,255),(150,150,150)))

exitButon=Button(WIDTH*0.4,HEIGH*0.80,ButtonX,ButtonY,textures=(exitbutton1,exitbutton2),function=lambda: sys.exit())
exitButon.text="Выход"
exitButon.set_parms(40,aligin=(40,20),color_backgroud=((255,255,255),(150,150,150)))

debugButton=Button(WIDTH*0.4,HEIGH*0.60,ButtonX,ButtonY,function=lambda: eng.change_work_func("debug"))
debugButton.text="Дебаг"
debugButton.set_parms(40,aligin=(40,20),color_backgroud=((255,255,255),(150,150,150)))

FpsLock60=Button(WIDTH*0.4,HEIGH*0.2,ButtonX,ButtonY,function=fpsLock)
FpsLock60.text="Лок в 60 фпс"
FpsLock60.isdraw=False
FpsLock60.set_parms(40,aligin=(20,20),color_backgroud=ButtnOn)


settingsTwo=Button(WIDTH*0.4,HEIGH*0.40,ButtonX,ButtonY,function=eng.clear_objects)
settingsTwo.text="Удалить"
settingsTwo.isdraw=False
settingsTwo.set_parms(40,aligin=(1,20),color_backgroud=ButtnOff)

settingsThree=Button(WIDTH*0.4,HEIGH*0.60,ButtonX,ButtonY,function=None)
settingsThree.text="Недоступно"
settingsThree.isdraw=False
settingsThree.set_parms(40,aligin=(1,20),color_backgroud=ButtnOff)

settingsBackToMenu=Button(WIDTH*0.4,HEIGH*0.80,ButtonX,ButtonY,textures=(menubutton1,menubutton2),function=settings)
settingsBackToMenu.text="Вернуться"
settingsBackToMenu.isdraw=False
settingsBackToMenu.set_parms(38,aligin=(2,20),color_backgroud=((255,255,255),(150,150,150)))

setingsButton=Button(WIDTH*0.4,HEIGH*0.40,ButtonX,ButtonY,textures=(settingsbutton1,settingsbutton2),function=settings)
setingsButton.text="Настройки"
setingsButton.set_parms(38,aligin=(2,20),color_backgroud=((255,255,255),(150,150,150)))



fps=Label(0,0,120,40)
cords=Label(130,0,320,40)
hp=Label(500,0,320,40)
enemyss=Label(700,0,200,40)
bulets_rightnow=Label(900,0,250,40)
all_enemys=Label(1150,0,250,40)

walls=[Wall((-1,0),1,HEIGH),
    Wall((WIDTH,0),1,HEIGH),
    Wall((0,-1),WIDTH,1),
    Wall((0,HEIGH),WIDTH,1),
    ]

enemys=[Enemy((WIDTH-230,r.randint(100,HEIGH-150)),
            WIDTH*0.1,HEIGH*0.095,r.choice(enemy_texures),125,-100) for i in range(kolvo_enemys)]


def pistol_traek(x):
    return x*0.0017

pistol=Weapon(damage=10,vectorx=1,shoot_parms=(10,150),start_spread=(-2,2),permanent_spread=(0,0),trajectory=pistol_traek)
automat=Weapon(damage=5,vectorx=1,shoot_parms=(40,150),start_spread=(-3,3),permanent_spread=(-4,1))
pulemet=Weapon(damage=12,vectorx=1,shoot_parms=(50,150),start_spread=(-5,3),permanent_spread=(-4,4))
laser=Weapon(damage=12,vectorx=1,shoot_parms=(12,150),start_spread=(0,1),permanent_spread=(0,0))

pistol_bullets=[Bullet(bullet_texture,4,3,1,r.randint(9,12),True,granis=(0,0,WIDTH,HEIGH)) for i in range(10)]
automat_bullets=[Bullet(bullet_texture,12,5,3,r.randint(16,18),True,granis=(0,0,WIDTH,HEIGH)) for i in range(45)]
pulemet_bullets=[Bullet(bullet_texture,14,6,2,r.randint(21,24),True,granis=(0,0,WIDTH,HEIGH)) for i in range(45)]
laser_bullets=[Bullet(bullet_texture,25,5,32,r.randint(16,18),True,granis=(0,0,WIDTH,HEIGH)) for i in range(3)]

pistol.load_bullets(pistol_bullets,Game_play)
automat.load_bullets(automat_bullets,Game_play)
pulemet.load_bullets(pulemet_bullets,Game_play)
laser.load_bullets(laser_bullets,Game_play)

weapons=[automat,pulemet,laser]

boxHP=Box(pos=(700,500),player=player,height=100,width=120,hp=0)
boxSheild=Box(pos=(700,500),player=player,height=100,width=120,hp=0)
boxWeapon=Box(pos=(700,500),player=player,height=100,width=120,hp=0)
bufHP=Buf(hp=100)
bufDefense=Buf(defense=10)
boxHP.isdraw=False
boxSheild.isdraw=False
boxWeapon.isdraw=False


for enem in enemys:
    pistol_enmy=Weapon(damage=2,vectorx=-1,shoot_parms=(2,160),start_spread=(-2,2),permanent_spread=(-6,6))
    pistol_bullets_enemy=[Bullet(bullet_texture_enemy,30,21,1,r.randint(6,9),False,granis=(0,0,WIDTH,HEIGH)) for i in range(kolvo_bullets_enemys)]
    pistol_enmy.load_bullets(pistol_bullets_enemy,Game_play)
    enem.get_weapon(pistol_enmy)
    enem.speed=speed_enemys

    
player.set_texture(hero)
eng.set_frame(FPS)


player.get_weapon(pistol)
player.speed=speed_player
player.set_res((WIDTH,HEIGH))
player.forandroid=False

boxHP.set_texture(box_texture_hp)
boxSheild.set_texture(box_texture_shield)
boxWeapon.set_texture(box_texture_weapon)

def debug():
    fps.show(eng.display,text=f"FPS - {int(eng.fps_now)}",isbackground=False)
    cords.show(eng.display,text=f"xy({int(player.x)} {int(player.y)})",isbackground=False)
    hp.show(eng.display,text=f"hp: {int(player.hp)}",isbackground=False)
    enemyss.show(eng.display,text=f"enemys: {len(eng.objects['enemys'])}",isbackground=False)
    buls=len([i for i in eng.objects["bullets"] if i.isdraw])
    bulets_rightnow.show(eng.display,text=f"bullets: {buls}",isbackground=False)
    c=0
    for i in eng.objects:
        c+=len(eng.objects[i])
    all_enemys.show(eng.display,text=f"objects: {c}",isbackground=False)

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
        if r.randint(-2000,200000)>199930:
            boxWeapon.hp=r.randint(150,300)
            boxWeapon.isdraw=True
         
         

         
 
[Game_play.add_objects(i) for i in walls]
Game_play.add_objects(player)
Game_play.add_objects(phone)
Game_play.add_objects(phone2)
mainMenu.add_objects(phone_menu)
Game_play.add_objects(boxHP)
Game_play.add_objects(boxWeapon)
Game_play.add_objects(boxSheild)
mainMenu.add_objects(startButton)
Game_play.add_objects(stopButton)
mainMenu.add_objects(debugButton)
mainMenu.add_objects(exitButon)
mainMenu.add_objects(setingsButton)
mainMenu.add_objects(FpsLock60)
mainMenu.add_objects(settingsTwo)
mainMenu.add_objects(settingsThree)
mainMenu.add_objects(settingsBackToMenu)
[Game_play.add_objects(i) for i in enemys]    

eng.addCustomFunc("debug",debug,False)
eng.addCustomFunc("boxesGen",gen_box,False)


eng.load_scene(mainMenu)

eng.run(showColision=0)