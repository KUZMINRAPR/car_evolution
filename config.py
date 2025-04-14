import pygame
import os
PIC_WIDTH = 2000
PIC_HEIGHT = 2000
PIC_SIZE = (PIC_WIDTH, PIC_HEIGHT)
CAR_WIDTH = 40
CAR_HEIGHT = 72
FIRST_LAYER_COUNT = 8
SECOND_LAYER_COUNT = 4
START_POS_X = 935
START_POS_Y = 400
CAR_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "car.jpg"))
)
ROUTE_IMAGE = pygame.image.load(os.path.join("images", "route2.jpg"))
BORDER_COLOR = (238, 204, 53, 255)
SPEED = 300
GENERATIONS = 50
