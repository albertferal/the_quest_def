import pygame as pg  
import random

pg.init()
pg.mixer.init()

VENTANA_X = 1000
VENTANA_Y = 600 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


ventana = pg.display.set_mode((VENTANA_X, VENTANA_Y))
pg.display.set_caption("THE QUEST")
reloj = pg.time.Clock()


#CLASES
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

#SE ENCARGARÁ DE SUBIR NIVEL (1, 2 Y 3)
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

    nivel += 1 
    if nave.salud <=0:
        nivel = 3
    #texto subida de nivel:
    texto = pg.font.SysFont("Arial", 100)
    marcador = texto.render("", 1 ,(255, 0 ,0))
    ventana.blit(marcador, (250 -(marcador.get_width()//2), 200))
    pg.display.update()
    pg.time.delay(2000)

    #verifica si pasó el último lvl
    #en caso de pasar el último, termina el juego y termina el ciclo (playing)
    if nivel > nivel_max and nave.salud > 0:
        pg.mixer.music.stop()
        pg.mixer.music.load("music/victory.wav")
        pg.mixer.music.play(-1)
        playing = False
        gana = True
    
    #en caso de perder, se actualiza musica y pantalla
    elif nivel > nivel_max and nave.salud <0:
        
        pg.mixer.music.stop()
        pg.mixer.music.load("music\gosong.wav")
        pg.mixer.music.play(-1)
        playing = False
        gana = True
    
    #en caso de pasar un nivel intermedio, se actualiza la música y todo al nuevo nivel:
    else: 
        nave = naves[nivel]
        planeta = planetas[nivel]
        listaast = []
        for i in range(45):
            listaast.append(Asteroide(random.randint(500, 7500), random.randint(50, 550), random.randint(5,6)))
        pg.mixer.music.stop()
        musica_fondo = pg.mixer.music.load(rutamusica[nivel])
        pg.mixer.music.play(-1) 

repetir = True 
while repetir:

    listaast = []
    for i in range(40):
        listaast.append(Asteroide(random.randint(500, 4500), random.randint(50, 550), random.randint(3,4)))


    #INICIAMOS ELEMENTOS JUEGO:
    nivel = 0
    nivel_max = 2
    background = [pg.image.load("images/backgroundstg1.jpg"), pg.image.load("images/backgroundstg2.jpg"), 
                  pg.image.load("images/backgroundstg3.jpg")]
    #AGREGAMOS MUSICAb
    rutamusica = ["music\MSTAGE1.wav", "music\MSTAGE2.wav", "music\MSTAGE3.wav"]
    musica_fondo = pg.mixer.music.load(rutamusica[nivel])
    pg.mixer.music.play(-1)

    puntaje = 0
    texto_juego = pg.font.SysFont("console", 80, True)
    texto_puntos = pg.font.SysFont("Arial", 30, True)
    texto_nivel = pg.font.SysFont("Arial", 30, True)
    texto_intro = pg.font.SysFont("console", 40, True)
    texto_resultado = pg.font.SysFont("console", 80, True)
    texto_comandos = pg.font.SysFont("console", 20, True)
    esta_en_intro = True
    gana = False
    
    #CREACION OBJETOS:
    naves = [Nave(30, 300), Nave(30, 300), Nave(30, 300)]
    nave = naves[nivel]
    planetas = [Planeta(4000, -100), Planeta(4000, -100), Planeta(4000, -100)]
    planeta = planetas[nivel]

    while esta_en_intro:
        reloj.tick(60)
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                quit()
        backgroundmm = pg.image.load("images/backgroundintro.jpg")
        ventana.blit(backgroundmm, (0, 0))
        titulo = texto_juego.render("THE QUEST", 1, (255, 0, 0))
        instrucciones = texto_intro.render("Presiona ENTER para empezar a jugar", 1, (255, 255, 255))
        comandos = texto_comandos.render("Mantén pulsado ARRIBA o ABAJO para mover la nave", 1, (255, 255, 255))
        comandos2 = texto_comandos.render("Presiona la tecla SPACE para aumentar la velocidad", 1, (255, 255, 255))
        ventana.blit(titulo, ((VENTANA_X // 2) - (titulo.get_width() // 2), 50))
        ventana.blit(instrucciones, ((VENTANA_X // 2) - (instrucciones.get_width() // 2), 530))
        ventana.blit(comandos, ((VENTANA_X // 2) - (instrucciones.get_width() // 2), 470))
        ventana.blit(comandos2, ((VENTANA_X // 2) - (instrucciones.get_width() // 2), 500))

        tecla = pg.key.get_pressed()

        if tecla[pg.K_RETURN]:
            esta_en_intro = False
            playing = True
        
        pg.display.update()



    #SECCION DEL JUEGO
    playing = True
    while playing:
        reloj.tick(60)
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                quit()
        #EVENTO MVOIMIENTO PJ
        teclas = pg.key.get_pressed()
        if nave.x <= 30:
            nave.se_mueve_segun(teclas, pg.K_UP, pg. K_DOWN, pg.K_SPACE)
        planeta.se_mueve_segun()
        for ast in listaast:
            ast.se_mueve_segun()
            puntaje += 1
            #VERIFICAR CHOQUE:
            if ast.se_encuentra_con(nave):
                ast.es_golpeado() 
                puntaje -= 10000
                nave.reinicio_nave()
        #consulta para saber si se sube de nivel
        if nave.x >= 550:
            subir_nivel()
        if nave.salud <= 0:
            subir_nivel()
            gana = False

        repintar_cuadro_juego()
    
    #SECCIÓN PANTALLA FINAL:
    final = True
    while final:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                quit()
        ventana.fill((0, 0, 0))
        titulo = texto_intro.render("JUEGO TERMINADO", 1, (255, 0, 0))
        if gana:
            resultado = texto_resultado.render("HAS GANADO", 1, (255, 0, 0))
        else:
            resultado = texto_resultado.render("HAS PERDIDO", 1, (255, 255, 255))
        pts = texto_intro.render("Puntuación total: " + str(puntaje), 1, (255, 255, 255))
        instrucciones = texto_intro.render("Presione ENTER para cerrar", 1, (255, 255, 255))
        reintentar = texto_intro.render("Presione R para volver al inicio", 1, (255, 255, 255))
        ventana.blit(titulo, (VENTANA_X//2 - titulo.get_width() // 2, 10))
        ventana.blit(resultado, (VENTANA_X//2 - resultado.get_width() // 2, 250))
        ventana.blit(pts, (VENTANA_X//2 - pts.get_width() // 2, 100))
        ventana.blit(instrucciones, (VENTANA_X//2 - instrucciones.get_width() // 2, 450))
        ventana.blit(reintentar, (VENTANA_X//2 - reintentar.get_width() // 2, 500))
        pg.display.update()

        tecla = pg.key.get_pressed()
        if tecla [pg.K_RETURN]:
            repetir = False
            final = False
        if tecla[pg.K_r]:
            repetir = True
            final = False
     
pg.quit()