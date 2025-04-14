import neat.config
import pygame
import neat
from config import *
from car import Car

def draw_window(screen, cars):
    screen.blit(ROUTE_IMAGE, (0, 0))
    for car in cars:
        screen.blit(car.image, (car.x, car.y))
    pygame.display.flip()

    
def main(genomes, config):
    pygame.init()
    pygame.display.set_caption("Car Evolution")

    screen = pygame.display.set_mode((PIC_WIDTH, PIC_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    cars_pos = pygame.Vector2(START_POS_X, START_POS_Y)
    
    # my arrays
    cars = []
    nets = []
    ge = []
    for i,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(cars_pos.x, cars_pos.y))
        g.fitness = 0
        ge.append(g)

    # Game loop
    last_check_time = 0
    while running and len(cars) > 0:
        to_remove = []
        current_time = pygame.time.get_ticks() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for x,car in enumerate(cars):
            car.get_indications()
            if current_time - last_check_time > 0.75:
                if car.prev_indications == car.indications:
                    if to_remove.count(x) == 0:
                        ge[x].fitness -= 1
                        to_remove.append(x)
                last_check_time = current_time
            if ROUTE_IMAGE.get_at((int(car.x), int(car.y))) == BORDER_COLOR or ROUTE_IMAGE.get_at((int(car.x) + 40, int(car.y) + 72)) == BORDER_COLOR or ROUTE_IMAGE.get_at((int(car.x) + 40, int(car.y))) == BORDER_COLOR or ROUTE_IMAGE.get_at((int(car.x), int(car.y) + 72)) == BORDER_COLOR:
                if to_remove.count(x) == 0:
                    print("Car was destroyed")
                    ge[x].fitness -= 1
                    to_remove.append(x)

            ge[x].fitness += 0.1

            print(car.indications)

            output = nets[x].activate((car.indications["right"], car.indications["down"], car.indications["left"], car.indications["up"],
                car.indications["right_up"], car.indications["right_down"], car.indications["left_up"], car.indications["left_down"]))

            print(output)

            #Activate function
            car.move(dt,output)
        # Remove cars that are destroyed
        for x in sorted(to_remove, reverse=True):
            cars.pop(x)
            nets.pop(x)
            ge.pop(x)

        dt = clock.tick(60) / 1000
        draw_window(screen, cars)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                                config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,GENERATIONS)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)