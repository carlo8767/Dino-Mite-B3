# Dino-Mite-B3

A 2D survival platformer built with **Python** and **Pygame**.

The player travels through different historical eras  
(**Dinosaur Age → Stone Age → Modern Age**) while surviving environmental hazards.

The objective is simple:  
**Survive the timer in each level to unlock the next era.**

---

## Game Structure

The game is structured into three sequential levels:

### Dinosaur Age  
- Meteors  
- Rolling Rocks  

### Stone Age  
- Fireballs  
- Monster Arm  

### Modern Age  
- Bombs  
- Helicopters  
- Drones  

Each level increases in difficulty.

---

## ⚠️ Game Rules

If the player collides with a hazard:

- The game resets to **Menu**
- No checkpoints are saved

Survive long enough, and the portal activates. 
The player must enter in the portal within 5 second. Alternatively, it will die. 

---

## Architecture

The project follows a modular structure inspired by:

- Model–View–Controller (MVC)
- Observer-style update logic
- Reusable level loader

---

## Game State Flow

MENU → RULES → STORYLINE → LEVEL ONE
→ TRANSITION → LEVEL TWO
→ TRANSITION → LEVEL THREE
→ WIN / LOSE


## Notes
The user manual is under the rules section in the main menu or 
written inside rules.txt
(/Dino-Mite-B3/main/text_files/rules.txt)


AI Usage log:

backgroundLevelOne.jpeg - Gimini
backgroundLevelTwo.jpeg - Gimini
backgroundLevelThree.jpeg - Gimini
meteor.png - Gimini
rolling_rock.png - Gimini

