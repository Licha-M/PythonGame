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

# ---------- Constantes ----------
ANCHO_PANTALLA = 1300
ALTO_PANTALLA = 500
FPS = 60

COLOR_ENEMIGO = (220, 40, 40)
COLOR_TEXTO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ALERTA = (255, 60, 60)
COLOR_HITBOX = (0, 0, 255)  # Color azul para las hitboxes

# --- COLORES DE LA BARRA DE ENERGIA ---
COLOR_BARRA_FONDO   = (40, 40, 60)       # Fondo oscuro de la barra
COLOR_BARRA_BORDE   = (180, 180, 220)     # Borde plateado
COLOR_BARRA_LLENA   = (255, 210, 0)       # Dorado cuando está al 100 %
COLOR_BARRA_NORMAL  = (80, 200, 120)      # Verde mientras se carga
COLOR_BARRA_ACTIVA  = (255, 80, 30)       # Naranja/rojo mientras se gasta
COLOR_BARRA_TEXTO   = (255, 255, 255)

# --- AJUSTES DE HITBOX (Márgenes internos para mayor precisión de colisión) ---
PERSONAJE_HITBOX_OFFSET_X = 45  # Píxeles a recortar a la izquierda y derecha
PERSONAJE_HITBOX_OFFSET_Y = 45  # Píxeles a recortar arriba y abajo

ENEMIGO_HITBOX_OFFSET_X = 0      # Píxeles a recortar a los lados
ENEMIGO_HITBOX_OFFSET_Y = 0       # Píxeles a recortar arriba y abajo

VELOCIDAD_ENEMIGO = 8
VELOCIDAD_FONDO = 2

# --- AJUSTES DE APARICION DE ENEMIGOS ---
# Distancia mínima (en píxeles) que debe haber entre el borde derecho de un
# enemigo existente y el borde derecho de la pantalla antes de poder spawnear
# uno nuevo. Aumentar este valor separa más a los enemigos entre sí.
DISTANCIA_MINIMA_ENTRE_ENEMIGOS = 400

# Intervalo aleatorio de spawn: cada vez que se puede spawnear un enemigo, se
# espera entre MIN y MAX frames antes de intentarlo de nuevo.
SPAWN_INTERVALO_MIN = 60   # frames mínimos entre intentos (~1 seg a 60 FPS)
SPAWN_INTERVALO_MAX = 180  # frames máximos entre intentos (~3 seg a 60 FPS)

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

# Lista de enemigos activos. Cada enemigo es un diccionario con claves 'x' e 'y'.
Enemigo_y = ALTO_PANTALLA - 220
Enemigo_ancho = 50
Enemigo_alto = 50

enemigos = []           # Lista de enemigos en pantalla
spawn_contador = 0      # Cuenta frames hasta el próximo intento de spawn
spawn_espera = SPAWN_INTERVALO_MIN  # Espera inicial antes del primer spawn

# --- BARRA DE ENERGIA ---
energia = 0.0           # Porcentaje actual (0-100)
energia_activa = False  # True cuando el jugador activó la barra con Shift

# --- ATAQUE ---
atacando = False            # True mientras se reproduce una animación de ataque
anim_ataque_actual = []     # Lista de frames del ataque en curso
frame_ataque = 0            # Frame actual del ataque
contador_ataque = 0         # Contador para cadencia de la animación de ataque

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
    """Dibuja el avatar del personaje.
    Prioridad de animación: ataque > salto > correr."""
    global frame_actual, contador_anim, personaje_y, velocidad_y, esta_saltando
    global atacando, anim_ataque_actual, frame_ataque, contador_ataque

    # Física del salto (siempre se actualiza, incluso si está atacando)
    if esta_saltando:
        personaje_y += velocidad_y
        velocidad_y += GRAVEDAD
        if personaje_y >= y_suelo:
            personaje_y = y_suelo
            esta_saltando = False
            frame_actual = 0
            contador_anim = 0

    # ---- Animación de ataque (tiene prioridad sobre correr/saltar) ----
    if atacando:
        contador_ataque += 1
        if contador_ataque >= 4:          # Cadencia: avanza frame cada 4 ticks
            contador_ataque = 0
            frame_ataque += 1
            if frame_ataque >= len(anim_ataque_actual):
                frame_ataque = 0
                atacando = False          # Animación completada

        if atacando:                      # Puede haberse desactivado arriba
            imagen_actual = anim_ataque_actual[frame_ataque]
            pantalla.blit(imagen_actual, (personaje_x, personaje_y))
            rect_personaje = pygame.Rect(
                personaje_x + PERSONAJE_HITBOX_OFFSET_X,
                personaje_y + PERSONAJE_HITBOX_OFFSET_Y,
                imagen_actual.get_width() - (PERSONAJE_HITBOX_OFFSET_X * 2),
                imagen_actual.get_height() - (PERSONAJE_HITBOX_OFFSET_Y * 2)
            )
            pygame.draw.rect(pantalla, COLOR_HITBOX, rect_personaje, 2)
            return rect_personaje

    # ---- Animación normal (correr / saltar) ----
    anim_actual = anim_saltar if esta_saltando else anim_correr
    contador_anim += 1
    if contador_anim >= 4:
        contador_anim = 0
        frame_actual += 1
        if frame_actual >= len(anim_actual):
            frame_actual = len(anim_actual) - 1 if esta_saltando else 0

    if frame_actual >= len(anim_actual):
        frame_actual = 0

    imagen_actual = anim_actual[frame_actual]
    pantalla.blit(imagen_actual, (personaje_x, personaje_y))

    rect_personaje = pygame.Rect(
        personaje_x + PERSONAJE_HITBOX_OFFSET_X,
        personaje_y + PERSONAJE_HITBOX_OFFSET_Y,
        imagen_actual.get_width() - (PERSONAJE_HITBOX_OFFSET_X * 2),
        imagen_actual.get_height() - (PERSONAJE_HITBOX_OFFSET_Y * 2)
    )
    pygame.draw.rect(pantalla, COLOR_HITBOX, rect_personaje, 2)
    return rect_personaje


