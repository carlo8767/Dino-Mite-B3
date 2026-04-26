# Power-Ups — Implementation Notes

Technical notes on the power-up system in Dino-Mite-B3. Covers what exists, how it is wired through MVC, and how to add a new powerup.

---

## Current powerups

| Power-up | Class | Effect | Fall speed | Image |
|---|---|---|---|---|
| Shield Bubble | `ShieldBubble` | Protects from hazards for 5 s | 3 | `ShieldBubbleIcon.png` |
| Time Reduction | `TimeReduction` | Removes 5 s from the remaining timer | 3 | `ExtraTimeIcon.png` |
| Slower Hazards | `SlowerHazards` | Halves all hazard speeds for 5 s | 3 | `ReducedVelocityIcon.png` |

All three fall at the same speed (3 px/frame) so the player cannot identify a powerup by how fast it falls.

---

## Architecture

### Model — `power_ups.py`

Lives in `dino_mite_model/character_game/power_ups.py`.

**`PowerUp` (base class)**

Subclasses define three class attributes and implement one method:

```python
class PowerUp(pygame.sprite.Sprite):
    image_path: str = None   # path to the icon image
    name:       str = "PowerUp"
    _speed:     int = 3      # fall speed in px/frame

    def apply_effect(self, character):
        raise NotImplementedError(...)
```

The base `__init__` handles everything else:
- Loads and scales the image to 60×60
- Creates `self.rect`, `self.mask`
- Spawns off-screen at a random x position
- Sets `self.is_active = False`
- Copies `_speed` → `self.speed` so it is an instance attribute

Key methods on the base class:

| Method | Description |
|---|---|
| `activate()` | Moves to a random top x position and sets `is_active = True` |
| `update_position()` | Moves down each frame; deactivates when it exits the bottom |
| `update_position_collision()` | Deactivates and resets off-screen when collected |
| `draw(screen)` | Blits `self.image` at `self.rect` |
| `apply_effect(character)` | Abstract — subclasses must implement |

**`ShieldBubble`**

```python
def apply_effect(self, character):
    character.shield_active = True
    character.shield_timer  = 5000
```

Sets the shield flag and a 5 s countdown on the character. The controller ticks `shield_timer` down each frame and clears the flag when it reaches 0.

**`TimeReduction`**

```python
def apply_effect(self, character):
    pass   # effect is handled in the view's timer calculation
```

`apply_effect` does nothing. The effect is applied in `BaseLevelView`: when the controller returns `"TimeReduction"` from `detection_collision_powerup()`, the view adds 5000 to `self.time_reduction_ms`, which shifts the timer forward.

**`SlowerHazards`**

```python
def apply_effect(self, character):
    pass   # effect is handled in BaseLevelController
```

`apply_effect` does nothing. The controller detects that a `SlowerHazards` instance was collected and activates the slowdown itself (see below).

---

### Controller — `BaseLevelController`

Lives in `dino_mite_controller/model/base_level_controller.py`. All levels share this logic.

**Deck system**

Powerups spawn from a shuffled deck rather than pure random selection. One deck = 5 cards:

```
3 × ShieldBubble
1 × TimeReduction
1 × SlowerHazards
```

The deck is shuffled at the start and after every 5 collections, giving an exact 60 / 20 / 20 ratio with unpredictable order. A new powerup spawns every 8000 ms.

Relevant attributes:

| Attribute | Default | Description |
|---|---|---|
| `powerup_spawn_interval` | 8000 ms | Time between powerup spawns |
| `current_powerup` | `None` | The currently falling powerup |
| `_deck` | shuffled list | The deck of upcoming powerups |

**Slowdown powerup flow**

When `detection_collision_powerup()` finds that the collected powerup is a `SlowerHazards` instance, it calls `apply_slow_hazards()`, which:

1. Reads the speed attribute (`speed` or `move_x`) of every hazard in `self.slowed_hazards`
2. Stores the original values in `self.original_hazard_speeds`
3. Sets each hazard's speed to `max(1, int(original * 0.5))`

After 5000 ms, `update_powerup()` calls `restore_hazard_speeds()` to put them back.

The slowdown works automatically on any hazard registered in `slowed_hazards` — no hazard-specific code is needed.

---

### View — `BaseLevelView`

**Rendering**

The falling powerup is drawn in `_draw_hud()`:

```python
if controller.current_powerup and controller.current_powerup.is_active:
    controller.current_powerup.draw(window)
```

The shield bubble rendered around the character is also in `_draw_hud()` — a separate 150×150 image centered on the character rect.

**TimeReduction timer math**

The view tracks `self.time_reduction_ms`. Each `TimeReduction` collected adds 5000 to it. The timer formula is:

```
remaining = total_seconds - (elapsed_ms + time_reduction_ms) / 1000
```

Adding to elapsed makes the elapsed value appear larger, so remaining time shrinks. Example with a 90-second level:

| Event | elapsed_ms | time_reduction_ms | remaining |
|---|---|---|---|
| 20 s in, no powerup | 20 000 | 0 | 70 s |
| Collect TimeReduction | 20 000 | 5 000 | 65 s |
| Collect another | 20 000 | 10 000 | 60 s |

---

## How to add a new powerup

### Step 1 — Add the subclass to `power_ups.py`

```python
class YourPowerUp(PowerUp):
    image_path = "./image/bubble/YourIcon.png"
    name       = "YourPowerUp"   # unique name used by the controller
    _speed     = 3               # keep at 3 to match all other powerups

    def apply_effect(self, character):
        # Place simple character-state effects here.
        # For anything that requires controller or view state, leave this empty
        # and handle it in BaseLevelController.detection_collision_powerup().
        pass
```

### Step 2 — Instantiate it in `BaseLevelModel`

```python
# base_level_model.py
self.pw_up_your_powerup = YourPowerUp()
```

One instance is created per level and reused for the entire session.

### Step 3 — Add it to the deck in `BaseLevelController`

```python
# base_level_controller.py  _build_deck()
deck = (
    [self.level_model.pw_up_shield_bubble]   * 3 +
    [self.level_model.pw_up_time_reduction]  * 1 +
    [self.level_model.pw_up_slower_hazard]   * 1 +
    [self.level_model.pw_up_your_powerup]    * 1  # add here
)
```

Adjust the multipliers to set how often it appears relative to the other powerups.

### Step 4 — Handle the effect (if needed)

If the effect changes controller or view state (not just character state), add a branch in `BaseLevelController.detection_collision_powerup()`:

```python
if name == "YourPowerUp":
    # apply whatever state change is needed
    ...
```

For a view-side effect (like TimeReduction), add a branch in `BaseLevelView.draw_screen()`:

```python
if collected == "YourPowerUp":
    # adjust view state
    ...
```

---

## MVC compliance checklist

- [ ] `power_ups.py` does not import from `dino_mite_view` or `dino_mite_controller`
- [ ] `apply_effect` only touches `character` attributes — controller/view state is handled elsewhere
- [ ] The view only reads powerup state, never mutates it directly
- [ ] `name` is unique across all powerup classes
- [ ] `_speed = 3` so all powerups fall at the same speed
- [ ] New instance added to `BaseLevelModel` (not per-level model)
- [ ] Deck multipliers updated in `BaseLevelController._build_deck()`
