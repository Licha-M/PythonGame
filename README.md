# Far, Far Away

> Versión en español: [docs/es/LEEME.md](docs/es/LEEME.md)

A 2D side-scrolling action game built with Python and Pygame, developed as a school project at **Institución Educativa Sagrado Corazón de Jesús**. The player controls a character who must dodge and defeat enemies across an endless urban landscape, with two distinct gameplay modes and a full suite of animations.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Gameplay](#gameplay)
  - [Controls](#controls)
  - [Game Modes](#game-modes)
  - [Energy Bar](#energy-bar)
  - [Enemies](#enemies)
- [Project Structure](#project-structure)
- [Assets](#assets)
- [Technical Details](#technical-details)
  - [Physics System](#physics-system)
  - [Enemy Spawning](#enemy-spawning)
  - [Collision Detection](#collision-detection)
  - [Animation System](#animation-system)
- [Requirements](#requirements)
- [Installation & Running](#installation--running)
- [Configuration](#configuration)
- [AI Usage](#ai-usage)
- [License](#license)

---

## Overview

**Far, Far Away** is a side-scrolling runner/fighter game where the player character runs through a continuously scrolling city background and must survive against incoming enemies. Players can jump over enemies or activate an energy mode to destroy them on contact. The game tracks distance traveled in meters and offers a limited-distance mode where the objective is to reach the finish line.

The project was built as an educational exercise in Python game development, covering topics such as sprite sheet animation, physics simulation, hitbox-based collision detection, and state-machine game logic.

---

## Features

- Two fully playable game modes: **Endless** and **Limited**
- Smooth sprite sheet animations for running, jumping, attacking, dying, and idling
- Three distinct attack animations selected at random
- Two enemy types (**Slime** and **Spider**) with independent frame-based animations
- Physics-based jumping with configurable gravity and fast-fall mechanic
- Energy bar system with visual feedback and attack mode
- Animated goal/trophy for Limited Mode
- Distance counter displayed in meters (European dot-separated format)
- Configurable hitbox debug overlay
- Seamless infinite background scrolling using a double-blit loop technique
- Game state machine covering: menu, gameplay, death animation, post-death pause, and victory

---

## Gameplay

### Controls

| Key | Action |
|---|---|
| `Space` / `Arrow Up` | Jump |
| `Arrow Down` (while airborne) | Fast fall |
| `Left Shift` / `Right Shift` | Activate energy mode (requires full bar) |
| `Arrow Up` / `Arrow Down` (in menu) | Navigate options |
| `Enter` (in menu) | Confirm selection |

### Game Modes

**Endless Mode**  
Enemies spawn indefinitely. The goal is to survive as long as possible. There is no finish line; the game ends only when the player is hit without energy active.

**Limited Mode**  
The player must travel **5,000 meters** to reach the goal. As the character approaches the finish, an animated trophy appears on screen. Touching it triggers the victory sequence. Enemy spawning stops once the trophy appears.

### Energy Bar

The energy bar is displayed in the upper-right corner of the screen and fills passively as the player lands successful jumps (+5% per landing). Once it reaches 100%, the bar turns gold and the prompt **"SHIFT para activar"** appears inside it.

When activated with `Shift`:
- The bar drains by **10%** per enemy contact.
- Any enemy touched is destroyed with a fade-out animation.
- A random attack animation plays on the character.
- When the bar reaches 0%, attack mode deactivates automatically.

### Enemies

Two enemy types appear randomly with independent sprite animations:

| Enemy | Frames | Behavior |
|---|---|---|
| Slime | 2 | Ground-level obstacle, moves left at constant speed |
| Spider | 3 | Ground-level obstacle, moves left at constant speed |

All enemies move from right to left at `VELOCIDAD_ENEMIGO = 9` pixels per frame. Defeated enemies play a 0.5-second fade-out effect before being removed.

---

## Project Structure

```
PythonGame/
├── far_far_away.py          # Main game file (all logic)
├── imgs/
│   ├── background/
│   │   └── Background-big.jpg   # City scrolling background
│   ├── sprites/
│   │   ├── RUN.png              # Running animation   (8 frames)
│   │   ├── JUMP.png             # Jump animation      (5 frames)
│   │   ├── IDLE.png             # Idle animation      (7 frames)
│   │   ├── ATTACK 1.png         # Attack variant 1   (6 frames)
│   │   ├── ATTACK 2.png         # Attack variant 2   (5 frames)
│   │   ├── ATTACK 3.png         # Attack variant 3   (6 frames)
│   │   └── DEATH.png            # Death animation    (12 frames)
│   ├── enemies/
│   │   ├── slime1.png           # Slime frame 1
│   │   ├── slime2.png           # Slime frame 2
│   │   ├── spider1.png          # Spider frame 1
│   │   ├── spider2.png          # Spider frame 2
│   │   └── spider3.png          # Spider frame 3
│   └── trophy.png               # Goal trophy sprite  (4 frames)
├── LICENSE
└── README.md
```

---

## Assets

All sprite sheets are horizontal strips where each frame has equal width (`sheet_width / frame_count`). The `cargar_animacion()` function slices and scales each frame to 175×175 pixels at load time.

Enemy sprites are individual PNG files loaded separately and mirrored horizontally so they face the player. They are scaled to 80×80 pixels.

The background is a single wide JPEG that is rendered twice side-by-side and scrolled left continuously. When the first copy exits the screen, the offset resets to create a seamless loop.

---

## Technical Details

### Physics System

Jumping is handled with a simple Euler integration model:

```
velocity_y += GRAVITY       (each frame)
position_y += velocity_y
```

| Constant | Value | Description |
|---|---|---|
| `GRAVEDAD` | 0.7 | Normal gravity applied each frame |
| `GRAVEDAD_RAPIDA` | 2.2 | Extra gravity when holding Down during a jump |
| `FUERZA_SALTO` | -17 | Initial upward velocity on jump |

The character's ground Y position (`y_suelo`) is computed once at startup and used as the landing threshold. The death animation also uses this system to let the character fall to the ground before playing the death frames.

### Enemy Spawning

The spawn system uses a **distance-based gap** approach rather than a fixed timer:

1. When an enemy spawns at the right edge of the screen (`ANCHO_PANTALLA`), a random gap `G` is chosen in `[SEPARACION_MIN_ENEMIGOS, SEPARACION_MAX_ENEMIGOS]` (300–700 px).
2. A trigger position is computed: `proximo_spawn_x = ANCHO_PANTALLA - G - enemy_width`.
3. Each frame, the rightmost enemy's X is compared to `proximo_spawn_x`. When it crosses that threshold, the next enemy spawns.

This guarantees that the visual gap between consecutive enemies in the player's field of view always corresponds to the randomly chosen distance, regardless of enemy speed changes.

### Collision Detection

Hitboxes are inset from the sprite bounding box to reduce false positives caused by transparent sprite padding:

| Entity | Offset X | Offset Y |
|---|---|---|
| Player | 45 px per side | 45 px per side |
| Enemy | 10 px per side | 0 px |

Setting `MOSTRAR_HITBOXES = True` draws the active collision rectangles in blue, which is useful for tuning these values.

Collision resolution has two branches:
- **Normal mode:** first collision triggers the death sequence and freezes the killing enemy on screen.
- **Energy mode:** collision destroys the enemy (fade-out) and drains 10% energy. Multiple enemies can be hit in the same frame.

### Animation System

All animations are driven by a tick counter. A frame advances every N game ticks, where N varies by animation type:

| Animation | Ticks per Frame | Effective FPS (at 60) |
|---|---|---|
| Run / Jump / Attack | 4 | ~15 fps |
| Death | 5 | ~12 fps |
| Idle / Victory | 6 | ~10 fps |
| Enemy | 8 | ~7.5 fps |
| Trophy | 6 | ~10 fps |

Attack animations are chosen randomly from three variants each time combat is triggered, giving visual variety without additional input from the player.

---

## Requirements

- **Python** 3.8 or higher
- **Pygame** 2.x

Install Pygame via pip:

```bash
pip install pygame
```

---

## Installation & Running

1. Clone or download this repository:

```bash
git clone https://github.com/Licha-M/PythonGame.git
cd PythonGame
```

2. Install the dependency:

```bash
pip install pygame
```

3. Run the game:

```bash
python far_far_away.py
```

> The script must be executed from the repository root so that the relative paths to `imgs/` resolve correctly.

---

## Configuration

All tunable constants are declared at the top of `far_far_away.py`:

| Constant | Default | Description |
|---|---|---|
| `ANCHO_PANTALLA` | 1300 | Window width in pixels |
| `ALTO_PANTALLA` | 500 | Window height in pixels |
| `FPS` | 60 | Target frame rate |
| `VELOCIDAD_ENEMIGO` | 9 | Enemy horizontal speed (px/frame) |
| `VELOCIDAD_FONDO` | 2 | Background scroll speed (px/frame) |
| `SEPARACION_MIN_ENEMIGOS` | 300 | Minimum gap between spawned enemies (px) |
| `SEPARACION_MAX_ENEMIGOS` | 700 | Maximum gap between spawned enemies (px) |
| `ENEMIGOS_MINIMOS` | 1 | Minimum enemies always on screen |
| `META_DISTANCIA` | 5000 | Meters required to win in Limited Mode |
| `GRAVEDAD` | 0.7 | Physics gravity per frame |
| `GRAVEDAD_RAPIDA` | 2.2 | Fast-fall gravity per frame |
| `FUERZA_SALTO` | -17 | Jump impulse velocity |
| `MOSTRAR_HITBOXES` | `False` | Debug: draw hitbox rectangles |
| `PERSONAJE_HITBOX_OFFSET_X/Y` | 45 | Player hitbox inset per axis |
| `ENEMIGO_HITBOX_OFFSET_X` | 10 | Enemy hitbox inset (horizontal) |

---

## AI Usage

This project was developed with selective use of AI assistance. For a full breakdown of how and where AI tools were consulted, including a sample of the questions asked during development, see the dedicated disclosure document:

[docs/en/AI_USAGE.md](docs/en/AI_USAGE.md)

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for full terms.

Copyright (c) 2026 Lisandro Muñoz Castaño