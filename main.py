import sys
import random

import pygame
from Car import Car
from Position import Position
from Map import Map
from Ray import Ray
from neural.Network import Network
from neural.Layer import Layer
from neural.Neuron import Neuron
from Checkpoint import Checkpoint

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

STARTING_POSITION = Position(60, 420)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My First Pygame!")

clock = pygame.time.Clock()
FPS = 60

def create_cars(amount=1):
    cars = []
    for i in range(amount):
        new_car = Car(STARTING_POSITION, 0.15, 8.0, 90, 0.3, 0.15, 5, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        car_brain = make_car_brain()
        new_car.set_network(car_brain)
        new_car.build_rays()
        cars.append(new_car)
    return cars

def rebuild_cars(cars, amount):
    breed_pool = get_breed_pool(cars)
    return breed(breed_pool, amount)

def get_breed_pool(cars):
    return cars

def breed(breed_pool, amount):
    cars = []
    for i in range(amount):
        new_car = Car(STARTING_POSITION, 0.15, 8.0, 90, 0.3, 0.15, 5,
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        car_brain = make_car_brain()
        new_car.set_network(car_brain)
        new_car.build_rays()
        cars.append(new_car)
    return cars

def make_car_brain():
    input_layer = Layer(size=7, activation_function="input", is_input_layer=True)
    hidden_layer_1 = Layer(size=25, activation_function="relu")
    hidden_layer_2 = Layer(size=25, activation_function="relu")
    output_layer = Layer(size=4, activation_function="sigmoid")

    input_layer.seed_random_inputs()

    car_brain = Network(layers=[input_layer, hidden_layer_1, hidden_layer_2, output_layer])

    car_brain.forward_pass()
    return car_brain


def main():
    car_amount = 500
    max_training_time = 500

    cars = create_cars(amount=car_amount)
    map = Map("Red", "tracks/track1.png")

    checkpoints = [
        Checkpoint(Position(70, 300), 130, 10),
        Checkpoint(Position(80, 200), 150, 10),
        Checkpoint(Position(180, 140), 10, 100),
        Checkpoint(Position(270, 140), 10, 100),
        Checkpoint(Position(350, 140), 10, 100),
        Checkpoint(Position(450, 140), 10, 100),
        Checkpoint(Position(550, 140), 10, 100),
        Checkpoint(Position(350, 340), 10, 100),
        Checkpoint(Position(450, 340), 10, 100),
        Checkpoint(Position(550, 340), 10, 100)
    ]

    running = True
    crashes = 0
    training_time = 0

    while running:

        # =====================================================
        # CLEAR SCREEN
        # =====================================================

        screen.fill((40, 44, 52))

        # =====================================================
        # EVENT HANDLING
        # =====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # =====================================================
        # GAME LOGIC
        # =====================================================

        crashes = 0

        for car in cars:

            if not car.get_is_alive():
                crashes += 1
                continue

            car.update_rect()

            # Training timeout / test condition
            if (
                training_time == 50
                and car.get_position().get_y() > 300
            ):
                car.crash()
                crashes += 1
                continue

            # Neural network controls car
            car.handle_network_input(
                map.get_mask()
            )

            # Checkpoint collision
            for checkpoint in checkpoints:

                if checkpoint.check_collision(
                    car.get_current_rect()
                ):
                    car.set_score(
                        car.get_score() + 5
                    )

            # Track collision
            offset_x = car.get_current_rect().x
            offset_y = car.get_current_rect().y

            if map.get_mask().overlap(
                car.get_mask(),
                (offset_x, offset_y)
            ):
                car.crash()
                crashes += 1

        # =====================================================
        # GENERATION RESET
        # =====================================================

        if (
            crashes == car_amount
            or training_time >= max_training_time
        ):
            cars = rebuild_cars(
                cars,
                car_amount
            )

            training_time = 0
            crashes = 0

        # =====================================================
        # RENDERING
        # =====================================================

        # Draw map ONCE
        map.draw(screen)

        # Draw checkpoints ONCE
        for checkpoint in checkpoints:
            checkpoint.draw(screen)

        # Draw cars
        for car in cars:

            if not car.get_is_alive():
                continue

            car.draw(
                screen,
                map.get_mask()
            )

        # =====================================================
        # DISPLAY
        # =====================================================

        pygame.display.flip()

        # =====================================================
        # FRAME RATE
        # =====================================================

        clock.tick(FPS)

        training_time += 1

        print(training_time)

    # =========================================================
    # CLEANUP
    # =========================================================

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
