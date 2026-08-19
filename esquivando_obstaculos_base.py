# ==========================================================
# Proyecto: Esquivando Obstaculos en la Ciudad
# Materia: Programacion en Python
# Colegio: Institucion Educativa Sagrado Corazon de Jesus
# Codigo base v1.0
#
# Descripcion: juego base 2D donde un personaje debe esquivar
# Enemigos en un escenario urbano. Este es el punto de partida
# del proyecto: a partir de aca cada grupo agrega las consignas
# (imagenes propias, salto, animacion de fondo, barra de
# energia, contador de kilometros, mensajes de fin de juego, etc.)
# ==========================================================

# ---------- Librerias ----------
import pygame
import sys
import os

# ---------- Constantes ----------
ANCHO_PANTALLA = 1300
ALTO_PANTALLA = 500
FPS = 60

COLOR_ENEMIGO = (220, 40, 40)
COLOR_TEXTO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ALERTA = (255, 60, 60)
COLOR_HITBOX = (0, 0, 255)  # Color azul para las hitboxes

# --- AJUSTES DE HITBOX (Márgenes internos para mayor precisión de colisión) ---
PERSONAJE_HITBOX_OFFSET_X = 45  # Píxeles a recortar a la izquierda y derecha
PERSONAJE_HITBOX_OFFSET_Y = 45  # Píxeles a recortar arriba y abajo

ENEMIGO_HITBOX_OFFSET_X = 0      # Píxeles a recortar a los lados
ENEMIGO_HITBOX_OFFSET_Y = 0       # Píxeles a recortar arriba y abajo

VELOCIDAD_ENEMIGO = 6
VELOCIDAD_FONDO = 2

# ---------- Variables globales ----------
personaje_x = 60
personaje_y = ALTO_PANTALLA - 300
fondo_x = 0

# Variables físicas para el salto
esta_saltando = False
velocidad_y = 0
GRAVEDAD = 0.7
FUERZA_SALTO = -16
y_suelo = personaje_y

Enemigo_x = ANCHO_PANTALLA
Enemigo_y = ALTO_PANTALLA - 220
Enemigo_ancho = 80
Enemigo_alto = 80

mostrar_reglas = True


# ---------- Funciones ----------

def dibujar_fondo(pantalla):
    """Dibuja el fondo usando la imagen Background-big.jpg y lo mueve en bucle."""
    global fondo_x
    
    # Mover el fondo hacia la izquierda solo si ya comenzó el juego (no se muestran las reglas)
    if not mostrar_reglas:
        fondo_x -= VELOCIDAD_FONDO
        
        # Si el primer fondo sale por completo de la pantalla, reiniciar posición
        if fondo_x <= -ANCHO_PANTALLA:
            fondo_x = 0
        
    # Dibujar dos fondos pegados para crear el bucle infinito
    pantalla.blit(fondo_imagen, (fondo_x, 0))
    pantalla.blit(fondo_imagen, (fondo_x + ANCHO_PANTALLA, 0))


def dibujar_reglas(pantalla, fuente):
    """Muestra el cartel de reglas al inicio del juego."""
    texto1 = fuente.render("Esquivando Obstaculos en la Ciudad", True, COLOR_TEXTO)
    texto2 = fuente.render("Presiona una tecla para comenzar", True, COLOR_TEXTO)
    caja = pygame.Rect(0, 0, ANCHO_PANTALLA, 70)
    pygame.draw.rect(pantalla, COLOR_NEGRO, caja)
    pantalla.blit(texto1, (20, 15))
    pantalla.blit(texto2, (20, 40))


def dibujar_personaje(pantalla):
    """Dibuja el avatar del personaje usando el sprite animado (correr o saltar)."""
    global frame_actual, contador_anim, personaje_y, velocidad_y, esta_saltando
    
    # Física del salto
    if esta_saltando:
        personaje_y += velocidad_y
        velocidad_y += GRAVEDAD
        # Si toca o pasa el nivel del suelo, termina el salto
        if personaje_y >= y_suelo:
            personaje_y = y_suelo
            esta_saltando = False
            frame_actual = 0
            contador_anim = 0
            
    # Seleccionar la animación correcta
    anim_actual = anim_saltar if esta_saltando else anim_correr
    
    # Actualizamos el frame de la animación
    contador_anim += 1
    if contador_anim >= 4:
        contador_anim = 0
        frame_actual += 1
        if frame_actual >= len(anim_actual):
            if esta_saltando:
                # Durante el salto, mantenemos el último frame hasta tocar el suelo
                frame_actual = len(anim_actual) - 1
            else:
                frame_actual = 0
                
    # Evitar índice fuera de rango al cambiar de animación
    if frame_actual >= len(anim_actual):
        frame_actual = 0
            
    # Obtenemos la imagen del frame actual
    imagen_actual = anim_actual[frame_actual]
    
    # Dibujamos la imagen en la pantalla
    pantalla.blit(imagen_actual, (personaje_x, personaje_y))
    
    # Retornamos el rectángulo de colisión con los offsets (márgenes) aplicados
    rect_personaje = pygame.Rect(
        personaje_x + PERSONAJE_HITBOX_OFFSET_X,
        personaje_y + PERSONAJE_HITBOX_OFFSET_Y,
        imagen_actual.get_width() - (PERSONAJE_HITBOX_OFFSET_X * 2),
        imagen_actual.get_height() - (PERSONAJE_HITBOX_OFFSET_Y * 2)
    )
    
    # Dibujar la hitbox del personaje con un contorno azul (grosor 2)
    pygame.draw.rect(pantalla, COLOR_HITBOX, rect_personaje, 2)
    
    return rect_personaje


