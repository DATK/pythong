import pygame as pg
import os
import random as r
from Engine.src.config import *
import sys




class ImageLoader:
    
    def __init__(self):
        pass
    
    def load(self,image,colorkey=[False,(0,0,0)],scale=(1,1)):
        image=f"{IMAGES_PATH}{image}"
        res= os.path.splitext(image)
        if res==".png":
            surface = pg.image.load(image).convert_alfa()
        else:
            surface = pg.image.load(image).convert()
        if colorkey[0]:
            surface.set_colorkey((colorkey[1]))
        if scale!=(1,1):
            surface=pg.transform.scale(surface,size=(surface.get_width()*scale[0],surface.get_height()*scale[1]))
        return surface
        
    def load_bits(self,image_path):
        try:
            with open(image_path, "rb") as f:
                image=f.read()
        except:
            image=None
        return image



    
class Image:
    
    def __init__(self,image,pos=(0,0),dynamic=False,formenu=False,speed=-5,width=1280,hieght=800):
        self.image=pg.transform.scale(image,(width+3,hieght))
        self.x,self.y=pos
        self.dynamic=dynamic
        self.speedx=speed
        self.speedy=0
        self.width=width
        self.isdraw=True
        self.forMenu=formenu
        self.hieght=hieght


        
    def drawin(self):
        if self.isdraw:
            self.isdraw=False
        else:
            self.isdraw=True
    
    def init_(self,scr):
        if self.isdraw:
            self.move()
            scr.blit(self.image,(self.x,self.y))
    
    def move(self):
        if self.dynamic:
            width=self.width
            if self.x<=0-width:
                self.x=self.width
            self.x+=self.speedx
            self.y+=self.speedy

    def get_type(self):
        return "image"
    


class Bot:
    
    def __init__(self):
        self.speed_x=4.2
        self.speed_y=4.2
        self.size=50
        self.koef=7
        self.radius=self.size/self.koef
        self.x=r.randint(10,WIDTH-15)
        self.y=r.randint(10,HEIGH-15)
        self.rc=pg.Rect(self.x,self.y,self.radius,self.radius)
        

    def moving(self):
        if self.x>WIDTH:
            self.speed_x*=-1
        elif self.x<0:
            self.speed_x*=-1
        if self.y>HEIGH:
            self.speed_y*=-1
        elif self.y<0:
            self.speed_y*=-1
        self.x+=self.speed_x
        self.y+=self.speed_y
    
        
    def moring(self,rzm):
        if rzm<self.size:
            self.size+=rzm
            self.radius=self.size/self.koef
        else:
            pass
       
    
    def get_size(self):
        return self.size
    
    def draw_rect(self,scr):
        pg.draw.rect(scr,(0,255,0),self.rc)
    
    def minusing(self):
        if 100<self.size<300:
            self.size-=0.04
        elif 300<self.size<600:
            self.size-=0.25
        elif 600<self.size<800:
            self.size-=0.5
        elif 800<self.size<2000:
            self.size-=1.2
        
    def init_(self,scr):
        self.moving()
        self.minusing()
        self.rc=pg.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
        pg.draw.circle(scr,(255,0,0),(self.x,self.y),self.radius)
        
    def get_type(self):
        return "player"
    

class Weapon:
    
    def __init__(self,damage=10,vectorx=1,shoot_parms=(10,140),start_spread=(-7,-7),permanent_spread=(-6,6),kickback=0,trajectory=None):
        self.bullets=[]
        self.start_spread=start_spread
        self.kickback=kickback
        self.permanent_spread=permanent_spread
        self.infbullets=True
        self.damage=damage
        self.vectorX=vectorx
        self.shoot_parms=shoot_parms
        if trajectory==None:
            self.trajectory=self.defaul_trajectory
        else:
            self.trajectory=trajectory

    def load_bullets(self,bulets,eng):
        self.bulets=[i for i in bulets]
        for i in self.bulets:
            i.speed*=self.vectorX
            i.permanent_spread=self.permanent_spread
            i.set_trajectory(self.trajectory)
            i.damage+=self.damage
            eng.add_objects(i)
        self.bulets_save=self.bulets

    def defaul_trajectory(self,x): #return y cord
        return x*0

    def get_trajectory(self,functionX): #fucntion is get only x and return y
        self.trajectory=functionX

    def shoot(self,x,y):
        if self.bulets!=[]:
            #rint("shoot"+str(self.i))
            self.bulets[0].set_start_cords(x,y+r.randint(self.start_spread[0],self.start_spread[1]))
            self.bulets[0].isdraw=True
            self.bulets=self.bulets[1:]
            #self.i+=1
        elif self.infbullets:
            self.bulets=self.bulets_save
        

