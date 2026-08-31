class Position:
    __x = None
    __y = None

    def __init__(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y