def dibujar_Enemigo(pantalla):
    """Dibuja el Enemigo que se desplaza hacia el personaje (por ahora, un
    rectangulo rojo). Consigna 1 del proyecto: reemplazar por una imagen
    de Enemigo real."""
    # Rectángulo para la representación visual (tamaño completo)
    rect_visual = pygame.Rect(Enemigo_x, Enemigo_y, Enemigo_ancho, Enemigo_alto)
    pygame.draw.rect(pantalla, COLOR_ENEMIGO, rect_visual)
    
    # Rectángulo real de colisión (hitbox reducida)
    rect_hitbox = pygame.Rect(
        Enemigo_x + ENEMIGO_HITBOX_OFFSET_X,
        Enemigo_y + ENEMIGO_HITBOX_OFFSET_Y,
        Enemigo_ancho - (ENEMIGO_HITBOX_OFFSET_X * 2),
        Enemigo_alto - (ENEMIGO_HITBOX_OFFSET_Y * 2)
    )
    
    # Dibujar la hitbox del Enemigo con un contorno azul (grosor 5)
    pygame.draw.rect(pantalla, COLOR_HITBOX, rect_hitbox, 5)
    
    return rect_hitbox


def mover_Enemigo():
    """Mueve el Enemigo hacia la izquierda. Si sale de la pantalla por el lado
    izquierdo, vuelve a aparecer del lado derecho (consigna 4 del proyecto)."""
    global Enemigo_x
    Enemigo_x -= VELOCIDAD_ENEMIGO
    if Enemigo_x < -Enemigo_ancho:
        Enemigo_x = ANCHO_PANTALLA


def cargar_animacion(ruta_imagen, cantidad_frames):
    # Carga la imagen manteniendo la transparencia PNG
    sheet = pygame.image.load(ruta_imagen).convert_alpha()
    ancho_frame = sheet.get_width() // cantidad_frames
    alto_frame = sheet.get_height()
    
    frames = []
    for i in range(cantidad_frames):
        # Recorta cada recuadro (x, y, ancho, alto)
        frame = sheet.subsurface((i * ancho_frame, 0, ancho_frame, alto_frame))
        frame = pygame.transform.scale(frame, (175, 175)) 
        frames.append(frame)
    return frames


# ---------- Bloque de inicializacion ----------
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Esquivando Obstaculos en la Ciudad")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 20)
fuente_grande = pygame.font.SysFont("arial", 32, bold=True)


# Cargar tiras de imágenes y fondo
fondo_imagen = pygame.image.load("imgs/background/Background-big.jpg").convert()
fondo_imagen = pygame.transform.scale(fondo_imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
anim_correr = cargar_animacion("imgs/sprites/RUN.png", 8)   # 8 cuadros
anim_saltar = cargar_animacion("imgs/sprites/JUMP.png", 5)  # 5 cuadros
# Variables para controlar la animación
frame_actual = 0
contador_anim = 0


# ---------- Bloque principal ----------
juego_activo = True
while juego_activo:
    reloj.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_activo = False
        if evento.type == pygame.KEYDOWN:
            if mostrar_reglas:
                mostrar_reglas = False
            elif evento.key == pygame.K_SPACE and not esta_saltando:
                # Iniciar el salto
                esta_saltando = True
                velocidad_y = FUERZA_SALTO
                frame_actual = 0
                contador_anim = 0

    dibujar_fondo(pantalla)

    if mostrar_reglas:
        dibujar_reglas(pantalla, fuente)
    else:
        mover_Enemigo()
        rect_personaje = dibujar_personaje(pantalla)
        rect_Enemigo = dibujar_Enemigo(pantalla)

        # Deteccion simple de colision. Consigna 7 del proyecto:
        # reemplazar este aviso por el texto "JUEGO TERMINADO" pausando
        # el juego.
        if rect_personaje.colliderect(rect_Enemigo):
            texto_choque = fuente_grande.render("CHOQUE!", True, COLOR_ALERTA)
            pantalla.blit(texto_choque, (ANCHO_PANTALLA // 2 - 60, 90))

        # Consigna 5 del proyecto: acá va la barra de energia (60 segundos).
        # Consigna 6 del proyecto: acá va el contador de kilometros restantes.

    pygame.display.flip()

pygame.quit()
sys.exit()
