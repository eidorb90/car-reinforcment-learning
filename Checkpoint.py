import pygame
from Position import Position


class Checkpoint:
    __position = None
    __width = None
    __height = None
    __rect = None
    __is_checked = None

    def __init__(self, position=None, width=20, height=20):
        if position is None:
            position = Position(0, 0)
        self.set_position(position)
        self.set_width(width)
        self.set_height(height)
        self.set_is_checked(False)
        self.init()

    # Helpers
    def init(self):
        rect = pygame.Rect(
            self.get_position().get_x() - self.get_width() / 2,
            self.get_position().get_y() - self.get_height() / 2,
            self.get_width(),
            self.get_height()
        )
        self.set_rect(rect)

    def check_collision(self, car_rect):
        """Returns True if the car's rect overlaps this checkpoint and it hasn't been counted yet."""
        if self.get_is_checked():
            return False
        if self.get_rect().colliderect(car_rect):
            self.set_is_checked(True)
            return True
        return False

    def reset(self):
        self.set_is_checked(False)

    def draw(self, surface):
        color = (0, 255, 0) if self.get_is_checked() else (255, 255, 0)
        pygame.draw.rect(surface, color, self.get_rect(), width=2)

    # Getters
    def get_position(self):
        return self.__position

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_rect(self):
        return self.__rect

    def get_is_checked(self):
        return self.__is_checked

    # Setters
    def set_position(self, position):
        self.__position = position

    def set_width(self, width):
        self.__width = width

    def set_height(self, height):
        self.__height = height

    def set_rect(self, rect):
        self.__rect = rect

    def set_is_checked(self, is_checked):
        self.__is_checked = is_checked