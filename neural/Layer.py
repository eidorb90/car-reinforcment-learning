import math
import random

from neural.Connection import Connection
from neural.Neuron import Neuron


class Layer:
    __neurons = None
    __activation_function = None
    __is_input_layer = None

    def __init__(self,size=3, activation_function="relu", neurons=None, is_input_layer=False):
        self.set_neurons(neurons)
        self.set_activation_function(activation_function)
        self.set_is_input_layer(is_input_layer)
        self.init(size)

    # Helpers
    def add_neuron(self, neuron=None):
        if neuron is None:
            neuron = Neuron(is_input_neuron=self.get_is_input_layer())
        self.get_neurons().append(neuron)

    def init(self, size):
        if self.get_neurons() == []:
            neurons = [Neuron(is_input_neuron=self.get_is_input_layer()) for _ in range(size)]
            # print("Initialzing layer, adding " + str(len(neurons)) + " neurons to layer")
            self.set_neurons(neurons)

    def activate_layer(self):
        if self.get_activation_function() == "tanh":
            self.activate_tanh()
        elif self.get_activation_function() == "relu":
            self.activate_relu()
        elif self.get_activation_function() == "sigmoid":
            self.activate_sigmoid()
        elif self.get_activation_function() == "input":
            return
        else:
            print("Activation function not set or invalid")
            print("Valid options are 'tanh', 'relu', 'sigmoid', 'input'(does noting to neuron values)")

    def activate_tanh(self):
        for neuron in self.get_neurons():
            x = neuron.compute_value()
            neuron.set_activated_value(math.tanh(x))

    def activate_relu(self):
        for neuron in self.get_neurons():
            x = neuron.compute_value()
            neuron.set_activated_value(max(0, x))

    def activate_sigmoid(self):
        for neuron in self.get_neurons():
            x = neuron.compute_value()
            if x >= 0:
                result = 1 / (1 + math.exp(-x))
            else:
                e_x = math.exp(x)
                result = e_x / (1 + e_x)
            neuron.set_activated_value(result)

    def connect(self, layer):
        for neuron in self.get_neurons():
            for out_neuron in layer.get_neurons():
                new_connection = Connection(in_neuron=neuron, out_neuron=out_neuron)
                neuron.add_connection(new_connection)
                out_neuron.add_connection(new_connection)

    def seed_random_inputs(self, max=1, min=-1):
        if self.get_is_input_layer():
            for neuron in self.get_neurons():
                random_value = round(random.uniform(min, max), 2)
                neuron.set_value(random_value)
        else:
            print("Cannot seed inputs for not input layer")


    # Getters
    def get_neurons(self):
        return self.__neurons

    def get_activation_function(self):
        return self.__activation_function

    def get_is_input_layer(self):
        return self.__is_input_layer

    # Setters
    def set_neurons(self, neurons):
        if neurons is None:
            neurons = []
        self.__neurons = neurons

    def set_activation_function(self, activation_function):
        self.__activation_function = activation_function

    def set_is_input_layer(self, is_input_layer):
        self.__is_input_layer = is_input_layer

    def __str__(self) -> str:
        string = ""
        for neuron in self.get_neurons():
            string += "" + str(neuron.get_activated_value()) + " "
        return string
