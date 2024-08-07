import pygame as pg
from math import sin,cos
import os
import random as r
from src.config import *
from functools import cache
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
        
    
class Images:
    
    def __init__(self,image,pos=(0,0)):
        self.image=image
        self.pos=pos
    
    def init_(self,scr):
        scr.blit(self.image,self.pos)
        
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
    
    def __init__(self,obj):
        self.obj=obj
        self.bullets=[]

    def load_bullets(self,bulets):
        self.bulets=bulets
        for i in self.bulets:
            #eng.add_objects(i)
            pass
        self.bulets_save=self.bulets

    def shoot(self):
        if self.bulets!=[]:
            #rint("shoot"+str(self.i))
            self.bulets[0].x=self.x+self.width
            self.bulets[0].y=self.y+self.height//2+r.randint(-7,7)
            self.bulets[0].isdraw=True
            self.bulets=self.bulets[1:]
            self.x-=self.otdacha
            #self.i+=1
        elif self.infbullets:
            self.bulets=self.bulets_save

class Bullet:
    
    def __init__(self,texure_bullet=None,width=5,height=5,damage=5,speed=3):
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
        self.player=False
        self.granis=(0,0,1280,720)

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
            self.y+=r.randint(-6,6)
            if not self.player:
                self.x-=self.speed
            else:
                self.x+=self.speed
            #print("drawed")
            if self.x>self.granis[2] or self.x<self.granis[0]:
                self.isdraw=False
        else:
            self.x,self.y=-100,-100
            self.rc=pg.Rect(self.x,self.y,self.texure_bullet.get_width(),self.texure_bullet.get_height())
                
    def get_type(self):
        return "bullet"
        
    
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
        self.bulets=[]
        self.ishoot=False
        self.infbullets=False
        self.bulets_save=[]
        self.speed_shoot=1
        self.count=0
        self.max_shootSpeed=10
        self.otdacha=0

    def add_bullets(self,bulets,eng):
        self.bulets=[i for i in bulets if i.player]
        for i in self.bulets:
            eng.add_objects(i)
        self.bulets_save=self.bulets

    def set_shoot_parms(self,speed,max_speed):
        self.speed_shoot=speed
        self.max_shootSpeed=max_speed

    def shoot(self):
        if self.bulets!=[]:
            #rint("shoot"+str(self.i))
            self.bulets[0].x=self.x+self.width
            self.bulets[0].y=self.y+self.height//2+r.randint(-7,7)
            self.bulets[0].isdraw=True
            self.bulets=self.bulets[1:]
            self.x-=self.otdacha
            #self.i+=1
        elif self.infbullets:
            self.bulets=self.bulets_save


    def set_texture(self,surface):
        self.texture=pg.transform.scale(surface,size=(self.width,self.height))
        self.rc=self.texture.get_rect()
    
    def moving(self):
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
        if keys[pg.K_SPACE] and pg.KEYDOWN:
            if self.count>=self.max_shootSpeed:
                self.shoot()
                self.count=0
        self.count+=self.speed_shoot      
        self.x+=self.vector[0]*self.speedx
        self.y+=self.vector[1]*self.speedy
              
    def init_(self,scr):
        self.moving()
        scr.blit(self.texture,(self.x,self.y))
        self.rc=pg.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
        #print(self.rc)
     
    def collider_chek(self,obj):
        if pg.Rect.colliderect(self.rc,obj.rc) and not obj.player:
            get_damage=obj.get_damage()
            self.hp-=get_damage
            get_damage=0
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

    def __init__(self,start_xy=(),width=10,height=10,texture=None,hp=10):
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
        self.bulets=[]
        self.live=True
        self.infbullets=False
        self.bulets_save=[]
        self.speed_shoot=1
        self.count=0
        self.max_shootSpeed=10
        self.otdacha=5
    
    def add_bullets(self,bulets,eng):
        self.bulets=[i for i in bulets if not i.player]
        for i in self.bulets:
            eng.add_objects(i)
        self.bulets_save=self.bulets
    
    def shoot(self):
        if self.bulets!=[]:
            #rint("shoot"+str(self.i))
            self.bulets[0].x=self.x
            self.bulets[0].y=self.y+self.height//2+r.randint(-7,7)
            self.bulets[0].isdraw=True
            self.bulets=self.bulets[1:]
            self.x+=self.otdacha
        elif self.infbullets:
            self.bulets=self.bulets_save
    
    def set_texture(self,surface):
        self.texture=pg.transform.scale(surface,size=(self.width,self.height))
        self.rc=self.texture.get_rect()    

    def set_xy(self, cord=()):
        if len(cord) != 2:
            cord = (self.x, self.y)
        self.x, self.y = cord

    def collider_chek(self,obj):
        if pg.Rect.colliderect(self.rc,obj.rc) and obj.player:
            get_damage=obj.get_damage()
            self.hp-=get_damage
            get_damage=0
            #self.texture=pg.transform.

    def set_x(self, x):
        self.x = x

    def set_shoot_parms(self,speed,max_speed):
        self.speed_shoot=speed
        self.max_shootSpeed=max_speed

    def set_y(self, y):
        self.x = y

    
    def init_(self, scr):
        if self.live:
            #print(len(self.bulets))
            scr.blit(self.texture,(self.x,self.y))
            self.rc=pg.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
            self.x-=self.speed+r.randint(-1,2)
            if self.count>=self.max_shootSpeed:
                self.shoot()
                self.count=0
            if self.hp<1 or self.x < 0:
                self.hp=self.hpsave
                self.x=self.mx
                self.y=r.randint(50,self.my-70)
            self.count+=self.speed_shoot
        else:
            del self.rc
        
        
        
    def draw_rect(self,scr):
        pg.draw.rect(scr,(0,255,0),self.rc)

    def get_type(self):
        return "enemy"