class Bullet:
    
    def __init__(self,texure_bullet=None,width=5,height=5,damage=5,speed=3,player=False,granis=(0,0,1280,720)):
        if texure_bullet==None:
            self.texure_bullet=pg.Surface((width,height))
            self.texure_bullet.fill((255,0,0))
        else:
            self.texure_bullet=texure_bullet
            self.texure_bullet=pg.transform.scale(self.texure_bullet,size=(width,height))
        self.rc=self.texure_bullet.get_rect()
        self.x=0
        self.width,self.height=width,height
        self.y=0
        self.damage=damage
        self.speed=speed
        self.isdraw=False
        self.player=player
        self.granis=granis
        self.permanent_spread=(-1,1)

    def set_start_cords(self,x,y):
        self.x=x
        self.y=y

    def set_trajectory(self,functionX):
        self.trajectory=functionX

    def get_damage(self):
        self.isdraw=False
        return self.damage
    
    def set_texture(self,surface):
        self.texure_bullet=pg.transform.scale(surface,size=(self.width,self.height))
        self.rc=self.texure_bullet.get_rect()
    
    def init_(self,scr):
        if self.isdraw:
            self.rc=pg.Rect(self.x,self.y,self.texure_bullet.get_width(),self.texure_bullet.get_height())
            scr.blit(self.texure_bullet,(self.x,self.y))
            self.x+=self.speed
            self.y=self.y+self.trajectory(self.x)
            self.y+=r.randint(self.permanent_spread[0],self.permanent_spread[1])
            #print("drawed")
            if self.x>self.granis[2] or self.x<self.granis[0]:
                self.isdraw=False
                self.x,self.y=-100,-100
                self.rc=pg.Rect(self.x,self.y,self.texure_bullet.get_width(),self.texure_bullet.get_height())
        else:
            self.x,self.y=-100,-100
            self.rc=pg.Rect(self.x,self.y,self.texure_bullet.get_width(),self.texure_bullet.get_height())

    def draw_rect(self,scr):
        pg.draw.rect(scr,(0,255,0),self.rc)
    
    def get_type(self):
        return "bullet"

class Buf:
    
    def __init__(self,hp=0,defense=0,):
        self.hp=hp
        self.defense=defense
        
    def init_(self):
        return (self.hp,self.defense)

class Box:

    def __init__(self,pos=(0,0),hp=100,width=10,height=10,player=None,texture=None)   :
        self.x,self.y=pos
        self.width,self.height=width,height
        self.obj=None
        self.isdraw=True
        self.hp=hp
        self.player=player
        if texture==None:
            self.texture=pg.Surface((width,height))
            self.texture.fill((255,0,0))
        else:
            self.texture=texture
            self.texture=pg.transform.scale(self.texture,size=(self.width,self.height))
        self.rc=self.texture.get_rect()

    def init_(self,scr):
        if self.isdraw:
            scr.blit(self.texture,(self.x,self.y))
            self.rc=pg.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
            if self.hp<0:
                self.isdraw=False
                self.x,self.y=(-1000,-100)
                self.rc=pg.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
                if self.obj!=None:
                    if self.type=="Weapon":
                        self.player.get_weapon(self.obj)
                    elif self.type=="Buf":
                        self.player.hp += self.obj.init_()[0]
                        self.player.defense+=self.obj.init_()[1]
                        
                        
    def set_pos(self,pos=(0,0)):
        self.x,self.y=pos
        
    def set_WH(self,wh=(0,0)):
        self.width,self.y=wh
        
    def set_texture(self,surface):
        self.texture=pg.transform.scale(surface,size=(self.width,self.height))
        self.rc=self.texture.get_rect()
    
    def set_player(self,player):
        self.player=player
    
    def set_obj(self,obj,type):
        self.obj=obj
        self.type=type
        
    def collider_chek(self,obj):
        if pg.Rect.colliderect(self.rc,obj.rc) and obj.player:
            get_damage=obj.get_damage()
            self.hp-=get_damage
            get_damage=0

    def get_type(self):
        return "enemy"

    def draw_rect(self,scr):
        if self.isdraw: pg.draw.rect(scr,(0,255,0),self.rc)


