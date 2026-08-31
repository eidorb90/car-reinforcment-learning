import math

import pygame
from Position import Position
from Ray import Ray
from neural.Network import Network


class Car:
    __position = None
    __velocity = None
    __acceleration = None
    __max_speed = None
    __angle = None
    __braking = None
    __friction = None
    __turning_speed = None
    __current_speed = None
    __mask = None
    __surface = None
    __color = None
    __current_rect = None
    __is_alive = None
    __network = None
    __rays = None
    __ray_amount = None
    __ray_length = None
    __score = None

    def __init__(
        self,
        position,
        acceleration,
        max_speed,
        angle,
        braking,
        friction,
        turning_speed,
        color,
        network=None,
        ray_amount=7,
        ray_length=100
    ):
        self.set_position(position)
        self.set_velocity(0)
        self.set_acceleration(acceleration)
        self.set_max_speed(max_speed)
        self.set_current_speed(0)
        self.set_angle(angle)
        self.set_braking(braking)
        self.set_friction(friction)
        self.set_turning_speed(turning_speed)
        self.set_color(color)
        self.set_is_alive(True)
        self.set_network(network)
        self.set_ray_amount(ray_amount)
        self.set_rays([])
        self.set_ray_length(ray_length)
        self.set_score(0)

        self.init()

    def init(self):
        rect_surface = pygame.Surface((25, 15), pygame.SRCALPHA)

        self.set_surface(rect_surface)

        pygame.draw.rect(
            self.get_surface(),
            self.get_color(),
            (0, 0, 25, 15)
        )

        self.set_current_rect(rect_surface)
        self.set_mask(
            pygame.mask.from_surface(self.get_surface())
        )

        self.build_rays()

    # ---------------------------------------------------------
    # CAR
    # ---------------------------------------------------------

    def crash(self):
        self.set_is_alive(False)
        self.set_score(self.get_score() - 5)
        self.set_current_speed(0)

    # ---------------------------------------------------------
    # RAYS
    # ---------------------------------------------------------

    def build_rays(self):
        self.set_rays([])

        spread = math.pi
        start_angle = -math.pi / 2

        car_angle = math.radians(-self.get_angle())

        for i in range(self.get_ray_amount()):

            if self.get_ray_amount() == 1:
                offset = 0
            else:
                offset = start_angle + (
                    spread * i / (self.get_ray_amount() - 1)
                )

            ray_angle = car_angle + offset

            ray = Ray(
                (
                    self.get_position().get_x(),
                    self.get_position().get_y()
                ),
                ray_angle,
                max_length=self.get_ray_length()
            )

            self.get_rays().append(ray)

    def update_rays(self):
        spread = math.pi
        start_angle = -math.pi / 2

        car_angle = math.radians(-self.get_angle())

        for i, ray in enumerate(self.get_rays()):

            if len(self.get_rays()) == 1:
                offset = 0
            else:
                offset = start_angle + (
                    spread * i / (len(self.get_rays()) - 1)
                )

            ray_angle = car_angle + offset

            ray.update_origin(
                (
                    self.get_position().get_x(),
                    self.get_position().get_y()
                ),
                ray_angle
            )

    def get_ray_values(self, map_mask):
        values = []

        for ray in self.get_rays():
            values.append(
                ray.get_normalized_distance(map_mask)
            )

        return values

    # ---------------------------------------------------------
    # DRAW
    # ---------------------------------------------------------
    def draw(self, surface, map_mask):
        rotated_surface = pygame.transform.rotate(
            self.get_surface(),
            self.get_angle()
        )

        self.set_mask(
            pygame.mask.from_surface(rotated_surface)
        )

        target_center = (
            self.get_position().get_x(),
            self.get_position().get_y()
        )

        new_rect = rotated_surface.get_rect(
            center=target_center
        )

        self.set_current_rect(new_rect)

        surface.blit(
            rotated_surface,
            new_rect
        )

        self.update_score(map_mask)

    # ---------------------------------------------------------
    # SCORE
    # ---------------------------------------------------------

    def update_score(self, map_mask):
        ray_values = self.get_ray_values(map_mask)

        for ray_value in ray_values:

            if ray_value < 0.1:
                self.set_score(
                    self.get_score() - 0.1
                )

            elif ray_value < 0.2:
                self.set_score(
                    self.get_score() - 0.03
                )

            elif ray_value < 0.4:
                self.set_score(
                    self.get_score() - 0.01
                )

        ray_left = ray_values[0]
        ray_right = ray_values[-1]

        diff = abs(ray_left - ray_right)

        current_speed = self.get_current_speed()

        if diff <= 0.1:
            self.set_score(
                self.get_score() + 0.2
            )

        elif diff <= 0.3:
            self.set_score(
                self.get_score() + 0.05
            )

        elif diff <= 0.5:
            self.set_score(
                self.get_score() + 0.01
            )

        else:
            self.set_score(
                self.get_score() - 0.01
            )

        if abs(current_speed) > 3:
            self.set_score(
                self.get_score() + 0.1
            )

        elif abs(current_speed) > 1:
            self.set_score(
                self.get_score() + 0.01
            )

    # ---------------------------------------------------------
    # KEYBOARD INPUT
    # ---------------------------------------------------------

    def handle_keys(self, keys):
        if not self.get_is_alive():
            return

        current_speed = self.get_current_speed()

        current_x = self.get_position().get_x()
        current_y = self.get_position().get_y()

        current_angle = self.get_angle()

        # Steering
        if abs(current_speed) > 0.1:

            direction_modifier = (
                1 if current_speed > 0 else -1
            )

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                current_angle = (
                    current_angle
                    + self.get_turning_speed()
                    * direction_modifier
                ) % 360

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                current_angle = (
                    current_angle
                    - self.get_turning_speed()
                    * direction_modifier
                ) % 360

        # Acceleration / braking
        if keys[pygame.K_UP] or keys[pygame.K_w]:

            if current_speed < 0:
                self.set_current_speed(
                    current_speed + self.get_braking()
                )
            else:
                self.set_current_speed(
                    current_speed + self.get_acceleration()
                )

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:

            if current_speed > 0:
                self.set_current_speed(
                    current_speed - self.get_braking()
                )
            else:
                self.set_current_speed(
                    current_speed - self.get_acceleration()
                )

        # Friction
        else:

            if current_speed > 0:
                self.set_current_speed(
                    max(
                        0,
                        current_speed - self.get_friction()
                    )
                )

            elif current_speed < 0:
                self.set_current_speed(
                    min(
                        0,
                        current_speed + self.get_friction()
                    )
                )

        # Movement
        rad = math.radians(-current_angle)

        current_x += (
            self.get_current_speed()
            * math.cos(rad)
        )

        current_y += (
            self.get_current_speed()
            * math.sin(rad)
        )

        self.set_angle(current_angle)

        self.set_position(
            Position(current_x, current_y)
        )

        # Update ray position and direction
        self.update_rays()

    # ---------------------------------------------------------
    # NETWORK INPUT
    # ---------------------------------------------------------

    def handle_network_input(self, map_mask, threshold=0.5):
        if not self.get_is_alive():
            return

        network = self.get_network()

        # Get ray values once
        ray_values = self.get_ray_values(map_mask)

        # Feed rays into neural network
        network.set_input_values(ray_values)
        network.forward_pass()

        outputs = network.get_output_layer_values()

        up = outputs[0] > threshold
        left = outputs[1] > threshold
        right = outputs[2] > threshold
        down = outputs[3] > threshold

        if not up and not left and not right:
            self.crash()

        current_speed = self.get_current_speed()

        current_x = self.get_position().get_x()
        current_y = self.get_position().get_y()

        current_angle = self.get_angle()

        # Steering
        if abs(current_speed) > 0.1:

            direction_modifier = (
                1 if current_speed > 0 else -1
            )

            if left:
                current_angle = (
                    current_angle
                    + self.get_turning_speed()
                    * direction_modifier
                ) % 360

            if right:
                current_angle = (
                    current_angle
                    - self.get_turning_speed()
                    * direction_modifier
                ) % 360

        # Acceleration
        if up:

            if current_speed < 0:
                self.set_current_speed(
                    current_speed + self.get_braking()
                )
            else:
                self.set_current_speed(
                    current_speed + self.get_acceleration()
                )
        elif down:
            if current_speed > 0:
                self.set_current_speed(
                    current_speed - self.get_braking()
                )
            else:
                self.set_current_speed(
                    current_speed - self.get_acceleration()
                )

        # Friction
        else:

            if current_speed > 0:
                self.set_current_speed(
                    max(
                        0,
                        current_speed - self.get_friction()
                    )
                )

            elif current_speed < 0:
                self.set_current_speed(
                    min(
                        0,
                        current_speed + self.get_friction()
                    )
                )

        # Movement
        rad = math.radians(-current_angle)

        current_x += (
            self.get_current_speed()
            * math.cos(rad)
        )

        current_y += (
            self.get_current_speed()
            * math.sin(rad)
        )

        self.set_angle(current_angle)

        self.set_position(
            Position(current_x, current_y)
        )

        # Update rays after the car moves
        self.update_rays()

    def update_rect(self):
        rotated_surface = pygame.transform.rotate(
            self.get_surface(),
            self.get_angle()
        )

        target_center = (
            self.get_position().get_x(),
            self.get_position().get_y()
        )

        new_rect = rotated_surface.get_rect(
            center=target_center
        )

        self.set_current_rect(new_rect)

    # ---------------------------------------------------------
    # GETTERS
    # ---------------------------------------------------------

    def get_position(self):
        return self.__position

    def get_velocity(self):
        return self.__velocity

    def get_acceleration(self):
        return self.__acceleration

    def get_max_speed(self):
        return self.__max_speed

    def get_angle(self):
        return self.__angle

    def get_braking(self):
        return self.__braking

    def get_friction(self):
        return self.__friction

    def get_turning_speed(self):
        return self.__turning_speed

    def get_current_speed(self):
        return self.__current_speed

    def get_mask(self):
        return self.__mask

    def get_surface(self):
        return self.__surface

    def get_color(self):
        return self.__color

    def get_current_rect(self):
        return self.__current_rect

    def get_is_alive(self):
        return self.__is_alive

    def get_network(self):
        return self.__network

    def get_rays(self):
        return self.__rays

    def get_ray_amount(self):
        return self.__ray_amount

    def get_ray_length(self):
        return self.__ray_length

    def get_score(self):
        return self.__score

    # ---------------------------------------------------------
    # SETTERS
    # ---------------------------------------------------------

    def set_position(self, position):
        self.__position = position

    def set_velocity(self, velocity):
        self.__velocity = velocity

    def set_acceleration(self, acceleration):
        self.__acceleration = acceleration

    def set_max_speed(self, max_speed):
        self.__max_speed = max_speed

    def set_angle(self, angle):
        self.__angle = angle

    def set_braking(self, braking):
        self.__braking = braking

    def set_friction(self, friction):
        self.__friction = friction

    def set_turning_speed(self, turning_speed):
        self.__turning_speed = turning_speed

    def set_current_speed(self, current_speed):
        max_reverse = -self.get_max_speed() / 2

        if current_speed > self.get_max_speed():
            self.__current_speed = self.get_max_speed()

        elif current_speed < max_reverse:
            self.__current_speed = max_reverse

        else:
            self.__current_speed = current_speed

    def set_mask(self, mask):
        self.__mask = mask

    def set_surface(self, surface):
        self.__surface = surface

    def set_color(self, color):
        self.__color = color

    def set_current_rect(self, rect):
        self.__current_rect = rect

    def set_is_alive(self, is_alive):
        self.__is_alive = is_alive

    def set_network(self, network):
        self.__network = network

    def set_rays(self, rays):
        self.__rays = rays

    def set_ray_amount(self, ray_amount):
        self.__ray_amount = ray_amount

    def set_ray_length(self, ray_length):
        self.__ray_length = ray_length

    def set_score(self, score):
        self.__score = score
