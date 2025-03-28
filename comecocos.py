import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox


pygame.init()


MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)

pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA))
pygame.display.set_caption("Comecocos")


NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)


pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
velocidad = 10


mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 0, 0, 0, 2, 1, 0, 2, 0, 1, 0, 0, 2, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 2, 1, 0, 2, 0, 1, 0, 0, 0, 2, 0, 1, 0, 1, 1],
    [1, 2, 1, 2, 1, 0, 1, 0, 1, 0, 1, 2, 1, 2, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1],
    [1, 2, 1, 2, 0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 1, 2, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


def reiniciar_juego():
    """Restablece el estado del juego a sus valores iniciales."""
    global pac_x, pac_y, puntos, fan_x, fan_y
    pac_x, pac_y = 1, 1
    fan_x, fan_y = 10, 5
    puntos = 0


def mover_pacman(dx, dy):
    """Mueve el Pac-Man en la dirección dada y actualiza la recolección de puntos."""
    global pac_x, pac_y, puntos, fan_x, fan_y
   
    if 0 <= pac_x + dx < MAPA_ANCHO and 0 <= pac_y + dy < MAPA_ALTO:
        if mapa[pac_y + dy][pac_x + dx] != 1:  
            pac_x += dx
            pac_y += dy
           
            if mapa[pac_y][pac_x] == 2:
                puntos += 10
                mapa[pac_y][pac_x] = 0  # Eliminar el punto de esa celda


def mover_fantasma():
    """Mueve el fantasma de forma aleatoria en direcciones permitidas."""
    global fan_x, fan_y
  
    direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
    if direccion == 'arriba' and fan_y > 0 and mapa[fan_y - 1][fan_x] != 1:
        fan_y -= 1
    elif direccion == 'abajo' and fan_y < MAPA_ALTO-1 and mapa[fan_y + 1][fan_x] != 1:
        fan_y += 1
    elif direccion == 'izquierda' and fan_x > 0 and mapa[fan_y][fan_x - 1] != 1:
        fan_x -= 1
    elif direccion == 'derecha' and fan_x < MAPA_ANCHO-1 and mapa[fan_y][fan_x + 1] != 1:
        fan_x += 1


def mostrar_game_over():
    """Muestra la pantalla de Game Over y pregunta si el jugador quiere reiniciar."""
  
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont('Arial', 48)
    texto = fuente.render("Game Over", True, ROJO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.flip()

  
    pygame.time.wait(1000)
    preguntar_volver_a_jugar("¿Quieres volver a jugar?")


def preguntar_volver_a_jugar(mensaje):
    """Muestra un cuadro de diálogo preguntando si el jugador quiere volver a jugar."""
 
    root = tk.Tk()
    root.withdraw()  
    respuesta = messagebox.askyesno("Juego Terminado", mensaje)
    if respuesta:
        reiniciar_juego()
    else:
        pygame.quit()
        sys.exit()


def juego():
    global pac_x, pac_y, fan_x, fan_y, puntos
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

      
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            mover_pacman(-1, 0)
        if teclas[pygame.K_RIGHT]:
            mover_pacman(1, 0)
        if teclas[pygame.K_UP]:
            mover_pacman(0, -1)
        if teclas[pygame.K_DOWN]:
            mover_pacman(0, 1)

        
        mover_fantasma()

        
        if pac_x == fan_x and pac_y == fan_y:
            mostrar_game_over()

     
        pantalla.fill(BLANCO)  
        
      
        for y in range(MAPA_ALTO):
            for x in range(MAPA_ANCHO):
                if mapa[y][x] == 1: 
                    pygame.draw.rect(pantalla, AZUL, (x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                elif mapa[y][x] == 2:  
                    pygame.draw.circle(pantalla, AMARILLO, (x * TAMANO_CELDA + TAMANO_CELDA // 2, y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 5)
        

        pygame.draw.circle(pantalla, AMARILLO, (pac_x * TAMANO_CELDA + TAMANO_CELDA // 2, pac_y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
   
        pygame.draw.rect(pantalla, ROJO, (fan_x * TAMANO_CELDA, fan_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
        
        fuente = pygame.font.SysFont('Arial', 24)
        texto = fuente.render(f"Puntos: {puntos}", True, NEGRO)
        pantalla.blit(texto, (10, 10))

       
        pygame.display.flip()

        
        pygame.time.Clock().tick(velocidad)

    pygame.quit()
    sys.exit()


juego()
