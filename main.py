import pygame as pg  
import random
from clases import Nave, Asteroide, Planeta
from scores import *


pg.init()
pg.mixer.init()

VENTANA_X = 1000
VENTANA_Y = 600 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ventana = pg.display.set_mode((VENTANA_X, VENTANA_Y))
pg.display.set_caption("THE QUEST")
reloj = pg.time.Clock()

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
    puntos = texto_puntos.render("SCORE: " + str(score), 1, (WHITE))
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

    score = 0
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
            score += 1
            #VERIFICAR CHOQUE:
            if ast.se_encuentra_con(nave):
                ast.es_golpeado() 
                score -= 10000
                nave.reinicio_nave()
        #consulta para saber si se sube de nivel
        if planeta.x <= 700:
            nave.se_mueve_sola()
            if nave.x >=550:
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
        name = "lol"
        pts = texto_intro.render("Puntuación total: " + str(score), 1, (255, 255, 255))
        insertRow(name, score)
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