# Adding Hazards — Step-by-Step Guide

How to add a new hazard type for any level. Four files need to change: the hazard module, the level model, the level controller, and the level view.

---

## 1. Add the hazard class

Hazards live in one of two files depending on how they move:

| Movement | File |
|---|---|
| Falls from the top of the screen | `dino_mite_model/character_game/vertical_hazard.py` |
| Rolls/walks across the ground | `dino_mite_model/character_game/horizontal_hazard.py` |

### Vertical hazard (falls down)

Subclass `VerticalHazard`. Override only what differs from the base.

```python
class YourHazard(VerticalHazard):
    image_path = os.path.join("./image/hazard", "your_image.png")
    name       = "YourHazard"   # must be unique across all hazards
    _speed     = 7              # pixels per frame (slowdown powerup modifies this)

    def update_position(self):
        # call the base movement, then add any horizontal drift
        self.rect.y += self.speed
        self.rect.x += random.randint(-2, 2)  # optional drift
        if self.rect.top > HEIGHT:
            self._reset()
```

If the hazard falls straight down with no drift, you don't need to override `update_position` at all — the base handles it.

### Horizontal hazard (ground level)

Subclass `HorizontalHazard`.

```python
class YourHazard(HorizontalHazard):
    image_path = os.path.join("./image/hazard", "your_image.png")
    name       = "YourHazard"
    _move_x    = 3              # pixels per frame rightward
    size       = (80, 80)       # scale the image to this size
    _start_x   = -300           # off-screen left reset position
    _start_y   = 600            # ground level y position
```

Again, no method overrides needed unless the hazard has special movement logic.

### What the base classes give you for free

Both base classes handle all of the following automatically — you do not need to write this yourself:

- `self.image_loaded` — scaled image surface
- `self.rect` — position rectangle
- `self.mask` — pixel-perfect collision mask
- `self.is_active` — whether the hazard is currently visible
- `self.speed` / `self.move_x` — instance copy of the speed (allows the slowdown powerup to modify it without corrupting the class default)
- `update_position_collision()` — resets position on collision
- `_reset()` / `update_position_collision()` — repositions off-screen

---

## 2. Add the hazard to the level model

Open the level's model file (e.g. `dino_mite_model/level_model/leveltwo.py`).

1. Import your new class at the top.
2. Instantiate it in `__init__`.

```python
from dino_mite_model.character_game.vertical_hazard import YourHazard

class LevelTwo(BaseLevelModel):
    def __init__(self):
        super().__init__(os.path.join("./text_files", "end_story.txt"))

        self.hazard_yourHazard    = YourHazard()
        self.hazard_yourHazardOne = YourHazard()  # add more instances as needed
        ...
```

The model is a plain data container. Do not add movement, collision, or game logic here.

---

## 3. Register the hazard in the level controller

Open the level's controller file (e.g. `dino_mite_controller/model/controller_level_two.py`).

Add every hazard instance to `self.slowed_hazards` inside `register_slowable_hazards()`.

```python
def register_slowable_hazards(self):
    self.slowed_hazards = [
        self.level_model.hazard_yourHazard,
        self.level_model.hazard_yourHazardOne,
    ]
```

That single list drives four things automatically via `BaseLevelController`:

| What | How |
|---|---|
| Frame-by-frame movement | `update_movement()` calls `hazard.update_position()` on every entry |
| Collision detection | `_build_collision_registry()` registers every entry by its `name` |
| Slowdown powerup | `apply_slow_hazards()` halves `speed`/`move_x` on every entry |
| Level reset | `reset_level()` calls `hazard.update_position_collision()` on every entry |

You do not call any of these manually — they are called by the shared game loop in `BaseLevelView`.

---

## 4. Draw the hazard in the level view

Open the level's view file (e.g. `dino_mite_view/game_component/base_view/view_level_two.py`).

Inside `_draw()`, blit the hazard after the background and HUD.

**Vertical hazard** — guard with `is_active` (it can be off-screen and inactive):

```python
if controller.level_model.hazard_yourHazard.is_active:
    window.blit(
        controller.level_model.hazard_yourHazard.image_loaded,
        controller.level_model.hazard_yourHazard.rect,
    )
```

**Horizontal hazard** — always on screen, no guard needed:

```python
window.blit(
    controller.level_model.hazard_yourHazard.image_loaded,
    controller.level_model.hazard_yourHazard.rect,
)
```

---

## Complete checklist

- [ ] Hazard class added to `vertical_hazard.py` or `horizontal_hazard.py`
- [ ] `name` is unique (collision system keys on this string)
- [ ] `image_path` points to a real file under `./image/hazard/`
- [ ] Hazard instantiated in the level model `__init__`
- [ ] All instances listed in `register_slowable_hazards()` in the controller
- [ ] `_draw()` in the level view blits `image_loaded` at `rect`

---

## Current hazards per level

| Level | Hazard | Type | Class | Speed |
|---|---|---|---|---|
| 1 | Meteor ×3 | Vertical | `Meteor` | 6 |
| 1 | Rolling Rock ×1 | Horizontal | `RollingRock` | move_x 2 |
| 2 | Fireball ×3 | Vertical | `Fireball` | 8 |
| 2 | Mammoth ×1 | Horizontal | `Mammoth` | move_x 3 |
| 3 | *(to be defined)* | — | — | — |
