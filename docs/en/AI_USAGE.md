# AI Usage Disclosure

This document describes how artificial intelligence tools were used during the development of **Far, Far Away**, in accordance with transparency guidelines for academic projects.

---

## Overview

AI assistance was used at a **moderate level** throughout this project. The core game logic, structure, and design decisions were conceived and implemented by the developer. AI tools were consulted selectively to resolve specific technical doubts, understand how certain Pygame subsystems work, and clarify Python concepts that were not yet covered in class. The AI was not used to generate complete blocks of code or to substitute independent problem-solving; rather, it served as a reference tool, similar to how one might use documentation or a programming forum.

The final code was written, reviewed, and understood by the developer. Every answer obtained from an AI was adapted to fit the project's specific needs.

---

## Extent of Use

| Area | AI Involvement | Notes |
|---|---|---|
| Game architecture & structure | None | Designed independently |
| Physics (jump, gravity) | Low | Consulted to understand the math behind velocity integration |
| Sprite sheet loading | Moderate | Asked how to slice frames from a horizontal strip |
| Enemy spawn logic | Moderate | Asked how to calculate gaps between spawns |
| Hitbox collision system | Low | Asked for clarification on `pygame.Rect.colliderect` behavior |
| Background scrolling loop | Low | Asked how double-blit infinite scroll works |
| Energy bar rendering | None | Implemented independently |
| Animation state machine | Moderate | Asked about managing animation priority between states |
| Overall code writing | None | Written by the developer |

---

## Questions Asked

The following is a representative sample of the questions asked to AI tools during development. No complete code solutions were requested; the questions were used to understand concepts and mechanisms.

---

### Pygame & Game Development

- How does `pygame.Rect.colliderect` determine whether two rectangles are overlapping?
- What is the correct way to load a horizontal sprite sheet and extract individual frames using `subsurface`?
- How does the double-blit technique work to create a seamless infinite scrolling background?
- Why does `pygame.transform.flip` need to be called after scaling and not before when loading sprite frames?
- How does `pygame.Surface.set_alpha` work, and what is the difference between per-surface and per-pixel alpha?
- What is the recommended way to control animation speed independently of the game's FPS?

---

### Python Language

- How does slicing a list in place with `list[:] = [...]` differ from reassigning the variable directly with `list = [...]`?
- What is the purpose of the `global` keyword inside a function, and when is it strictly necessary?
- How does `random.choice` select elements, and is every element equally likely to be chosen?
- What is the difference between a shallow copy using `dict(obj)` and a deep copy, and when does it matter?
- How does Python resolve the order of operations when chaining comparison operators like `0 <= x <= 100`?

---

### Physics & Math

- How does Euler integration work when simulating gravity and vertical velocity frame by frame?
- Why does applying a negative initial velocity simulate an upward jump in a coordinate system where Y increases downward?
- How can a minimum and maximum gap between spawned objects be enforced when the objects are moving at a fixed speed?

---

*This document was written as part of the academic submission for the Python Programming course at Institución Educativa Sagrado Corazón de Jesús.*
