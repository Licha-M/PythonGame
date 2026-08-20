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
ANCHO_PANTALLA = 1000
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
# Separacion minima en pixeles entre el borde derecho del ultimo enemigo
# spawneado y el punto donde aparecera el siguiente.
SEPARACION_MIN_ENEMIGOS = 400   # Minimo de separacion (pegados)
SEPARACION_MAX_ENEMIGOS = 800   # Maximo de separacion (alejados)

# Cantidad minima de enemigos que deben estar siempre en pantalla.
ENEMIGOS_MINIMOS = 2

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
# --- CONFIGURACION DE LA META (CUADRADO AMARILLO) ---
META_ANCHO = 50           # Ancho del cuadrado de la meta en pixeles
META_ALTO = 50             # Alto del cuadrado de la meta en pixeles
META_POS_Y = ALTO_PANTALLA - 220  # Posicion Y (vertical) de la meta en pantalla

enemigos = []           # Lista de enemigos en pantalla
# Posicion x del proximo spawn (se calcula al aparecer cada enemigo)
proximo_spawn_x = None  # None = calcular el primer spawn de inmediato

# --- BARRA DE ENERGIA ---
energia = 0.0           # Porcentaje actual (0-100)
energia_activa = False  # True cuando el jugador activó la barra con Shift

# --- ATAQUE ---
atacando = False            # True mientras se reproduce una animación de ataque
anim_ataque_actual = []     # Lista de frames del ataque en curso
frame_ataque = 0            # Frame actual del ataque
contador_ataque = 0         # Contador para cadencia de la animación de ataque

mostrar_menu = True
menu_opcion = 0  # 0 = Endless, 1 = Con Limites
menu_titulo = "Por definir"  # Texto del titulo del menu

# --- MUERTE ---
muriendo = False            # True mientras se reproduce la animacion de muerte
frame_muerte = 0            # Frame actual de la animacion de muerte
contador_muerte = 0         # Contador de cadencia de frames de muerte
pausa_post_muerte = 0       # Frames de pausa tras terminar la animacion (0 = no en pausa)

# --- DISTANCIA Y MODO ---
distancia = 0.0             # Metros recorridos (se muestra como entero)
META_DISTANCIA = 5000       # Distancia para ganar en modo limitado
modo_juego = 0              # 0 = Endless, 1 = Con Limites
meta_x = None               # Posicion x de la linea de meta
ganando = False             # True cuando el jugador choca la meta
contador_victoria = 0       # Tiempo de pausa tras ganar


# ---------- Funciones ----------

def dibujar_fondo(pantalla):
    """Dibuja el fondo usando la imagen Background-big.jpg y lo mueve en bucle."""
    global fondo_x
    
    # Mover el fondo solo si el juego esta activo (no menu, no muerte, no pausa, no ganando)
    if not mostrar_menu and not muriendo and pausa_post_muerte == 0 and not ganando:
        fondo_x -= VELOCIDAD_FONDO
        
        # Si el primer fondo sale por completo de la pantalla, reiniciar posicion
        if fondo_x <= -ANCHO_PANTALLA:
            fondo_x = 0
        
    # Dibujar dos fondos pegados para crear el bucle infinito
    pantalla.blit(fondo_imagen, (fondo_x, 0))
    pantalla.blit(fondo_imagen, (fondo_x + ANCHO_PANTALLA, 0))


