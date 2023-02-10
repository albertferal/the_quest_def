import pygame as pg
import random
from main import *

VENTANA_X = 1000
VENTANA_Y = 600 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


ventana = pg.display.set_mode((VENTANA_X, VENTANA_Y))
pg.display.set_caption("THE QUEST")
reloj = pg.time.Clock()


class Nave(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagen_nave = pg.image.load("images/navydef2.png")
        self.imagen_nave.set_colorkey(WHITE)
        self.velocidad = 3
        self.zona_impacto = (self.x, self.y, 83, 65)
        self.salud = 149

    def dibujar(self, cuadro):
        cuadro.blit(self.imagen_nave, (self.x, self.y))
        self.zona_impacto = (self.x, self.y, 83, 63)
        pg.draw.rect(cuadro, (WHITE), (400, 10, 155, 25))
        self.hp_roja = pg.draw.rect(cuadro, (255, 0, 0), (403, 13, 149, 19))
        self.hp_verde = pg.draw.rect(cuadro, (0, 120, 0), (403, 13, 50 - (1 * (50 - self.salud)), 19))

    def se_mueve_segun(self, k, arriba, abajo, espacio):
            if k[arriba] and self.y > 60:
                self.y -= self.velocidad
                if k[espacio]:
                    self.y -= 5
            if k[abajo] and self.y < 520:
                self.y += self.velocidad
                if k[espacio]:
                    self.y += 5
   
    def se_mueve_sola(self):
                if self.y < 250:
                    self.y +=1
                if self.y > 250:
                    self.y -=1        
                if self.x < 300:
                    self.x += 1  
                if self.x >= 300: 
                    self.imagen_nave = pg.transform.flip(pg.image.load("images/navydef2.png"), True, True)
                    self.imagen_nave.set_colorkey(WHITE)
                if self.x < 550:
                    self.x += 1

    def reinicio_nave(self):
        self.y = 300
        self.imagen_nave = pg.image.load("images/navydef2.png")
        self.imagen_nave.set_colorkey(WHITE)
        self.salud -= 50
        print(self.salud)

class Asteroide(object):
    def __init__(self, x, y, velocidad):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.imagen_asteroide = pg.image.load("sprites\steroid4.png")
        self.imagen_asteroide.set_colorkey(WHITE)
        self.zona_impacto = (self.x, self.y, 83, 65)

    def dibujar(self, cuadro):
        cuadro.blit(self.imagen_asteroide, (self.x, self.y))
        self.zona_impacto = (self.x, self.y, 73, 59)
        
    def se_mueve_segun(self):
        self.x -= self.velocidad
    
    def se_encuentra_con(self, alguien): #PARA VERIFICAR COLISIONES
        R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
        R1_ar = self.zona_impacto[1] 
        R1_iz = self.zona_impacto[0] 
        R1_de = self.zona_impacto[0] + self.zona_impacto[2]

        R2_ab = alguien.zona_impacto[1] + self.zona_impacto[3]
        R2_ar = alguien.zona_impacto[1] 
        R2_iz = alguien.zona_impacto[0] 
        R2_de = alguien.zona_impacto[0] + self.zona_impacto[2]

        return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

    def es_golpeado(self):
        self.colision = pg.mixer.Sound("music\colision.wav")
        self.colision.play()
        self.y = 700
        
class Planeta(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 2
        self.imagen_planeta = pg.image.load("images\planetstg3.png")


    def dibujar(self,cuadro):
        cuadro.blit(self.imagen_planeta, (self.x, self.y))

    def se_mueve_segun(self):
        if self.x >= 580:
            self.x -= self.velocidad
        if self.x < 580:
            nave.se_mueve_sola()
        

def repintar_cuadro_juego():
    if nivel <= nivel_max:
        ventana.blit(background[nivel], (0, 0))
    else:
        ventana.fill((0,0,0))

    nave.dibujar(ventana)
    planeta.dibujar(ventana)
    for ast in listaast:
        ast.dibujar(ventana)
    #TEXTOS
    puntos = texto_puntos.render("SCORE: " + str(puntaje), 1, (WHITE))
    nivel_actual = texto_nivel.render("Level: " + str(nivel + 1), 1, (255, 255, 255))
    ventana.blit(puntos, (10, 6))
    ventana.blit(nivel_actual, (420, 40))
    pg.display.update()

def subir_nivel():
    global nivel
    global nave
    global nivel_max
    global musica_fondo
    global planeta
    global ventana
    global playing
    global listaast
    global gana