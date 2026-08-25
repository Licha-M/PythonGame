# Far, Far Away

Un juego de acción de desplazamiento lateral en 2D construido con Python y Pygame, desarrollado como proyecto escolar en la **Institución Educativa Sagrado Corazón de Jesús**. El jugador controla a un personaje que debe esquivar y derrotar enemigos a lo largo de un paisaje urbano en desplazamiento continuo, con dos modos de juego distintos y un conjunto completo de animaciones.

> Versión en inglés: [README.md](../../README.md)

---

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Características](#características)
- [Jugabilidad](#jugabilidad)
  - [Controles](#controles)
  - [Modos de juego](#modos-de-juego)
  - [Barra de energía](#barra-de-energía)
  - [Enemigos](#enemigos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Assets](#assets)
- [Detalles técnicos](#detalles-técnicos)
  - [Sistema de físicas](#sistema-de-físicas)
  - [Generación de enemigos](#generación-de-enemigos)
  - [Detección de colisiones](#detección-de-colisiones)
  - [Sistema de animaciones](#sistema-de-animaciones)
- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Configuración](#configuración)
- [Uso de IA](#uso-de-ia)
- [Licencia](#licencia)

---

## Descripción general

**Far, Far Away** es un juego de tipo runner/lucha en desplazamiento lateral donde el personaje corre por un fondo urbano que se mueve de forma continua y debe sobrevivir a los enemigos que vienen desde la derecha. Los jugadores pueden saltar sobre los enemigos o activar un modo de energía para destruirlos al contacto. El juego registra la distancia recorrida en metros y ofrece un modo de distancia limitada cuyo objetivo es llegar a la línea de meta.

El proyecto fue desarrollado como ejercicio educativo en programación de videojuegos con Python, abarcando temas como animación con sprite sheets, simulación de físicas, detección de colisiones por hitboxes y lógica de juego basada en máquina de estados.

---

## Características

- Dos modos de juego completos: **Sin límite** y **Con límites**
- Animaciones fluidas a partir de sprite sheets: correr, saltar, atacar, morir e idle
- Tres animaciones de ataque distintas seleccionadas aleatoriamente
- Dos tipos de enemigos (**Slime** y **Araña**) con animaciones de frames independientes
- Salto con física configurable, gravedad normal y caída rápida
- Sistema de barra de energía con retroalimentación visual y modo de ataque
- Meta animada (trofeo) para el Modo Con Límites
- Contador de distancia en metros con formato de puntos europeo
- Overlay de debug de hitboxes configurable
- Fondo infinito y sin costuras mediante técnica de doble blit
- Máquina de estados que cubre: menú, juego, animación de muerte, pausa post-muerte y victoria

---

## Jugabilidad

### Controles

| Tecla | Acción |
|---|---|
| `Espacio` / `Flecha Arriba` | Saltar |
| `Flecha Abajo` (en el aire) | Caída rápida |
| `Shift Izquierdo` / `Shift Derecho` | Activar modo energía (requiere barra llena) |
| `Flecha Arriba` / `Flecha Abajo` (en menú) | Navegar opciones |
| `Enter` (en menú) | Confirmar selección |

### Modos de juego

**Modo Sin Límite (Endless)**  
Los enemigos aparecen de forma indefinida. El objetivo es sobrevivir el mayor tiempo posible. No hay línea de meta; el juego termina únicamente cuando el jugador es golpeado sin energía activa.

**Modo Con Límites (Limited)**  
El jugador debe recorrer **5.000 metros** para llegar a la meta. A medida que el personaje se acerca al final, aparece en pantalla un trofeo animado. Tocarlo activa la secuencia de victoria. La generación de enemigos se detiene una vez que aparece el trofeo.

### Barra de energía

La barra de energía se muestra en la esquina superior derecha y se carga de forma pasiva al realizar saltos exitosos (+5% por aterrizaje). Cuando alcanza el 100%, la barra se vuelve dorada y aparece el mensaje **"SHIFT para activar"** dentro de ella.

Al activarse con `Shift`:
- La barra se vacía **10%** por cada enemigo tocado.
- Cualquier enemigo con el que se colisione es destruido con una animación de desvanecimiento.
- Se reproduce una animación de ataque aleatoria sobre el personaje.
- Cuando la barra llega a 0%, el modo ataque se desactiva automáticamente.

### Enemigos

Aparecen dos tipos de enemigos de forma aleatoria, con animaciones de sprites independientes:

| Enemigo | Frames | Comportamiento |
|---|---|---|
| Slime | 2 | Obstáculo a ras del suelo, se mueve hacia la izquierda a velocidad constante |
| Araña | 3 | Obstáculo a ras del suelo, se mueve hacia la izquierda a velocidad constante |

Todos los enemigos se desplazan de derecha a izquierda a `VELOCIDAD_ENEMIGO = 9` píxeles por frame. Los enemigos derrotados reproducen un efecto de desvanecimiento de 0,5 segundos antes de ser eliminados.

---

## Estructura del proyecto

```
PythonGame/
├── far_far_away.py          # Archivo principal del juego (toda la lógica)
├── imgs/
│   ├── background/
│   │   └── Background-big.jpg   # Fondo urbano en desplazamiento
│   ├── sprites/
│   │   ├── RUN.png              # Animación de correr    (8 frames)
│   │   ├── JUMP.png             # Animación de salto     (5 frames)
│   │   ├── IDLE.png             # Animación idle         (7 frames)
│   │   ├── ATTACK 1.png         # Ataque variante 1      (6 frames)
│   │   ├── ATTACK 2.png         # Ataque variante 2      (5 frames)
│   │   ├── ATTACK 3.png         # Ataque variante 3      (6 frames)
│   │   └── DEATH.png            # Animación de muerte    (12 frames)
│   ├── enemies/
│   │   ├── slime1.png           # Slime frame 1
│   │   ├── slime2.png           # Slime frame 2
│   │   ├── spider1.png          # Araña frame 1
│   │   ├── spider2.png          # Araña frame 2
│   │   └── spider3.png          # Araña frame 3
│   └── trophy.png               # Sprite de la meta/trofeo  (4 frames)
├── docs/
│   ├── en/
│   │   └── AI_USAGE.md
│   └── es/
│       ├── LEEME.md             # Este archivo
│       └── USO_IA.md
├── LICENSE
└── README.md
```

---

## Assets

Todos los sprite sheets son tiras horizontales donde cada frame tiene el mismo ancho (`ancho_total / cantidad_frames`). La función `cargar_animacion()` recorta y escala cada frame a 175×175 píxeles al momento de carga.

Los sprites de los enemigos son archivos PNG individuales cargados por separado y reflejados horizontalmente para que miren hacia el jugador. Se escalan a 80×80 píxeles.

El fondo es un JPEG ancho que se dibuja dos veces lado a lado y se desplaza continuamente hacia la izquierda. Cuando la primera copia sale de la pantalla, el desplazamiento se reinicia para crear un bucle sin costuras.

---

## Detalles técnicos

### Sistema de físicas

El salto se maneja con un modelo simple de integración de Euler:

```
velocidad_y += GRAVEDAD       (cada frame)
posicion_y  += velocidad_y
```

| Constante | Valor | Descripción |
|---|---|---|
| `GRAVEDAD` | 0.7 | Gravedad normal aplicada cada frame |
| `GRAVEDAD_RAPIDA` | 2.2 | Gravedad extra al mantener Abajo durante el salto |
| `FUERZA_SALTO` | -17 | Velocidad vertical inicial al saltar |

La posición Y del suelo (`y_suelo`) se calcula una sola vez al inicio y se usa como umbral de aterrizaje. La animación de muerte también usa este sistema para que el personaje caiga al suelo antes de reproducir los frames de muerte.

### Generación de enemigos

El sistema de aparición usa un enfoque de **separación basada en distancia** en lugar de un temporizador fijo:

1. Cuando un enemigo aparece en el borde derecho de la pantalla (`ANCHO_PANTALLA`), se elige aleatoriamente una separación `S` en el rango `[SEPARACION_MIN_ENEMIGOS, SEPARACION_MAX_ENEMIGOS]` (300–700 px).
2. Se calcula una posición de disparo: `proximo_spawn_x = ANCHO_PANTALLA - S - ancho_enemigo`.
3. Cada frame, la posición X del enemigo más a la derecha se compara con `proximo_spawn_x`. Cuando la cruza, aparece el siguiente enemigo.

Esto garantiza que el hueco visual entre enemigos consecutivos siempre corresponda a la distancia elegida aleatoriamente, independientemente de cambios en la velocidad.

### Detección de colisiones

Las hitboxes tienen un margen interior respecto al bounding box del sprite para reducir falsos positivos causados por el relleno transparente:

| Entidad | Offset X | Offset Y |
|---|---|---|
| Personaje | 45 px por lado | 45 px por lado |
| Enemigo | 10 px por lado | 0 px |

Activar `MOSTRAR_HITBOXES = True` dibuja los rectángulos de colisión activos en azul, lo cual es útil para ajustar estos valores.

La resolución de colisiones tiene dos ramas:
- **Modo normal:** la primera colisión dispara la secuencia de muerte y congela al enemigo responsable en pantalla.
- **Modo energía:** la colisión destruye al enemigo (con desvanecimiento) y drena un 10% de energía. Varios enemigos pueden ser golpeados en el mismo frame.

### Sistema de animaciones

Todas las animaciones se controlan mediante un contador de ticks. Un frame avanza cada N ticks de juego, donde N varía según el tipo de animación:

| Animación | Ticks por frame | FPS efectivos (a 60) |
|---|---|---|
| Correr / Saltar / Atacar | 4 | ~15 fps |
| Muerte | 5 | ~12 fps |
| Idle / Victoria | 6 | ~10 fps |
| Enemigo | 8 | ~7.5 fps |
| Trofeo | 6 | ~10 fps |

Las animaciones de ataque se eligen aleatoriamente entre tres variantes cada vez que se activa el combate, aportando variedad visual sin intervención adicional del jugador.

---

## Requisitos

- **Python** 3.8 o superior
- **Pygame** 2.x

Instalar Pygame con pip:

```bash
pip install pygame
```

---

## Instalación y ejecución

1. Clonar o descargar el repositorio:

```bash
git clone https://github.com/Licha-M/PythonGame.git
cd PythonGame
```

2. Instalar la dependencia:

```bash
pip install pygame
```

3. Ejecutar el juego:

```bash
python far_far_away.py
```

> El script debe ejecutarse desde la raíz del repositorio para que las rutas relativas a `imgs/` se resuelvan correctamente.

---

## Configuración

Todas las constantes configurables están declaradas al inicio de `far_far_away.py`:

| Constante | Valor por defecto | Descripción |
|---|---|---|
| `ANCHO_PANTALLA` | 1300 | Ancho de la ventana en píxeles |
| `ALTO_PANTALLA` | 500 | Alto de la ventana en píxeles |
| `FPS` | 60 | Tasa de fotogramas objetivo |
| `VELOCIDAD_ENEMIGO` | 9 | Velocidad horizontal del enemigo (px/frame) |
| `VELOCIDAD_FONDO` | 2 | Velocidad de desplazamiento del fondo (px/frame) |
| `SEPARACION_MIN_ENEMIGOS` | 300 | Separación mínima entre enemigos spawneados (px) |
| `SEPARACION_MAX_ENEMIGOS` | 700 | Separación máxima entre enemigos spawneados (px) |
| `ENEMIGOS_MINIMOS` | 1 | Mínimo de enemigos siempre en pantalla |
| `META_DISTANCIA` | 5000 | Metros para ganar en Modo Con Límites |
| `GRAVEDAD` | 0.7 | Gravedad física por frame |
| `GRAVEDAD_RAPIDA` | 2.2 | Gravedad de caída rápida por frame |
| `FUERZA_SALTO` | -17 | Velocidad de impulso al saltar |
| `MOSTRAR_HITBOXES` | `False` | Debug: dibujar rectángulos de hitbox |
| `PERSONAJE_HITBOX_OFFSET_X/Y` | 45 | Margen interior de hitbox del personaje |
| `ENEMIGO_HITBOX_OFFSET_X` | 10 | Margen interior de hitbox del enemigo (horizontal) |

---

## Uso de IA

Este proyecto fue desarrollado con uso selectivo de herramientas de inteligencia artificial. Para un desglose completo de cómo y dónde se consultaron dichas herramientas, incluyendo una muestra de las preguntas realizadas durante el desarrollo, ver el documento de declaración:

[USO_IA.md](USO_IA.md)

---

## Licencia

Este proyecto está bajo la licencia **MIT**. Ver [LICENSE](../../LICENSE) para los términos completos.

Copyright (c) 2026 Lisandro Muñoz Castaño