class Player:
    
    def __init__(self,start_xy=(),width=10,height=10,texture=None,hp=100):
        self.x,self.y=start_xy
        self.width,self.height=width,height
        self.hp=hp
        if texture==None:
            self.texture=pg.Surface((width,height))
            self.texture.fill((255,0,0))
        else:
            self.texture=texture
            self.texture=pg.transform.scale(self.texture,size=(self.width,self.height))
        self.rc=self.texture.get_rect()
        self.speed=4
        self.speedx=self.speed
        self.vector=[0,0]
        self.speedy=self.speed
        self.speed_shoot=1
        self.count=0
        self.max_shootSpeed=10
        self.has_weapon=False
        self.defense=99
        self.defense_koef=0.4


    def get_weapon(self,weapon):
        self.weapon=weapon
        self.has_weapon=True
        self.speed_shoot,self.max_shootSpeed=weapon.shoot_parms[0],weapon.shoot_parms[1]

    def set_texture(self,surface):
        self.texture=pg.transform.scale(surface,size=(self.width,self.height))
        self.rc=self.texture.get_rect()
    
    def moving_pc(self):
        self.vector=[0,0]
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vector[1]-=1
        if keys[pg.K_s]:
            self.vector[1]+=1
        if keys[pg.K_a]:
            self.vector[0]-=1
        if keys[pg.K_d]:
            self.vector[0]+=1
        if keys[pg.K_SPACE] and self.has_weapon:
            if self.count>=self.max_shootSpeed:
                self.weapon.shoot(self.x+self.width,self.y+self.height//2)
                self.x-=self.weapon.kickback
                self.count=0
        self.count+=self.speed_shoot      
        self.x+=self.vector[0]*self.speedx
        self.y+=self.vector[1]*self.speedy
              
    def init_(self,scr):
        self.moving_pc()
        if self.defense<0:
                self.defense=0
        if self.defense>125:
            self.defense=125
        if self.hp>250:
            self.hp=250
        scr.blit(self.texture,(self.x,self.y))
        self.rc=pg.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
        #print(self.rc)
     
    def collider_chek(self,obj):
        if pg.Rect.colliderect(self.rc,obj.rc) and not obj.player:
            get_damage=obj.get_damage()
            dmg=get_damage-get_damage*self.defense/100
            if dmg<0:
                dmg=0
            self.hp-=dmg
            dmg=0
            self.defense-=self.defense_koef
            #self.texture=pg.transform.
            # 
   
    def chek_colis(self,rect):
        if pg.Rect.colliderect(self.rc,rect):
            if self.vector[0]==-1:
                self.x+=self.speedx
                self.speedx=0
            elif self.vector[0]==1:
                self.x-=self.speedx
                self.speedx=0
            if self.vector[1]==1:
                self.y-=self.speedy
                self.speedy=0
            elif self.vector[1]==-1:
               self.y+=self.speedy
        else:
            self.speedx=self.speed
            self.speedy=self.speed-2
                  
    def draw_rect(self,scr):
        pg.draw.rect(scr,(0,255,0),self.rc)
    
    def get_type(self):
        return "player"
 

class Wall:
    
    def __init__(self,start_xy=(0,0),width=10,height=10,texture=None):
        self.x,self.y=start_xy
        self.width,self.height=width,height
        if texture==None:
            self.texture=pg.Surface((width,height))
            self.texture.fill((0,255,0))
        else:
            self.texture=texture
            self.texture=pg.transform.scale(self.texture,size=(self.width,self.height))
        self.rc=self.texture.get_rect()
     
    def set_texture(self,surface):
        self.texture=pg.transform.scale(surface,size=(self.width,self.height))
        self.rc=self.texture.get_rect()
          
    def get_rc(self):
        return self.rc
        
    def init_(self,scr):
        scr.blit(self.texture,(self.x,self.y))
        self.rc=pg.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
        
    def get_type(self):
        return "wall"
   
class Circle:

    def __init__(self, start_pos=(0, 0), radius=10, function=None):
        self.x, self.y = start_pos
        self.radius = radius
        self.function = function
        self.color = (0, 0, 0)

    def set_color(self, color=(0, 0, 0)):
        self.color = color

    def move_x(self, n):
        self.x += n

    def move_y(self, n):
        self.y += n

    def set_xy(self, cord=()):
        if len(cord) != 2:
            cord = (self.x, self.y)
        self.x, self.y = cord

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.x = y

    def init_(self, scr):
        pg.draw.circle(scr, self.color, (self.x, self.y), self.radius)
        self.function()

    def get_type(self):
        return "figure"
    

class Enemy:

    def __init__(self,start_xy=(),width=10,height=10,texture=None,hp=10,stopX=-100):
        self.x,self.y=start_xy
        self.width,self.height=width,height
        self.hp=hp
        if texture==None:
            self.texture=pg.Surface((width,height))
            self.texture.fill((255,0,0))
        else:
            self.texture=texture
            self.texture=pg.transform.scale(self.texture,size=(self.width,self.height))
        self.rc=self.texture.get_rect()
        self.speed=2
        self.vector=[0,0]
        self.hpsave=self.hp
        self.mx,self.my=1280,700
        self.live=True
        self.speed_shoot=1
        self.count=0
        self.max_shootSpeed=10
        self.has_weapon=False
        self.stopX=stopX
        self.defense=5


    def set_texture(self,surface):
        self.texture=pg.transform.scale(surface,size=(self.width,self.height))
        self.rc=self.texture.get_rect()    

    def set_xy(self, cord=()):
        if len(cord) != 2:
            cord = (self.x, self.y)
        self.x, self.y = cord

    def get_weapon(self,weapon):
        self.weapon=weapon
        self.has_weapon=True
        self.speed_shoot,self.max_shootSpeed=weapon.shoot_parms[0],weapon.shoot_parms[1]

    def collider_chek(self,obj):
        if pg.Rect.colliderect(self.rc,obj.rc) and obj.player:
            get_damage=obj.get_damage()
            dmg=get_damage-get_damage*self.defense/100
            if dmg<0:
                dmg=0
            self.hp-=dmg
            dmg=0
            #self.texture=pg.transform.

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.x = y

    def init_(self, scr):
        if self.live:
            #print(len(self.bulets))
            scr.blit(self.texture,(self.x,self.y))
            self.rc=pg.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
            self.x-=self.speed+r.randint(-1,2)
            if self.count>=self.max_shootSpeed and self.has_weapon:
                self.weapon.shoot(self.x,self.y+self.height//2)
                self.x-=self.weapon.kickback
                self.count=0
            if self.hp<1 or self.x < 0:
                self.hp=self.hpsave
                self.x=self.mx
                self.y=r.randint(50,self.my-100)
            if self.x<=self.stopX:
                self.speed=0
                self.x=self.stopX
            self.count+=self.speed_shoot
        else:
            self.rc=pg.Rect(-1000,-1000,self.texture.get_width(),self.texture.get_height())
        
        
    def draw_rect(self,scr):
        pg.draw.rect(scr,(0,255,0),self.rc)

    def get_type(self):
        return "enemy"


class Label:

    def __init__(self, x, y, weight, height, text="Label1",formenu=False, img_path=None):
        self.x = x
        self.y = y
        self.weight = weight
        self.height = height
        self.text = text
        self.img_path = img_path
        self.forMenu=formenu
        if img_path != None:
            self.zone = pg.image.load(self.img_path)
            self.zone = pg.transform.scale(
                self.zone, (self.weight, self.height))
            self.zone_rect = self.zone.get_rect()
        else:
            self.zone = pg.Surface((self.x, self.y))
            self.zone = pg.transform.scale(
                self.zone, (self.weight, self.height))
            self.zone_rect = self.zone.get_rect(topleft=(self.x, self.y))

    def show(self, scr, text=None, color_background=(0, 0, 0), isbackground=True, font="Comic Sans MS", size=25, aligin=(0, 0), color=(255, 255, 255)):
        if text != None:
            self.text = text
        my_font = pg.font.SysFont(font, size)
        if not isbackground:
            self.zone.fill((0, 0, 0))
            self.zone.set_colorkey((0, 0, 0))
        else:
            self.zone.fill(color_background)
        text_rnd = my_font.render(self.text, False, color)

        self.zone.blit(text_rnd, self.zone.get_rect(topleft=aligin))
        scr.blit(self.zone, self.zone_rect)
        #scr.blit(text_rnd, self.zone.get_rect())
        #scr.blit(self.zone, self.zone_rect.topleft)
        
    def get_type(self):
        return "label"


class Button:

    def __init__(self, x: int, y: int, width: int, height: int, textures=(), text=None, function=None, isPressed=False,formenu=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.function = function
        self.isPressed = isPressed
        self.text="Button"
        self.isdraw=True
        self.showed=False
        self.forMenu=formenu
        if textures!=():
            self.img1=textures[0]
            self.img1 = pg.transform.scale(
                self.img1, (self.width, self.height))
            self.img2=textures[1]
            self.img2 = pg.transform.scale(
                self.img2, (self.width, self.height))
            self.withtexture=True
        else:
            self.img1=pg.Surface((width,height))
            self.img1 = pg.transform.scale(self.img1, (self.width, self.height))
            self.img2=pg.Surface((width,height))
            self.img2 = pg.transform.scale(self.img2, (self.width, self.height))
            self.withtexture=False
        self.set_parms()

    def show(self, scr):
        if self.isdraw:
            if self.withtexture:
                if self.isPressed:self.curret_img = self.img2
                else: self.curret_img = self.img1
            else:
                if self.isPressed:self.curret_img = self.img2
                else: self.curret_img = self.img1
                self.curret_img.blit(self.text_rnd, self.curret_img.get_rect(topleft=self.aligin))
            scr.blit(self.curret_img,(self.x,self.y))
            self.showed=True
        else:
            self.showed=False
            
            
    def set_parms(self,size=15, font="Comic Sans MS", aligin=(0, 0), color=(0, 0, 0), color_backgroud=((255, 255, 255),(0,0,0))):
        self.size=size
        self.font=font
        self.aligin=aligin
        self.color=color
        self.color_backgroud=color_backgroud
        my_font = pg.font.SysFont(self.font, self.size)
        self.text_rnd = my_font.render(self.text, False, self.color)
        self.img1.fill(self.color_backgroud[0])
        self.img2.fill(self.color_backgroud[1])

    def changing(self, mouse_pos):
        if self.isdraw:
            self.isPressed = pg.rect.Rect(self.x,self.y,self.width,self.height).collidepoint(mouse_pos)

    def do_func(self, event):
        if self.function != None and self.isPressed and event.type == pg.MOUSEBUTTONUP and self.isdraw and self.showed:
            self.function()

    def get_type(self):
        return "button"


class Engine:

    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((1280, 720))
        self.w,self.h=(1280,720)
        self.events = []
        self.objects = {"buttons": [], "lables": [],
                        "enemys": [], "camera": [], "figures": [], "players": [],"walls":[],"images":[],"bullets":[]}
        self.runing = True
        self.frame = pg.time.Clock()
        self.fps = 144
        self.fps_now=145
        self.cstfnc={}
        self.upd=(100, 111, 87)
        self.caption="My game"
        self.methods=(False,False)
        self.fps_m1_koef=0.8
        self.lim_m1_koef=100
        self.menu=True
        pg.display.set_caption(self.caption)
        
    def set_res(self,res=(640,480)):
        self.w,self.h=res
        self.display = pg.display.set_mode(res)
        
    def add_objects(self, obj):
        typeob = obj.get_type()
        if typeob == "button":
            self.objects["buttons"].append(obj)
        elif typeob == "label":
            self.objects["lables"].append(obj)
        elif typeob == "enemy":
            self.objects["enemys"].append(obj)
        elif typeob == "bullet":
            self.objects["bullets"].append(obj)
        elif typeob == "player":
            self.objects["players"].append(obj)
        elif typeob == "wall":
            self.objects["walls"].append(obj)
        elif typeob == "image":
            self.objects["images"].append(obj)
        else:
            pass
    
    def set_fuclscreen(self):
        self.display=pg.display.set_mode((0,0),pg.FULLSCREEN)
        self.w,self.h=(self.display.get_width(),self.display.get_height())
        return (self.w,self.h)
        
    def set_icon(self,img_path):
        pg.display.set_icon(pg.image.load(img_path))
        
    def set_frame(self, fps):
        self.fps = fps

    def addCustomFunc(self,name_func,func,work=False):
        self.cstfnc[name_func]={"function":func,"work":work}
        
    def set_work_func(self,name_func,work):
        self.cstfnc[name_func]["work"]=work
        
    def change_work_func(self,name_func):
        self.cstfnc[name_func]["work"]=False if self.cstfnc[name_func]["work"] else True
        
    def customFunctions(self):
        for funcs in self.cstfnc:
            if self.cstfnc[funcs]["work"]:
                    self.cstfnc[funcs]["function"]()
                    
    def set_title(self,title):
        self.caption=title
        pg.display.set_caption(self.caption)   
           
    def updater_color(self,color=(100, 111, 87)):
        self.upd=color
    
    def startMenu(self):
        self.menu=True
    
    def startGame(self):
        self.menu=False
    
    def loadScene(self,scene):
        self.objects=scene.get()
    
    def clear_objects(self):
        self.objects["enemys"]=[]
        self.objects["players"]=[]
        self.objects["walls"]=[]
        self.objects["bullets"]=[]
    
    def clear_images(self):
        self.objects["images"]=[]
    
    def clear_all(self):
        for obj in self.objects:
            self.objects[obj]=[]
    
    def get_size_window(self):
        return self.display.get_size()
            
    
    def gameScene(self,showColision):
        for img in self.objects["images"]:
            if not img.forMenu: img.init_(self.display)
        for enemy in self.objects["enemys"]:
            enemy.init_(self.display) 
            for bul in self.objects["bullets"]:
                enemy.collider_chek(bul)
            if showColision: enemy.draw_rect(self.display)
        for player in self.objects["players"]:
            player.init_(self.display)
            for bul in self.objects["bullets"]:
                player.collider_chek(bul)
            if showColision: player.draw_rect(self.display)
        for wall in self.objects["walls"]:
            wall.init_(self.display)
            pl = self.objects["players"][0]
            pl.chek_colis(wall.rc)
        for bullet in self.objects["bullets"]:
            bullet.init_(self.display)
            if showColision: bullet.draw_rect(self.display)
        for label in self.objects["lables"]:
            if not label.forMenu: label.show(self.display)
        for button in self.objects["buttons"]:
                if not button.forMenu:
                    button.show(self.display)
        for event in pg.event.get():                
            for button in self.objects["buttons"]:
                if not button.forMenu:
                    button.changing(pg.mouse.get_pos())
                    button.do_func(event)
            if event.type == pg.QUIT:
                sys.exit()
    
    def changeScene(self):
        self.menu = False if self.menu else True
    
    def menuScene(self):
        for img in self.objects["images"]:
            if img.forMenu: img.init_(self.display)
        for label in self.objects["lables"]:
            if label.forMenu: label.show(self.display)
        for button in self.objects["buttons"]:
                if button.forMenu:
                    button.show(self.display)
        for event in pg.event.get():                
            for button in self.objects["buttons"]:
                if button.forMenu:
                    button.changing(pg.mouse.get_pos())
                    button.do_func(event)
            if event.type == pg.QUIT:
                sys.exit()
    
    def run(self,showColision=False):
        while self.runing:
            pg.draw.rect(self.display,self.upd,pg.Rect(0,0,self.w,self.h))
            self.fps_now=self.frame.get_fps()
            
            if self.menu:
                self.menuScene()
            else:
                self.gameScene(showColision)
                
            self.customFunctions()
            self.frame.tick(self.fps)
            pg.display.update()
            
            
            

