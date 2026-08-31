import pygame

class Map:
    __surface_location = None
    __surface = None
    __name = None
    __mask = None

    def __init__(self, name, surface_location):
        self.set_name(name)
        self.set_surface_location(surface_location)
        self.init()

    # Helpers
    def init(self):
        self.set_surface(pygame.image.load(self.get_surface_location()).convert_alpha())
        self.set_mask(pygame.mask.from_surface(self.get_surface()))

    def draw(self, surface):
        surface.blit(self.get_surface(), (0,0))

    # Getters
    def get_surface_location(self):
        return self.__surface_location

    def get_name(self):
        return self.__name

    def get_mask(self):
        return  self.__mask

    def get_surface(self):
        return self.__surface

    # Setters
    def set_surface_location(self, location):
        self.__surface_location = location

    def set_name(self, name):
        self.__name = name

    def set_mask(self, mask):
        self.__mask = mask

    def set_surface(self, surface):
        self.__surface = surface