def dibujar_menu(pantalla, fuente_titulo, fuente_opcion):
    """Muestra el menu principal centrado en la pantalla."""
    # Overlay semitransparente
    overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    pantalla.blit(overlay, (0, 0))

    cx = ANCHO_PANTALLA // 2
    cy = ALTO_PANTALLA // 2

    # --- Titulo (usa la variable global menu_titulo) ---
    txt_titulo = fuente_titulo.render(menu_titulo, True, (255, 220, 60))
    pantalla.blit(txt_titulo, (cx - txt_titulo.get_width() // 2, cy - 120))

    # --- Separador ---
    pygame.draw.line(pantalla, (200, 200, 200), (cx - 200, cy - 70), (cx + 200, cy - 70), 2)

    # --- Opciones ---
    opciones = ["Endless Mode", "Limited Mode"]
    for i, opcion in enumerate(opciones):
        y_opcion = cy - 20 + i * 60
        if i == menu_opcion:
            # Caja resaltada
            caja_rect = pygame.Rect(cx - 180, y_opcion - 8, 360, 44)
            pygame.draw.rect(pantalla, (255, 220, 60), caja_rect, border_radius=10)
            pygame.draw.rect(pantalla, (255, 255, 255), caja_rect, 2, border_radius=10)
            color_txt = (20, 20, 20)
        else:
            color_txt = (200, 200, 200)
        txt_op = fuente_opcion.render(opcion, True, color_txt)
        pantalla.blit(txt_op, (cx - txt_op.get_width() // 2, y_opcion))

    # --- Instruccion ---
    fuente_hint = pygame.font.SysFont("arial", 16)
    txt_hint = fuente_hint.render("\u2191 \u2193 para navegar  |  ENTER para seleccionar", True, (160, 160, 160))
    pantalla.blit(txt_hint, (cx - txt_hint.get_width() // 2, cy + 120))


def dibujar_muerte(pantalla):
    """Reproduce la animacion de muerte del personaje frame a frame.
    Cuando termina, activa la pausa post-muerte.
    Devuelve True mientras la animacion sigue activa."""
    global muriendo, frame_muerte, contador_muerte, pausa_post_muerte, personaje_y, velocidad_y

    # Si el personaje esta en el aire, hacerlo caer primero
    if personaje_y < y_suelo:
        personaje_y += velocidad_y
        velocidad_y += GRAVEDAD
        if personaje_y >= y_suelo:
            personaje_y = y_suelo
            velocidad_y = 0
        
        # Mostrar el primer frame de muerte mientras cae
        pantalla.blit(anim_muerte[0], (personaje_x, personaje_y))
        return True

    contador_muerte += 1
    if contador_muerte >= 5:   # Cadencia: 1 frame cada 5 ticks (~12 fps)
        contador_muerte = 0
        frame_muerte += 1
        if frame_muerte >= len(anim_muerte):
            # Animacion terminada
            muriendo = False
            pausa_post_muerte = FPS * 2  # 2 segundos de pausa
            return False

    if frame_muerte < len(anim_muerte):
        pantalla.blit(anim_muerte[frame_muerte], (personaje_x, personaje_y))
    return True


def reiniciar_juego(modo_seleccionado=0):
    """Reinicia todas las variables de estado del juego para una nueva partida."""
    global personaje_y, velocidad_y, esta_saltando, enemigos, proximo_spawn_x
    global energia, energia_activa, atacando, frame_actual
    global contador_anim, muriendo, frame_muerte, contador_muerte, pausa_post_muerte
    global fondo_x, distancia, modo_juego, meta_x, ganando, contador_victoria

    personaje_y   = y_suelo
    velocidad_y   = 0
    esta_saltando = False
    enemigos.clear()
    proximo_spawn_x = None  # Se recalcula al primer frame
    energia        = 0.0
    energia_activa = False
    atacando       = False
    frame_actual   = 0
    contador_anim  = 0
    muriendo       = False
    frame_muerte   = 0
    contador_muerte = 0
    pausa_post_muerte = 0
    fondo_x        = 0
    distancia      = 0.0
    modo_juego     = modo_seleccionado
    meta_x         = None
    ganando        = False
    contador_victoria = 0


def dibujar_distancia(pantalla, fuente_dist):
    """Dibuja el contador de distancia estilo dino de Google en la parte superior."""
    MARGEN      = 12
    ANCHO_CAJA  = 160
    ALTO_CAJA   = 28
    RADIO       = 6

    # Centrado horizontalmente
    cx = ANCHO_PANTALLA // 2
    dx = cx - ANCHO_CAJA // 2
    dy = MARGEN

    # Fondo y borde
    pygame.draw.rect(pantalla, (30, 30, 50), (dx, dy, ANCHO_CAJA, ALTO_CAJA), border_radius=RADIO)
    pygame.draw.rect(pantalla, (180, 180, 220), (dx, dy, ANCHO_CAJA, ALTO_CAJA), 2, border_radius=RADIO)

    # Texto
    txt = fuente_dist.render(f"{int(distancia):,} m".replace(",", "."), True, (255, 255, 255))
    lx = dx + (ANCHO_CAJA - txt.get_width()) // 2
    ly = dy + (ALTO_CAJA - txt.get_height()) // 2
    pantalla.blit(txt, (lx, ly))


def dibujar_personaje(pantalla):
    """Dibuja el avatar del personaje.
    Prioridad de animación: ganando > ataque > salto > correr."""
    global frame_actual, contador_anim, personaje_y, velocidad_y, esta_saltando
    global atacando, anim_ataque_actual, frame_ataque, contador_ataque

    # Física del salto (siempre se actualiza, incluso si está atacando o ganando)
    if esta_saltando or (ganando and personaje_y < y_suelo):
        personaje_y += velocidad_y
        velocidad_y += GRAVEDAD
        if personaje_y >= y_suelo:
            personaje_y = y_suelo
            esta_saltando = False
            frame_actual = 0
            contador_anim = 0

    if ganando and personaje_y >= y_suelo:
        # Animacion de victoria (IDLE)
        anim_actual = anim_idle
        contador_anim += 1
        if contador_anim >= 6:
            contador_anim = 0
            frame_actual = (frame_actual + 1) % len(anim_actual)
        
        imagen_actual = anim_actual[frame_actual]
        pantalla.blit(imagen_actual, (personaje_x, personaje_y))
        return None  # No hitbox needed

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
    """Spawnea un nuevo enemigo cuando el ultimo enemigo en pantalla llego
    al punto 'proximo_spawn_x'. Ese punto se calcula, en el momento en que
    UN enemigo nace en ANCHO_PANTALLA, restandole una separacion aleatoria
    (entre SEPARACION_MIN_ENEMIGOS y SEPARACION_MAX_ENEMIGOS) mas su ancho.
    Asi, cuando ese enemigo llega a esa posicion, ya dejo exactamente ese
    hueco libre detras suyo antes de que aparezca el siguiente."""
    import random
    global proximo_spawn_x

    if not enemigos:
        # No hay enemigos: spawnear directamente y calcular cuando ira el siguiente
        enemigos.append({'x': ANCHO_PANTALLA})
        separacion = random.randint(SEPARACION_MIN_ENEMIGOS, SEPARACION_MAX_ENEMIGOS)
        proximo_spawn_x = ANCHO_PANTALLA - separacion - Enemigo_ancho
        return

    # Encontrar el enemigo que esta mas a la derecha
    ultimo_x = max(e['x'] for e in enemigos)

    if proximo_spawn_x is None:
        # Salvaguarda por si esta variable no se calculo antes (no deberia pasar)
        separacion = random.randint(SEPARACION_MIN_ENEMIGOS, SEPARACION_MAX_ENEMIGOS)
        proximo_spawn_x = ultimo_x - separacion - Enemigo_ancho

    if ultimo_x <= proximo_spawn_x:
        # El ultimo enemigo ya dejo el hueco necesario: spawnear el siguiente
        enemigos.append({'x': ANCHO_PANTALLA})
        # Calcular cuando debe aparecer el que sigue despues de este
        separacion = random.randint(SEPARACION_MIN_ENEMIGOS, SEPARACION_MAX_ENEMIGOS)
        proximo_spawn_x = ANCHO_PANTALLA - separacion - Enemigo_ancho


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

    # Texto dentro de la barra: cambia segun el estado
    if energia_activa:
        label = fuente_barra.render("ACTIVA", True, (255, 255, 255))
    elif energia >= 100:
        label = fuente_barra.render("SHIFT para activar", True, (20, 20, 20))
    else:
        label = fuente_barra.render(f"{int(energia)}%", True, COLOR_BARRA_TEXTO)

    lx = bx + (ANCHO_BARRA - label.get_width()) // 2
    ly = by + (ALTO_BARRA - label.get_height()) // 2
    pantalla.blit(label, (lx, ly))


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
fuente_menu_titulo = pygame.font.SysFont("arial", 52, bold=True)
fuente_menu_opcion = pygame.font.SysFont("arial", 28)
fuente_dist        = pygame.font.SysFont("arial", 15, bold=True)


# Cargar tiras de imagenes y fondo
fondo_imagen = pygame.image.load("imgs/background/Background-big.jpg").convert()
fondo_imagen = pygame.transform.scale(fondo_imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
anim_correr  = cargar_animacion("imgs/sprites/RUN.png", 8)        # 8 cuadros
anim_saltar  = cargar_animacion("imgs/sprites/JUMP.png", 5)       # 5 cuadros
anim_ataque1 = cargar_animacion("imgs/sprites/ATTACK 1.png", 6)   # 6 cuadros
anim_ataque2 = cargar_animacion("imgs/sprites/ATTACK 2.png", 5)   # 5 cuadros
anim_ataque3 = cargar_animacion("imgs/sprites/ATTACK 3.png", 6)   # 6 cuadros
anim_muerte  = cargar_animacion("imgs/sprites/DEATH.png", 12)     # 12 cuadros
anim_idle    = cargar_animacion("imgs/sprites/IDLE.png", 7)       # 7 cuadros
# Fuente pequeña para la barra de energia
fuente_barra = pygame.font.SysFont("arial", 15, bold=True)
# Variables para controlar la animacion
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
            if mostrar_menu:
                if evento.key == pygame.K_UP:
                    menu_opcion = (menu_opcion - 1) % 2
                elif evento.key == pygame.K_DOWN:
                    menu_opcion = (menu_opcion + 1) % 2
                elif evento.key == pygame.K_RETURN:
                    if menu_opcion == 0:
                        # Endless Mode: reiniciar y comenzar
                        reiniciar_juego(0)
                        menu_titulo = "Por definir"
                        mostrar_menu = False
                    elif menu_opcion == 1:
                        # Limited Mode: reiniciar y comenzar
                        reiniciar_juego(1)
                        menu_titulo = "Por definir"
                        mostrar_menu = False
            elif not muriendo and pausa_post_muerte == 0 and not ganando:
                # Solo procesar inputs de juego si el personaje no esta muriendo ni ganando
                if evento.key in (pygame.K_SPACE, pygame.K_UP) and not esta_saltando:
                    # Iniciar el salto
                    esta_saltando = True
                    velocidad_y = FUERZA_SALTO
                    frame_actual = 0
                    contador_anim = 0
                elif evento.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    # Activar barra de energia solo si esta al 100 %
                    if energia >= 100 and not energia_activa:
                        energia_activa = True

    dibujar_fondo(pantalla)

    if mostrar_menu:
        dibujar_menu(pantalla, fuente_menu_titulo, fuente_menu_opcion)
    elif muriendo:
        # --- Animacion de muerte en curso ---
        dibujar_enemigos(pantalla)   # Mantener enemigos visibles pero quietos
        dibujar_muerte(pantalla)
    elif pausa_post_muerte > 0:
        # --- Pausa breve antes de volver al menu ---
        pausa_post_muerte -= 1
        # Dibujar personaje en el ultimo frame de muerte (posicion caido)
        pantalla.blit(anim_muerte[-1], (personaje_x, personaje_y))
        if pausa_post_muerte == 0:
            # Tiempo cumplido: mostrar menu de fin de juego
            mostrar_menu = True
            menu_titulo = "Fin del juego"
    elif ganando:
        # --- Animacion de victoria ---
        dibujar_personaje(pantalla)
        # Dibujar la meta amarilla (fija en el punto donde se choco)
        rect_meta = pygame.Rect(meta_x, META_POS_Y, META_ANCHO, META_ALTO)
        pygame.draw.rect(pantalla, (255, 220, 0), rect_meta)
        
        contador_victoria += 1
        if contador_victoria >= FPS * 3: # 3 segundos de idle
            mostrar_menu = True
            menu_titulo = "¡Ganaste!"
    else:
        # --- Juego normal ---
        # --- Logica de spawn por distancia aleatoria ---
        intentar_spawn_enemigo()

        # Garantizar minimo de enemigos en pantalla (spawn de emergencia)
        if len(enemigos) < ENEMIGOS_MINIMOS:
            # Forzar un spawn con separacion minima si no hay suficientes enemigos
            ultimo_x = max((e['x'] for e in enemigos), default=ANCHO_PANTALLA)
            nuevo_x = max(ANCHO_PANTALLA, ultimo_x + SEPARACION_MIN_ENEMIGOS + Enemigo_ancho)
            enemigos.append({'x': nuevo_x})
            # Mantener sincronizado el calculo del proximo spawn normal
            proximo_spawn_x = nuevo_x - SEPARACION_MIN_ENEMIGOS - Enemigo_ancho

        # Barra de energia: carga por salto exitoso
        saltaba_antes = esta_saltando

        mover_enemigos()
        rect_personaje = dibujar_personaje(pantalla)
        hitboxes_enemigos = dibujar_enemigos(pantalla)

        # Detectar aterrizaje exitoso -> +5% de energia
        if saltaba_antes and not esta_saltando and not energia_activa:
            energia = min(100.0, energia + 5.0)

        # --- Colision con enemigos ---
        enemigos_a_eliminar = []
        for i, hb in enumerate(hitboxes_enemigos):
            if rect_personaje.colliderect(hb):
                if energia_activa:
                    # MODO ATAQUE: eliminar enemigo (-10% de energia)
                    enemigos_a_eliminar.append(i)
                    energia -= 10.0
                    if energia <= 0:
                        energia = 0.0
                        energia_activa = False
                    if not atacando:
                        iniciar_ataque()
                else:
                    # MODO NORMAL: iniciar animacion de muerte
                    if not muriendo:
                        muriendo = True
                        frame_muerte = 0
                        contador_muerte = 0
                        enemigos.clear()   # Limpiar enemigos al morir
                    break               # Salir del loop para no procesar mas colisiones

        # Eliminar enemigos derrotados en modo ataque
        for i in sorted(enemigos_a_eliminar, reverse=True):
            if i < len(enemigos):
                enemigos.pop(i)

        # --- Sumar distancia recorrida (~10 m/s a 60 FPS) ---
        distancia += VELOCIDAD_FONDO * (10 / FPS)

        # --- Lógica de la meta en Modo Limitado ---
        if modo_juego == 1:
            distancia_restante = META_DISTANCIA - distancia
            # Spawnear la meta a ~200 metros (aprox 1200 pixeles de distancia)
            if distancia_restante <= 200 and meta_x is None:
                meta_x = ANCHO_PANTALLA
            
            if meta_x is not None:
                meta_x -= VELOCIDAD_FONDO
                rect_meta = pygame.Rect(meta_x, META_POS_Y, META_ANCHO, META_ALTO)
                pygame.draw.rect(pantalla, (255, 220, 0), rect_meta)
                
                # Check collision con la meta
                if rect_personaje and rect_personaje.colliderect(rect_meta):
                    ganando = True
                    enemigos.clear()
                    distancia = float(META_DISTANCIA)  # Clavar contador en 5000

        # --- Dibujar barra de energia y distancia ---
        if not muriendo:
            dibujar_barra_energia(pantalla, fuente_barra)
            dibujar_distancia(pantalla, fuente_dist)

        # Consigna 6 del proyecto: aca va el contador de kilometros restantes.

    pygame.display.flip()

pygame.quit()
sys.exit()