def dibujar_enemigos(pantalla):
    """Dibuja todos los enemigos activos y devuelve la lista de sus hitboxes.
    Consigna 1 del proyecto: reemplazar el rectángulo rojo por una imagen real."""
    hitboxes = []
    for enemigo in enemigos:
        # Rectángulo para la representación visual (tamaño completo)
        rect_visual = pygame.Rect(enemigo['x'], Enemigo_y, Enemigo_ancho, Enemigo_alto)
        pygame.draw.rect(pantalla, COLOR_ENEMIGO, rect_visual)

        # Rectángulo real de colisión (hitbox reducida)
        rect_hitbox = pygame.Rect(
            enemigo['x'] + ENEMIGO_HITBOX_OFFSET_X,
            Enemigo_y + ENEMIGO_HITBOX_OFFSET_Y,
            Enemigo_ancho - (ENEMIGO_HITBOX_OFFSET_X * 2),
            Enemigo_alto - (ENEMIGO_HITBOX_OFFSET_Y * 2)
        )

        # Dibujar la hitbox con un contorno azul (grosor 5)
        pygame.draw.rect(pantalla, COLOR_HITBOX, rect_hitbox, 5)
        hitboxes.append(rect_hitbox)
    return hitboxes


def mover_enemigos():
    """Mueve todos los enemigos hacia la izquierda y elimina los que salen
    de la pantalla por el lado izquierdo."""
    for enemigo in enemigos:
        enemigo['x'] -= VELOCIDAD_ENEMIGO
    # Eliminar enemigos que salieron completamente de la pantalla
    enemigos[:] = [e for e in enemigos if e['x'] > -Enemigo_ancho]


def intentar_spawn_enemigo():
    """Intenta agregar un nuevo enemigo a la derecha de la pantalla.
    Solo lo hace si ningún enemigo activo está a menos de DISTANCIA_MINIMA_ENTRE_ENEMIGOS
    píxeles del borde derecho. Devuelve la cantidad de frames a esperar hasta
    el próximo intento."""
    import random

    # Verificar si algún enemigo está demasiado cerca del borde derecho
    demasiado_cerca = any(
        e['x'] > ANCHO_PANTALLA - DISTANCIA_MINIMA_ENTRE_ENEMIGOS
        for e in enemigos
    )

    if not demasiado_cerca:
        enemigos.append({'x': ANCHO_PANTALLA})

    # Devolver el próximo intervalo de espera (aleatorio)
    return random.randint(SPAWN_INTERVALO_MIN, SPAWN_INTERVALO_MAX)


def cargar_animacion(ruta_imagen, cantidad_frames):
    """Carga un sprite sheet y devuelve la lista de frames escalados a 175x175."""
    sheet = pygame.image.load(ruta_imagen).convert_alpha()
    ancho_frame = sheet.get_width() // cantidad_frames
    alto_frame = sheet.get_height()
    frames = []
    for i in range(cantidad_frames):
        frame = sheet.subsurface((i * ancho_frame, 0, ancho_frame, alto_frame))
        frame = pygame.transform.scale(frame, (175, 175))
        frames.append(frame)
    return frames


