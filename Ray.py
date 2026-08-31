import math
import pygame


class Ray:
    __origin = None
    __angle = None
    __max_length = None
    __step = None
    __distance = None

    def __init__(self, origin, angle, max_length=200, step=2):
        self.set_origin(origin)
        self.set_angle(angle)
        self.set_max_length(max_length)
        self.set_step(step)
        self.set_distance(0)

    def update_origin(self, origin, angle):
        self.set_origin(origin)
        self.set_angle(angle)

    def cast(self, track_mask, track_offset=(0, 0)):
        x0, y0 = self.get_origin()

        dx = math.cos(self.get_angle())
        dy = math.sin(self.get_angle())

        width, height = track_mask.get_size()

        distance = 0

        while distance < self.get_max_length():
            x = x0 + dx * distance
            y = y0 + dy * distance

            mask_x = int(x - track_offset[0])
            mask_y = int(y - track_offset[1])

            # Ray has left the track mask
            if not (
                    0 <= mask_x < width
                    and 0 <= mask_y < height
            ):
                self.set_distance(distance)
                return distance, (x, y)

            # Ray hit an obstacle/wall
            if track_mask.get_at((mask_x, mask_y)) != 0:
                self.set_distance(distance)
                return distance, (x, y)

            distance += self.get_step()

        # Ray reached maximum length
        end_x = x0 + dx * self.get_max_length()
        end_y = y0 + dy * self.get_max_length()

        self.set_distance(self.get_max_length())

        return self.get_max_length(), (end_x, end_y)

    def get_normalized_distance(self, track_mask, track_offset=(0, 0)):
        distance, _ = self.cast(track_mask, track_offset)

        return distance / self.get_max_length()

    def draw(
        self,
        screen,
        track_mask,
        track_offset=(0, 0),
        color=(255, 0, 0)
    ):
        _, end = self.cast(track_mask, track_offset)

        pygame.draw.line(
            screen,
            color,
            self.get_origin(),
            end,
            1
        )

    # --- GETTERS ---

    def get_origin(self):
        return self.__origin

    def get_angle(self):
        return self.__angle

    def get_max_length(self):
        return self.__max_length

    def get_step(self):
        return self.__step

    def get_distance(self):
        return self.__distance

    # --- SETTERS ---

    def set_origin(self, origin):
        self.__origin = origin

    def set_angle(self, angle):
        self.__angle = angle

    def set_max_length(self, max_length):
        self.__max_length = max_length

    def set_step(self, step):
        self.__step = step

    def set_distance(self, distance):
        self.__distance = distance