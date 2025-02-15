from pygame.math import Vector2

## global variable
unlock = False
money = 39
look_menu = False
day_count = 1

#screensize
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

#overlay positions
OVERLAY_POSITIONS = {
    'tool' : (40, SCREEN_HEIGHT - 15),
    'seed' : (70, SCREEN_HEIGHT -5)}

PLAYER_TOOL_OFFSET = {
    'left':Vector2(-50, 40),
    'right':Vector2(50, 40),
    'up':Vector2(0, -10),
    'down':Vector2(0, 50)    
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
}

APPLE_POS = {
    'Small': [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    'Large': [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)]
}

GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}

SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20,
    'egg': 3,
    'milk': 6,
    'chicken': 8,
    'beef': 12
}

PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5,
    'plane_game': 20
}

ANIMAL_POS = {
    'chicken': [(15, 23), (30, 30), (36, 28), (14, 14), (32,16), (31,19)],
    #'chicken': [(30, 30), (36, 28)],
    'cow':[(22,31), (27,18)],
    'chicken_house':[(30,23),(30,24), (30,25),(30,26), (31,23),(31,24), (31,25),(31,26), (32,23),(32,24), (32,25),(32,26)]
}

ANIMAL_SPEED = {
    'chicken': 75,
    'cow': 50
}

ANIMAL_IMAGES_RESIZE = {
    'chicken': (64, 64),
    'cow': (150, 150)
}

AVAILABLE_POS = []