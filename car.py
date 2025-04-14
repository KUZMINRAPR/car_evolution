import math
import pygame
from config import CAR_IMAGE, CAR_WIDTH, CAR_HEIGHT, ROUTE_IMAGE, BORDER_COLOR, SPEED
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = SPEED
        self.indications = {
            "right": 0,
            "down": 0,
            "left": 0,
            "up": 0,
            "right_up": 0,
            "right_down": 0,
            "left_up": 0,
            "left_down": 0
        }
        self.image = CAR_IMAGE
        self.surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.points = {
            "left_up": (self.x, self.y),
            "right_up": (self.x + CAR_WIDTH, self.y),
            "left_down": (self.x, self.y + CAR_HEIGHT),
            "right_down": (self.x + CAR_WIDTH, self.y + CAR_HEIGHT),
            "left": (self.x, self.y + CAR_HEIGHT // 2),
            "right": (self.x + CAR_WIDTH, self.y + CAR_HEIGHT // 2),
            "up": (self.x + CAR_WIDTH // 2, self.y),
            "down": (self.x + CAR_WIDTH // 2, self.y + CAR_HEIGHT)
        }
        self.prev_indications = {
            "right": 0,
            "down": 0,
            "left": 0,
            "up": 0,
            "right_up": 0,
            "right_down": 0,
            "left_up": 0,
            "left_down": 0
        }

    def move(self, dt,output):
        keys = pygame.key.get_pressed()
        if output[0] > 0.5:
            self.y -= 300 * dt
        if output[1] > 0.5:
            self.y += 300 * dt
        if output[2] > 0.5:
            self.x -= 300 * dt
        if output[3] > 0.5:
            self.x += 300 * dt

        self.change_coordinates()
        self.get_indications()

    def distance_to_border(self,car_x, car_y, direction, route_image, border_color):

        step = 1  # Шаг луча в пикселях
        max_distance = 1000  # Максимальная длина луча
        for dist in range(0, max_distance, step):
            # Вычисляем координаты текущей точки луча
            check_x = int(car_x + dist * math.cos(direction))
            check_y = int(car_y - dist * math.sin(direction))  # Минус, так как ось Y направлена вниз

            # Проверяем, не вышли ли за границы изображения
            if not (0 <= check_x < route_image.get_width() and 0 <= check_y < route_image.get_height()):
                return 0  # Луч вышел за пределы изображения

            # Проверяем цвет пикселя
            if route_image.get_at((check_x, check_y)) == border_color:
                return dist  # Возвращаем расстояние до бордюра

        return 0  # Бордюр не найден в пределах max_distance   

    def get_indications(self): 
        directions = {
            "right": 0,
            "down": math.pi / 2,
            "left": math.pi,
            "up": 3*math.pi / 2,
            "right_up": 7*math.pi / 4,
            "right_down": math.pi / 4,
            "left_up": 5*math.pi / 4,
            "left_down": 3*math.pi / 4
        }

        for name, angle in directions.items():
            self.prev_indications[name] = self.indications[name]
            self.indications[name] = self.distance_to_border(self.points[name][0], 
                                                             self.points[name][1],
                                                             angle,
                                                             ROUTE_IMAGE, 
                                                             BORDER_COLOR)

    def change_coordinates(self):
        self.points["left_up"] = (self.x, self.y)
        self.points["right_up"] = (self.x + CAR_WIDTH, self.y)
        self.points["left_down"] = (self.x, self.y + CAR_HEIGHT)
        self.points["right_down"] = (self.x + CAR_WIDTH, self.y + CAR_HEIGHT)
        self.points["left"] = (self.x, self.y + CAR_HEIGHT // 2)
        self.points["right"] = (self.x + CAR_WIDTH, self.y + CAR_HEIGHT // 2)
        self.points["up"] = (self.x + CAR_WIDTH // 2, self.y)
        self.points["down"] = (self.x + CAR_WIDTH // 2, self.y + CAR_HEIGHT)
    
    def destroy(self):
        self.is_destroyed = True