class Label:

    def __init__(self, x, y, weight, height, text="Label1", img_path=None):
        self.x = x
        self.y = y
        self.weight = weight
        self.height = height
        self.text = text
        self.img_path = img_path
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

    def __init__(self, x: int, y: int, width: int, height: int, images_pathes=(), text=None, function=None, isPressed=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.images_pathes = images_pathes
        self.function = function
        self.isPressed = isPressed
        if self.images_pathes != ():
            self.img1 = pg.image.load(self.images_pathes[0])
            self.img1 = pg.transform.scale(
                self.img1, (self.width, self.height))
            self.img1.set_colorkey((255, 255, 255))
            self.img1_rect = self.img1.get_rect(topleft=(self.x, self.y))

            self.img2 = pg.image.load(self.images_pathes[1])
            self.img2 = pg.transform.scale(
                self.img2, (self.width, self.height))
            self.img2.set_colorkey((255, 255, 255))
        else:
            self.zone = pg.Surface((self.x, self.y))
            self.zone = pg.transform.scale(
                self.zone, (self.width, self.height))
            self.zone_rect = self.zone.get_rect(topleft=(self.x, self.y))

    def show(self, scr):
        self.curret_img = self.img2 if self.isPressed else self.img1
        scr.blit(self.curret_img, self.img1_rect.topleft)

    def show_rect(self, scr, size=15, font="Comic Sans MS", aligin=(0, 0), color=(0, 0, 0), color_backgroud=(255, 255, 255)):
        my_font = pg.font.SysFont(font, size)
        text_rnd = my_font.render(self.text, False, color)
        self.zone.fill(color_backgroud)
        self.zone.blit(text_rnd, self.zone.get_rect(topleft=aligin))
        scr.blit(self.zone, self.zone_rect)

    def changing(self, mouse_pos):
        self.isPressed = self.img1_rect.collidepoint(mouse_pos)

    def do_func(self, event):
        if self.function != None and self.isPressed and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.function()

    def changing_rect(self, mouse_pos):
        self.isPressed = self.zone_rect.collidepoint(mouse_pos)

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
    
    def set_icon(self,img_path):
        pg.display.set_icon(pg.image.load(img_path))
        
    def set_frame(self, fps):
        self.fps = fps

    def addCustomFunc(self,name_func,func,work=False):
        self.cstfnc[name_func]={"function":func,"work":work}
        
    def set_work_func(self,name_func,work):
        self.cstfnc[name_func]["work"]=work
        
    def customFunctions(self):
        for funcs in self.cstfnc:
            if self.cstfnc[funcs]["work"]:
                    self.cstfnc[funcs]["function"]()
                    
    def set_title(self,title):
        self.caption=title
        pg.display.set_caption(self.caption)   
        
    def optimithastion(self):
        #method 1
        if self.methods[0]:
            ki=0
            while ki<self.lim_m1_koef and self.fps_now<self.fps*self.fps_m1_koef:
                try:
                    del self.objects["enemys"][ki]
                except:
                    break
                ki+=1
                       
    def updater_color(self,color=(100, 111, 87)):
        self.upd=color
    
    def run(self,showColision=False,colision=True):
        while self.runing:
            pg.draw.rect(self.display,self.upd,pg.Rect(0,0,self.w,self.h))
            self.fps_now=self.frame.get_fps()
            for img in self.objects["images"]:
                img.init_(self.display)
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
            for label in self.objects["lables"]:
                label.show(self.display)
            for bullet in self.objects["bullets"]:
                bullet.init_(self.display)
            for event in pg.event.get():                
                for button in self.objects["buttons"]:
                    button.show_rect(self.display)
                    button.changing_rect(pg.mouse.get_pos())
                    button.do_func(event)
                if event.type == pg.QUIT:
                    sys.exit()
            self.customFunctions()
            self.frame.tick(self.fps)
            pg.display.flip()
            
            
            