def dibujar_barra_energia(pantalla, fuente_barra):
    """Dibuja la barra de energía en la esquina superior derecha."""
    MARGEN       = 12          # Separación del borde de pantalla
    ANCHO_BARRA  = 220
    ALTO_BARRA   = 28
    RADIO        = 6           # Bordes redondeados

    bx = ANCHO_PANTALLA - ANCHO_BARRA - MARGEN
    by = MARGEN

    # Fondo y borde
    pygame.draw.rect(pantalla, COLOR_BARRA_FONDO, (bx, by, ANCHO_BARRA, ALTO_BARRA), border_radius=RADIO)
    pygame.draw.rect(pantalla, COLOR_BARRA_BORDE, (bx, by, ANCHO_BARRA, ALTO_BARRA), 2, border_radius=RADIO)

    # Relleno según el estado
    fill_w = int(ANCHO_BARRA * energia / 100)
    if fill_w > 0:
        if energia_activa:
            color_fill = COLOR_BARRA_ACTIVA
        elif energia >= 100:
            color_fill = COLOR_BARRA_LLENA
        else:
            color_fill = COLOR_BARRA_NORMAL
        pygame.draw.rect(pantalla, color_fill, (bx, by, fill_w, ALTO_BARRA), border_radius=RADIO)

    # Texto de porcentaje centrado
    pct_txt = fuente_barra.render(f"{int(energia)}%", True, COLOR_BARRA_TEXTO)
    tx = bx + (ANCHO_BARRA - pct_txt.get_width()) // 2
    ty = by + (ALTO_BARRA - pct_txt.get_height()) // 2
    pantalla.blit(pct_txt, (tx, ty))

    # Indicador parpadeante "ACTIVA" cuando la barra funciona
    if energia_activa:
        ind = fuente_barra.render("⚡ ACTIVA", True, COLOR_BARRA_ACTIVA)
        pantalla.blit(ind, (bx, by + ALTO_BARRA + 4))
    elif energia >= 100:
        ind = fuente_barra.render("▶ SHIFT para activar", True, COLOR_BARRA_LLENA)
        pantalla.blit(ind, (bx - 60, by + ALTO_BARRA + 4))


def iniciar_ataque():
    """Selecciona aleatoriamente una de las 3 animaciones de ataque y
    comienza a reproducirla."""
    global atacando, anim_ataque_actual, frame_ataque, contador_ataque
    import random
    anim_ataque_actual = random.choice([anim_ataque1, anim_ataque2, anim_ataque3])
    frame_ataque   = 0
    contador_ataque = 0
    atacando       = True


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
anim_correr  = cargar_animacion("imgs/sprites/RUN.png", 8)        # 8 cuadros
anim_saltar  = cargar_animacion("imgs/sprites/JUMP.png", 5)       # 5 cuadros
anim_ataque1 = cargar_animacion("imgs/sprites/ATTACK 1.png", 6)   # 6 cuadros
anim_ataque2 = cargar_animacion("imgs/sprites/ATTACK 2.png", 5)   # 5 cuadros
anim_ataque3 = cargar_animacion("imgs/sprites/ATTACK 3.png", 6)   # 6 cuadros
# Fuente pequeña para la barra de energía
fuente_barra = pygame.font.SysFont("arial", 15, bold=True)
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
            elif evento.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                # Activar barra de energía solo si está al 100 %
                if energia >= 100 and not energia_activa:
                    energia_activa = True

    dibujar_fondo(pantalla)

    if mostrar_reglas:
        dibujar_reglas(pantalla, fuente)
    else:
        # --- Lógica de spawn con intervalo aleatorio ---
        spawn_contador += 1
        if spawn_contador >= spawn_espera:
            spawn_espera = intentar_spawn_enemigo()
            spawn_contador = 0

        # --- Barra de energía: carga por salto exitoso ---
        # Se detecta cuando el personaje acaba de aterrizar (esta_saltando
        # pasó de True a False). Lo manejamos con un flag.
        saltaba_antes = esta_saltando

        mover_enemigos()
        rect_personaje = dibujar_personaje(pantalla)
        hitboxes_enemigos = dibujar_enemigos(pantalla)

        # Detectar aterrizaje exitoso → +5 % de energía
        if saltaba_antes and not esta_saltando and not energia_activa:
            energia = min(100.0, energia + 5.0)

        # --- Colisión con enemigos ---
        enemigos_a_eliminar = []
        for i, hb in enumerate(hitboxes_enemigos):
            if rect_personaje.colliderect(hb):
                if energia_activa:
                    # MODO ATAQUE: eliminar enemigo (-10 % de energía) y reproducir animación
                    enemigos_a_eliminar.append(i)
                    energia -= 10.0
                    if energia <= 0:
                        energia = 0.0
                        energia_activa = False   # Se agotó → desactivar
                    if not atacando:
                        iniciar_ataque()
                else:
                    # MODO NORMAL: mostrar aviso de choque
                    texto_choque = fuente_grande.render("CHOQUE!", True, COLOR_ALERTA)
                    pantalla.blit(texto_choque, (ANCHO_PANTALLA // 2 - 60, 90))

        # Eliminar enemigos derrotados (de mayor a menor índice para no desplazar)
        for i in sorted(enemigos_a_eliminar, reverse=True):
            if i < len(enemigos):
                enemigos.pop(i)

        # --- Dibujar barra de energía ---
        dibujar_barra_energia(pantalla, fuente_barra)

        # Consigna 6 del proyecto: acá va el contador de kilometros restantes.

    pygame.display.flip()

pygame.quit()
sys.exit()
