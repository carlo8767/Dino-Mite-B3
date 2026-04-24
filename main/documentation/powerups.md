# Power-Ups - Implementation Notes

Technical notes on the power-up system in Dino-Mite-B3. Covers what exists, how it's wired through MVC, and implementation decisions worth knowing before extending it.

## Overview

Power-ups are collectible entities that spawn on a timer, fall down the screen (mirroring hazard movement), and apply an effect to the player on collision. 

Currently implemented:

| Power-up | Color | Effect | Speed |
|---|---|---|---|
| Shield Bubble | Red `(255, 0, 0)` | Protects from hazards for 5s | 3 |
| Time Reduction | Yellow `(255, 215, 0)` | Removes 5s from remaining timer | 4 |

## Architecture

The power-up system is split across the three MVC layers as follows.

### Model - `power_ups.py`

Lives in `dino_mite_model/character_game/power_ups.py`. Defines the base class and all subclasses.

**`PowerUp` (base class)**
- `__init__` accepts a `placeholder_color` parameter so each subclass picks its own color without overriding rendering logic until replaced with images
- `self.time_penalty = 0` on the base class — any power-up that doesn't penalize time simply inherits the default
- Movement logic mirrors `Hazard` (same update pattern, same rect-based positioning)

**`ShieldBubble(PowerUp)`**
- Passes red `(255, 0, 0)` to base constructor
- No behavior change from initial Abdallah implementation — this subclass exists for identification and future visual differentiation

**`TimeReduction(PowerUp)`**
- Passes yellow `(255, 215, 0)` to base constructor
- `speed = 4` - falls slightly faster than Shield Bubble for visual distinction
- `time_penalty = 5000` (milliseconds) - consumed by the controller on collection

### Controller - `controller_level_one.py`

Lives in `dino_mite_controller/model/controller_level_one.py`. Owns spawning, collision, and effect application.

**Spawning**
- `powerup_spawn_interval = 15000` ms — one power-up every 15 seconds (≈8 spawns across a 2-minute level)
- `spawn_powerup()` uses weighted random selection:
  - `random.random() < 0.25` → `TimeReduction`
  - otherwise → `ShieldBubble`
  - Expected per game: ~2 TimeReduction, ~6 ShieldBubble

**Collision**
- `detection_collision_powerup()` is a **separate collision method**, not merged into the hazard collision function 
- On collection, reads `powerup.time_penalty` and adds it to `self.time_penalty_ms` if non-zero
- Removes the collected power-up from its sprite group

**Shield integration with hazards**
- Shield protection is implemented inside `detection_collision_hazard()` via an `if` check against the player's shield counter
- On hazard hit while shield is active: shield counter decrements, hazard hit is ignored, player survives


**Time penalty accumulation**
- `self.time_penalty_ms` is an accumulator - every TimeReduction collected adds to it
- Read by the View during timer rendering (see below)

### View — `viewLevelOne.py`

Lives in `dino_mite_view/game_component/viewLevelOne.py`. Renders power-ups and the adjusted timer.

**Power-up rendering**
- Draws each active power-up as a colored placeholder at its rect position
- No logic — purely reads state from the controller and blits

**Timer display — `calculate_timer(ctr_level_one)`**
- Now takes the controller reference as a parameter
- Adds `ctr_level_one.time_penalty_ms` to `elapsed_ms` before computing remaining time

## Timer math - why adding is subtracting

A common point of confusion: the TimeReduction power-up should *reduce* remaining time, but the code *adds* `time_penalty_ms` to `elapsed_ms`. This is correct. The formula is:

```
remaining = total_seconds - (elapsed_ms / 1000)
```

Adding to `elapsed_ms` makes elapsed appear larger, which makes `remaining` smaller. Concrete example with a 120-second level:

| Event | elapsed_ms | time_penalty_ms | remaining |
|---|---|---|---|
| 30s into level, no powerup | 30000 | 0 | 90s |
| Collect TimeReduction | 30000 | 5000 | 85s |
| Collect another TimeReduction | 30000 | 10000 | 80s |


## MVC compliance checklist

For anyone adding new power-ups, verify:

- Model file (`power_ups.py`) does not import from `dino_mite_view` or `dino_mite_controller`
- View file only reads power-up state, never mutates it
- New effect logic lives in the Controller's collision handler, not in the power-up class itself
- New power-up subclass follows the `__init__(placeholder_color, ...)` pattern
- Collision detection stays in its own method, separate from hazard collision

## Known follow-ups

- Speed Break power-up (Abdallah, Sprint 2) - slows hazards temporarily
- HUD icons for active power-up state - pending Ada's asset pass
- Sprite replacement for placeholder colored rectangles - pending Ada's power-up sprites
- Visual indicator when shield is active on player - pending Sprint 1 