# Declaración de Uso de IA

Este documento describe cómo se utilizaron herramientas de inteligencia artificial durante el desarrollo de **Far, Far Away**, en concordancia con las pautas de transparencia para proyectos académicos.

---

## Descripción general

La asistencia de IA se utilizó en un **nivel moderado** a lo largo de este proyecto. La lógica central del juego, la estructura y las decisiones de diseño fueron concebidas e implementadas por el desarrollador. Las herramientas de IA se consultaron de forma selectiva para resolver dudas técnicas puntuales, entender cómo funcionan ciertos subsistemas de Pygame y aclarar conceptos de Python que aún no se habían visto en clase. La IA no se utilizó para generar bloques completos de código ni para sustituir la resolución independiente de problemas; funcionó como herramienta de referencia, de manera similar a como se usaría la documentación oficial o un foro de programación.

El código final fue escrito, revisado y comprendido por el desarrollador. Cada respuesta obtenida de una IA fue adaptada a las necesidades específicas del proyecto.

---

## Grado de uso

| Área | Participación de IA | Notas |
|---|---|---|
| Arquitectura y estructura del juego | Ninguna | Diseñada de forma independiente |
| Físicas (salto, gravedad) | Baja | Se consultó para entender la matemática detrás de la integración de velocidad |
| Carga de sprite sheets | Moderada | Se preguntó cómo recortar frames de una tira horizontal |
| Lógica de spawn de enemigos | Moderada | Se preguntó cómo calcular separaciones entre spawns |
| Sistema de colisiones con hitboxes | Baja | Se consultó el comportamiento de `pygame.Rect.colliderect` |
| Bucle de desplazamiento de fondo | Baja | Se preguntó cómo funciona el scroll infinito por doble blit |
| Renderizado de la barra de energía | Ninguna | Implementado de forma independiente |
| Máquina de estados de animaciones | Moderada | Se preguntó sobre la gestión de prioridad entre estados de animación |
| Escritura general del código | Ninguna | Escrito por el desarrollador |

---

## Preguntas realizadas

A continuación se presenta una muestra representativa de las preguntas realizadas a herramientas de IA durante el desarrollo. No se solicitaron soluciones de código completas; las preguntas se usaron para comprender conceptos y mecanismos.

---

### Pygame y desarrollo de videojuegos

- ¿Cómo determina `pygame.Rect.colliderect` si dos rectángulos se están superponiendo?
- ¿Cuál es la forma correcta de cargar un sprite sheet horizontal y extraer frames individuales usando `subsurface`?
- ¿Cómo funciona la técnica de doble blit para crear un fondo de desplazamiento infinito sin costuras?
- ¿Por qué `pygame.transform.flip` debe llamarse después de escalar y no antes al cargar frames de sprites?
- ¿Cómo funciona `pygame.Surface.set_alpha` y cuál es la diferencia entre el alpha por superficie y el alpha por píxel?
- ¿Cuál es la forma recomendada de controlar la velocidad de una animación de forma independiente al FPS del juego?

---

### Lenguaje Python

- ¿En qué se diferencia modificar una lista en el lugar con `lista[:] = [...]` de reasignar la variable directamente con `lista = [...]`?
- ¿Cuál es el propósito de la palabra clave `global` dentro de una función y cuándo es estrictamente necesaria?
- ¿Cómo selecciona elementos `random.choice` y todos los elementos tienen la misma probabilidad de ser elegidos?
- ¿Cuál es la diferencia entre una copia superficial con `dict(obj)` y una copia profunda, y cuándo importa esa distinción?
- ¿Cómo resuelve Python el orden de operaciones cuando se encadenan operadores de comparación como `0 <= x <= 100`?

---

### Física y matemáticas

- ¿Cómo funciona la integración de Euler al simular gravedad y velocidad vertical frame a frame?
- ¿Por qué aplicar una velocidad inicial negativa simula un salto hacia arriba en un sistema de coordenadas donde Y aumenta hacia abajo?
- ¿Cómo se puede imponer una separación mínima y máxima entre objetos que se generan mientras se mueven a velocidad constante?

---

*Este documento fue elaborado como parte de la entrega académica para la materia Programación en Python de la Institución Educativa Sagrado Corazón de Jesús.*
