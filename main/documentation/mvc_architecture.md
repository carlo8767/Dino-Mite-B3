# MVC Architecture — Dino-Mite

How the game is structured across Model, View, and Controller layers, what lives in each base class, and how a level is wired together.

---

## Overview

The game follows an MVC (Model-View-Controller) pattern. Each layer has a strict rule:

| Layer | Responsibility | Must NOT |
|---|---|---|
| **Model** | Data and state only | Call view or controller code |
| **Controller** | Game logic, collision, input, audio | Draw to screen |
| **View** | Render and game loop | Own game state or mutate model directly |

There are three base classes — one per layer — that contain all shared logic. Each level has a thin subclass that adds only what is level-specific.

---

## File map

```
dino_mite_model/
    level_model/
        base_level_model.py         ← shared state for all levels
        levelone.py                 ← Level 1 hazards + assets
        leveltwo.py                 ← Level 2 hazards + assets
        levelthree.py               ← Level 3 hazards + assets (stub)
    character_game/
        Character.py                ← player character
        power_ups.py                ← PowerUp base + ShieldBubble, TimeReduction, SlowerHazards
        vertical_hazard.py          ← VerticalHazard base + Meteor, Fireball
        horizontal_hazard.py        ← HorizontalHazard base + RollingRock, Mammoth

dino_mite_controller/
    model/
        base_level_controller.py    ← all shared game logic
        controller_level_one.py     ← Level 1 hazard registration
        controller_level_two.py     ← Level 2 hazard registration
        controller_level_three.py   ← Level 3 (stub)

dino_mite_view/
    game_component/
        base_view/
            base_level_view.py      ← shared game loop, timer, pause, HUD, death animation
            view_level_one.py       ← Level 1 background + hazard drawing
            view_level_two.py       ← Level 2 background + hazard drawing
            view_level_three.py     ← Level 3 (stub)
        game_state_interactor.py    ← top-level state machine
    event_game_notifications/
        event_controller.py         ← factory: creates fresh controller per level
```

---

## Model layer

### `BaseLevelModel`

Every level model inherits from this. It holds everything that is the same across all levels.

| Attribute | Type | Description |
|---|---|---|
| `character` | `CharacterDino` | The player |
| `pw_up_shield_bubble` | `ShieldBubble` | Powerup instance — reused, never re-created |
| `pw_up_time_reduction` | `TimeReduction` | Powerup instance |
| `pw_up_slower_hazard` | `SlowerHazards` | Powerup instance |
| `sound_complete_level` | `str` | Path to the level-complete music |
| `store_text_end` | `str` | Death screen text, read from a `.txt` file |
| `screen_width`, `screen_height` | `int` | Screen dimensions from `utilities_names` |

Constructor takes one argument: `text_file_path` — the path to the end-of-game text file.

### Level model subclasses (`LevelOne`, `LevelTwo`, `LevelThree`)

Each subclass:
1. Calls `super().__init__(text_file_path)`
2. Instantiates its hazards as named attributes (e.g. `self.hazard_fireball = Fireball()`)
3. Sets `self.image` (background path), `self.sound`, `self.sound_end_game`
4. Sets `self.image_loaded` and `self.rect` for the win animation

The model is a pure data container. No logic lives here.

---

## Controller layer

### `BaseLevelController`

All game logic lives here. Subclasses implement exactly one method.

**Subclass contract — the only requirement:**

```python
class ControllerLevelTwo(BaseLevelController):
    def __init__(self):
        self.level_model = LevelTwo()   # MUST be set before super().__init__()
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_model.hazard_fireball,
            self.level_model.hazard_mammoth,
        ]
```

`self.level_model` must be set before `super().__init__()` because the base `__init__` immediately calls `register_slowable_hazards()`, which reads from `self.level_model`.

**What `self.slowed_hazards` drives automatically:**

| System | Method | What it does |
|---|---|---|
| Movement | `update_movement()` | Calls `hazard.update_position()` on every hazard |
| Collision registry | `_build_collision_registry()` | Maps each hazard → `hazard.name` |
| Slowdown powerup | `apply_slow_hazards()` | Halves `speed` / `move_x` on every hazard |
| Level reset | `reset_level()` | Calls `hazard.update_position_collision()` on every hazard |

