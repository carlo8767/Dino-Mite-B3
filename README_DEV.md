# Basic DEV Hands Manual

## Description Class

### 1. Model Creation

The **Model** defines the general structure of the component.

The Model contains:

* Image loading
* Position
* Movement values
* Logic related to the model
* Rectangle for collision and positioning

Example:

```python
class CharacterDino:

    def __init__(self):

        self.move_x = 3
        self.move_y = 3

        self.position_x = 0
        self.position_y = 700

        self.image_dino_path = os.path.join("./image", "character.png")

        self.image_loaded = pygame.image.load(
            self.image_dino_path
        ).convert()

        self.image_loaded = pygame.transform.scale(
            self.image_loaded,
            (60, 60)
        )

        self.rectangle = self.image_loaded.get_rect()

        self.rectangle.center = (
            self.position_x,
            self.position_y
        )
```

### 2. Controller Model

Every Model has its own Controller.

The main purpose of the Controller is to:

* Return the Model
* Receive notifications from the EventController
* Apply updates to the Model

### 3. Event Controller

The purpose of the EventController is to:

* Handle input from the user
* Process events
* Notify the appropriate Controllers
* Update the game components

### 4. Game Component Framework

The Game Component initializes the game and manages the game state.

The game state is a global variable that tells us where we are in the game.

Example:

```python
self.GAME_STATE = utilities_names.LEVEL_ONE
```

The purpose of this class is to:

* Verify the current game state
* Notify the EventController
* Render the correct View

### 5. View

The main purpose of the View is to:

* Render graphics
* Display Models on screen
* Handle user input for the current screen

We must generate a View for every step of the game.

Example:

* Menu View
* Level View
* Game Over View

# How to Load an Image

We do not use sprites because they introduce too much hidden logic ("magic") and limitations.

Steps:

1. Upload the image into the `/image` folder
2. Load the image inside the Model
3. Associate the image with a rectangle

Example:

```python
self.image_dino_path = os.path.join("./image", "character.png")

self.image_loaded = pygame.image.load(
    self.image_dino_path
).convert()

self.rect = self.image_loaded.get_rect()

self.rect.center = (
    self.position_x,
    self.position_y
)
```

Every image MUST have a rectangle.

Documentation:

[https://www.pygame.org/docs/ref/image.html](https://www.pygame.org/docs/ref/image.html)
[https://www.youtube.com/watch?v=rHEnZfq_zEQ](https://www.youtube.com/watch?v=rHEnZfq_zEQ)

# How to Move

Example movement and rendering logic:

```python
for event in pygame.event.get():

    keys = pygame.key.get_pressed()

    # CHARACTER MOVE
    if keys[pygame.K_LEFT]:
        model_level_one.character.rect.x -= 5

    if keys[pygame.K_RIGHT]:
        model_level_one.character.rect.x += 5

# DRAW BACKGROUND
window.blit(
    sprite_image_background,
    (0, 0)
)

# DRAW HAZARD
window.blit(
    model_level_one.hazard_level_one.image_loaded,
    model_level_one.hazard_level_one.rect
)

# UPDATE HAZARD POSITION
model_level_one.hazard_level_one.rect.y += 2

# DRAW CHARACTER
window.blit(
    model_level_one.character.image_loaded,
    model_level_one.character.rect
)

# UPDATE DISPLAY
pygame.display.update()
```
