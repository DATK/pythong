import pygame as pg
from math import sin,cos
import random as r
from src.config import *
from functools import cache



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
    
    
    
class Player:
    
    def __init__(self,name):
        self.size=50
        self.max_size=6000
        self.koef=7
        self.speed_koef=0.5
        self.radius=self.size/self.koef
        self.name=name
        self.speed=5
        self.del_koef=1.3
        self.rad_koef=1.5
        self.angle=0.04
        self.tmp=self.speed
        self.x=r.randint(10,WIDTH-15)
        self.y=r.randint(10,HEIGH-15)
        self.rc=pg.Rect(self.x,self.y,self.radius,self.radius)
    
    def get_size(self):
        return self.size
    
    
    def moving(self):
        keys = pg.key.get_pressed()
        sin_a=sin(self.angle)
        cos_a=cos(self.angle)
        if keys[pg.K_w]:
            self.x+=self.speed*cos_a
            self.y+=self.speed*sin_a
        if keys[pg.K_s]:
            self.x-=self.speed*cos_a
            self.y-=self.speed*sin_a
        if keys[pg.K_a]:
            self.angle -= 0.07
        if keys[pg.K_d]:
            self.angle += 0.07

            
    def stop(self):
        self.tmp=self.speed
        self.speed=0
    
    def start(self):
        self.speed=self.tmp

    def moring(self,rzm):
        if rzm<self.size and self.size<=self.max_size:
            self.size+=rzm
            #self.speed=len(str(int(self.size)))/self.speed_koef
        else:
            pass
        
    def rating(self):
        self.radius=self.size/self.koef
        if 100<self.size<300:
            self.size-=0.02
        elif 300<self.size<600:
            self.size-=0.06
        elif 600<self.size<800:
            self.size-=0.08
        elif 800<self.size<2000:
            self.size-=0.16
        elif 2000<self.size<2300:
            self.size-=0.3
        elif 2300<self.size<4000:
                self.size-=0.5
        elif 4000<self.size<6000:
                self.size-=0.8
        elif 6000<self.size<12000:
            self.size-=1
        elif self.size>15000:
            self.size-=5
            
    def init_(self,scr):
        self.moving()
        self.rating()
        self.rc=pg.Rect(self.x-self.radius//self.del_koef,self.y-self.radius//self.del_koef,self.radius*self.rad_koef,self.radius*self.rad_koef)
        pg.draw.circle(scr,(255,0,0),(self.x,self.y),self.radius)
       # pg.draw.line(scr,(255,0,255),(self.x-self.radius,self.y-self.radius),(self.x+7,self.y+7),3)

    def draw_rect(self,scr):
        pg.draw.rect(scr,(0,255,0),self.rc)
    
    def get_type(self):
        return "player"
    
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
    
   
class Wall:
    
    def __init__(self,x,y,width,heigh,color=(255,255,255)):
        self.x,self.y=x,y
        self.width,self.hiegh=width,heigh
        self.color=color
        self.rc=pg.Rect(self.x,self.y,self.width,self.hiegh)
        
    
    def init_(self):
        self.rc=pg.Rect(self.x,self.y,self.width,self.hiegh)
        
    def get_type(self):
        return "wall"


class Enemy:

    def __init__(self,start_pos=(0,1),size=50):
        self.x, self.y = start_pos
        self.size=size
        self.koef=0.5
        self.radius=self.size/self.koef
        self.color=(r.randint(0,255),r.randint(0,255),r.randint(0,255))
        self.rc=pg.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
        
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

    def get_size(self):
        a = self.size
        self.restart()
        return a
    
    def restart(self):
        self.x, self.y=(r.randint(2,WIDTH-30),r.randint(2,HEIGH-30))
        self.size=1
        self.color=(r.randint(0,255),r.randint(0,255),r.randint(0,255))
        self.rc=pg.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
    
    def init_(self, scr):
        pg.draw.circle(scr, self.color, (self.x, self.y), self.radius)
        
        
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
                        "enemys": [], "camera": [], "figures": [], "players": [],"walls":[],"another":[]}
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
        elif typeob == "figure":
            self.objects["figures"].append(obj)
        elif typeob == "player":
            self.objects["players"].append(obj)
        elif typeob == "wall":
            self.objects["walls"].append(obj)
        else:
            pass
    
    #
    
    def set_frame(self, fps):
        self.fps = fps

    def addCustomFunc(self,name_func,func,work=False):
        self.cstfnc[name_func]={"function":func,"work":work}
        
    def set_work_func(self,name_func,work):
        self.cstfnc[name_func]["work"]=work
        

    def  customFunctions(self):
        for funcs in self.cstfnc:
            if self.cstfnc[funcs]["work"]:
                    self.cstfnc[funcs]["function"]()
                    
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

                
    def collision_chek(self):
        for pl in self.objects["players"]:
            for en in self.objects["enemys"]:
                if pg.Rect.colliderect(pl.rc,en.rc):
                    pl.moring(en.get_size())
                
    
    def updater_color(self,color=(100, 111, 87)):
        self.upd=color
    
    def run(self,showColision=False):
        while self.runing:
            pg.display.set_caption(self.caption)
            pg.draw.rect(self.display,self.upd,pg.Rect(0,0,self.w,self.h))
            self.fps_now=self.frame.get_fps()
            self.optimithastion()
            for enemy in self.objects["enemys"]:
                enemy.init_(self.display)
                if showColision: enemy.draw_rect(self.display)
            for player in self.objects["players"]:
                player.init_(self.display)
                if showColision: player.draw_rect(self.display)
            for label in self.objects["lables"]:
                label.show(self.display)
            for figure in self.objects["figures"]:
                figure.init_(self.display)
            for event in pg.event.get():                
                for button in self.objects["buttons"]:
                    button.show_rect(self.display)
                    button.changing_rect(pg.mouse.get_pos())
                    button.do_func(event)
                
                if event.type == pg.QUIT:
                    exit()
            self.collision_chek()
            self.customFunctions()
            self.frame.tick(self.fps)
            pg.display.flip()
            
            