**Other systems in `BaseLevelController`:**

| Method | Description |
|---|---|
| `init_music()` | Loads and plays `level_model.sound` |
| `init_music_end_level()` | Plays the lose music |
| `stop_music()` | Stops all music |
| `toggle_pause_menu()` | Flips `is_paused` |
| `handle_player_input(keys, events)` | Delegates to `character.handle_key_input` |
| `apply_player_gravity()` | Calls `character.gravity()` |
| `detection_collision_character(sprite)` | Returns `(True, name)` on collision; deflects if shield active |
| `update_collision_position(name)` | Resets all hazards matching that name |
| `update_powerup(delta_time)` | Ticks shield timer, slowdown timer, powerup spawn cycle |
| `detection_collision_powerup()` | Returns collected powerup name, applies its effect |

**Powerup deck system:**

One deck = 5 cards: 3 × ShieldBubble, 1 × TimeReduction, 1 × SlowerHazards. Shuffled. When the deck is exhausted it is rebuilt and reshuffled. This gives a predictable ratio (60 / 20 / 20) while keeping the order unpredictable. A new powerup spawns every 8000 ms.

---

## View layer

### `BaseLevelView`

The shared game loop. Subclasses never override `draw_screen()` — they override only the methods below.

**Methods subclasses must implement:**

| Method | Signature | Description |
|---|---|---|
| `_load_background` | `(controller) → Surface` | Load and scale the background image |
| `_draw` | `(window, controller, background)` | Blit background, HUD, character, hazards |
| `_win_sequence` | `(window, controller, background, clock) → str` | Win animation, return next state string |
| `_lose_sequence` | `(window, controller, clock) → str` | Lose animation, return `GAME_OVER` |
| `_next_level` | `() → str` | Return the state string for the next level |

**`time_duration_level` class attribute** — set this on the subclass to change the timer:

```python
class ViewLevelTwo(BaseLevelView):
    time_duration_level = 90   # 90 seconds
```

| Level | Duration |
|---|---|
| Level 1 | 120 s |
| Level 2 | 90 s |
| Level 3 | 60 s |

**Shared systems in `BaseLevelView`:**

| System | Description |
|---|---|
| Timer | Counts down from `time_duration_level`; pauses properly; `TimeReduction` powerup subtracts from it |
| Pause | ESC toggles pause; pause duration is excluded from timer |
| Portal spawn | When timer hits `00:00`, a portal spawns at a random ground position away from the player; touching it triggers the win sequence |
| HUD | Draws the timer, falling powerup, and shield bubble around the character |
| Death animation | Fades the screen in/out, plays dead character animation |
| Loading transition | Black fade with "ENTERING PORTAL..." text between levels |

---

## State machine — `GameStateInteractor`

Top-level loop that decides which screen to show. States:

```
MAIN_MENU  →  STORY  →  LEVEL_ONE  →  DRAW_LEVEL_ONE
                                            │
                                        LEVEL_TWO  →  DRAW_LEVEL_TWO
                                                           │
                                                       LEVEL_THREE  →  DRAW_LEVEL_THREE
                                                                            │
                                                                        GAME_OVER
```

Any level can also go to `GAME_OVER` on a loss, or `MAIN_MENU` via the pause menu.

The `EventsController` factory is called each time a level state is entered — it always returns a fresh controller instance, so state is fully reset between playthroughs.

---

## Adding a new level

1. Create `dino_mite_model/level_model/levelN.py` — subclass `BaseLevelModel`, add hazards.
2. Create `dino_mite_controller/model/controller_level_N.py` — subclass `BaseLevelController`, implement `register_slowable_hazards()`.
3. Create `dino_mite_view/game_component/base_view/view_level_N.py` — subclass `BaseLevelView`, implement the five abstract methods, set `time_duration_level`.
4. Add `event_level_N_notification()` to `EventsController`.
5. Wire the new states into `GameStateInteractor`.

See `adding_hazards.md` for the detailed hazard side of step 1–3.
