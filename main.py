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
from neural.Connection import Connection
from Checkpoint import Checkpoint
import pickle

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

STARTING_POSITION = Position(60, 420)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My First Pygame!")

clock = pygame.time.Clock()
FPS = 60

def create_cars(amount=100, brain=None):
    cars = []
    for i in range(amount):
        new_car = Car(STARTING_POSITION, 0.15, 5.0, 90, 0.3, 0.15, 5, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        if brain:
            with open(brain, 'rb') as file:
                brain_obj = pickle.load(file)
            car_brain = brain_obj
        else:
            car_brain = make_car_brain()
        new_car.set_network(car_brain)
        new_car.build_rays()
        cars.append(new_car)
    return cars

def rebuild_cars(cars, amount):
    breed_pool = get_breed_pool(cars)
    return breed(breed_pool, amount)

def get_breed_pool(cars):
    selected_car_count = 10
    temp_car_arr = []
    for i, car in enumerate(cars):
        temp_car_arr.append([car.get_score(), i])

    temp_car_arr.sort()
    temp_car_arr = temp_car_arr[::-1]

    sorted_best_cars = temp_car_arr[0:selected_car_count-1]
    best_cars = []
    for value in sorted_best_cars:
        best_cars.append(cars[value[1]])

    return best_cars
      
def breed(breeding_pool, amount):
    breeding_pairs = get_breeding_pairs(breeding_pool)
    children_cars = []

    while len(children_cars) < amount:
        for pair in breeding_pairs:
            parent_1 = pair[0]
            parent_2 = pair[1]

            new_brain = create_child_network(
                parent_1,
                parent_2
            )

            new_car = Car(
                STARTING_POSITION,
                0.15,
                5.0,
                90,
                0.3,
                0.15,
                5,
                (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            )

            new_car.set_network(new_brain)
            new_car.build_rays()

            children_cars.append(new_car)

            if len(children_cars) >= amount:
                break

    return children_cars


def create_child_network(parent_1, parent_2, mutation_rate=0.05, mutation_strength=0.2):
    parent_1_network = parent_1.get_network()
    parent_2_network = parent_2.get_network()

    child_network = clone_network_architecture(parent_1_network)

    for child_layer, parent_1_layer, parent_2_layer in zip(
        child_network.get_layers(),
        parent_1_network.get_layers(),
        parent_2_network.get_layers()
    ):
        for child_neuron, parent_1_neuron, parent_2_neuron in zip(
            child_layer.get_neurons(),
            parent_1_layer.get_neurons(),
            parent_2_layer.get_neurons()
        ):
            if random.random() < 0.5:
                bias = parent_1_neuron.get_bias()
            else:
                bias = parent_2_neuron.get_bias()
            if random.random() < mutation_rate:
                bias += random.gauss(0, mutation_strength)
            child_neuron.set_bias(bias)

            for child_connection, p1_connection, p2_connection in zip(
                child_neuron.get_in_connections(),
                parent_1_neuron.get_in_connections(),
                parent_2_neuron.get_in_connections()
            ):
                if random.random() < 0.5:
                    weight = p1_connection.get_weight()
                else:
                    weight = p2_connection.get_weight()
                if random.random() < mutation_rate:
                    weight += random.gauss(0, mutation_strength)
                child_connection.set_weight(weight)

    return child_network


def clone_network_architecture(network):
    """
    Builds a new Network with the same layer sizes, activation
    functions, and is_input_layer flags as `network`. Passing a
    fully-formed `layers` list into Network() makes its own
    __init__ call connect_layers() and init_weights() for us,
    so all connections are wired correctly with no manual
    Connection-object plumbing and no recursion of any kind.
    Biases/weights get overwritten by the crossover loop above.
    """
    new_layers = [
        Layer(
            size=len(layer.get_neurons()),
            activation_function=layer.get_activation_function(),
            is_input_layer=layer.get_is_input_layer()
        )
        for layer in network.get_layers()
    ]

    return Network(
        layers=new_layers,
        loss_function=network.get_loss_function(),
        optimizer=network.get_optimizer(),
        learning_rate=network.get_learning_rate(),
        batch_size=network.get_batch_size()
    )

def get_breeding_pairs(breeding_pool):
    cars = list(breeding_pool)
    random.shuffle(cars)

    return [
        [cars[i], cars[i + 1]]
        for i in range(0, len(cars) - 1, 2)
    ]


def make_car_brain():
    input_layer = Layer(size=7, activation_function="input", is_input_layer=True)
    hidden_layer_1 = Layer(size=25, activation_function="relu")
    hidden_layer_3 = Layer(size=25, activation_function="relu")
    output_layer = Layer(size=4, activation_function="sigmoid")

    input_layer.seed_random_inputs()

    car_brain = Network(layers=[input_layer, hidden_layer_1, hidden_layer_3, output_layer])

    car_brain.forward_pass()
    return car_brain


def main():
    WHITE = (255, 255, 255)

    car_amount = 250
    max_training_time = 1000
    generation = 0
    best_score = 0
    free_font = pygame.freetype.SysFont("Arial", 25)

    load = False
    if load:
        cars = create_cars(amount=car_amount, brain="best_cars/best_rl_car_3.pkl")
    else:
        cars = create_cars(amount=car_amount)

    red_checkpoints = [
        Checkpoint(Position(70, 300), 130, 10),
        Checkpoint(Position(80, 200), 150, 10),
        Checkpoint(Position(180, 140), 10, 100),
        Checkpoint(Position(270, 140), 10, 100),
        Checkpoint(Position(350, 140), 10, 100),
        Checkpoint(Position(450, 140), 10, 100),
        Checkpoint(Position(550, 140), 10, 100),
        Checkpoint(Position(350, 340), 10, 100),
        Checkpoint(Position(450, 340), 10, 100),
        Checkpoint(Position(550, 340), 10, 100),

        Checkpoint(Position(350, 490), 10, 100),
        Checkpoint(Position(450, 490), 10, 100),
        Checkpoint(Position(550, 490), 10, 100),

        Checkpoint(Position(350, 690), 10, 100),
        Checkpoint(Position(450, 690), 10, 100),
        Checkpoint(Position(550, 690), 10, 100)
    ]

    fe_checkpoints = [
        Checkpoint(Position(70, 300), 130, 10)

    ]
    crazy_checkpoints = [

    ]

    
    maps = [
            Map("Red", "tracks/track1.png", red_checkpoints),
            Map("Figure Eight", "tracks/fe.png", fe_checkpoints),
            Map("Crazy", "tracks/crazy.png", crazy_checkpoints)
            ]



    running = True
    crashes = 0
    training_time = 0
    map = random.choice(maps)

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
                and car.get_position().get_y() > 275
            ):
                car.crash()
                crashes += 1
                continue

            # Neural network controls car
            car.handle_network_input(
                map.get_mask()
            )

            # Checkpoint collision
            for checkpoint in map.get_checkpoints():

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
            best_gen_score = 0
            for car in cars:
                if car.get_score() > best_gen_score:
                    best_gen_score = car.get_score()
                    car.get_network().save_network("best_cars/best_rl_car_3.pkl")


            if best_gen_score > best_score:
                best_score = best_gen_score
            cars = rebuild_cars(cars, car_amount)
            generation += 1
            training_time = 0
            crashes = 0

            map = random.choice(maps)

            if generation == 25:
                max_training_time = max_training_time * 2


        # =====================================================
        # RENDERING
        # =====================================================

        # Draw map ONCE
        map.draw(screen)
        free_font.render_to(screen, (25, 50), f"Generation: {generation}", WHITE)
        free_font.render_to(screen, (400, 50), f"Best Score: {round(best_score, 2)}", WHITE)


        # Draw checkpoints ONCE
        for checkpoint in map.get_checkpoints():
            checkpoint.draw(screen)

        # Draw cars
        for car in cars:

            if not car.get_is_alive():
                continue

            car.draw(
                screen,
                map.get_mask(), 
                generation
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


    # =========================================================
    # CLEANUP
    # =========================================================

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
