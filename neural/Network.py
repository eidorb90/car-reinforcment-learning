from neural.Layer import Layer
import random
import math
import pickle

from neural.Neuron import Neuron


class Network:
    __layers = None
    __loss_function = None
    __optimizer = None
    __gradients = None
    __learning_rate = None
    __batch_size = None

    def __init__(self, layers=None, loss_function="mse", optimizer="adam", learning_rate=0.001, batch_size=32):
        self.set_layers(layers)
        self.set_loss_function(loss_function)
        self.set_optimizer(optimizer)
        self.set_learning_rate(learning_rate)
        self.set_batch_size(batch_size)
        self.init()

    # Helpers
    def init(self):
        if len(self.get_layers()) == 0:
            input_layer = self.add_layer()
            input_layer.add_neuron()
            input_layer.set_activation_function("input")
        if len(self.get_layers()) < 2:
            print("Not enough layers to connect please do so manually after adding more layers via the 'connect_layers' method")
        else:
            self.connect_layers()
            # print("input neuron 0 connections:", len(self.get_layers()[0].get_neurons()[0].get_connections()))

            self.init_weights()

    def init_weights(self):
        for layer in self.get_layers():
            if layer.get_is_input_layer():
                continue
            for neuron in layer.get_neurons():
                fan_in = len(neuron.get_in_connections())
                fan_out = len(neuron.get_out_connections())
                limit = math.sqrt(6 / (fan_in + fan_out))
                neuron.set_bias(random.uniform(0.01, 0.1))
                for connection in neuron.get_in_connections():
                    connection.set_weight(random.uniform(-limit, limit))

    def save_network(self, filename="network.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    def connect_layers(self):
        prev_layer = None
        for layer in self.get_layers():
            if prev_layer is not None:
                prev_layer.connect(layer)

            prev_layer = layer

    def add_layer(self, layer=None):
        if layer is None:
            layer = Layer()
        self.get_layers().append(layer)
        return layer

    def set_input_values(self, values):
        if len(values) != self.get_input_size():
            print("Need to submit list of " + str(self.get_input_size()) + " inputs to match the network")
            return

        for i, neuron in enumerate(self.get_input_layer().get_neurons()):
            neuron.set_value(values[i])

    def get_output_layer_values(self):
        output_values = []
        for neuron in self.get_output_layer().get_neurons():
            output_values.append(neuron.get_activated_value())
        return output_values

    def get_strongest_output(self):
        strongest = 0
        strongest_index = 0
        for i, neuron in enumerate(self.get_output_layer()):
            if neuron.get_activated_value() > strongest:
                strongest = neuron.get_activated_value()
                strongest_index = i
        return strongest_index, strongest


    # Getters
    def get_input_layer(self):
        return self.get_layers()[0]

    def get_output_layer(self):
        return self.get_layers()[-1]

    def get_input_size(self):
        return len(self.get_layers()[0].get_neurons())

    def get_output_size(self):
        return len(self.get_layers()[-1])

    def forward_pass(self):
        for layer in self.get_layers():
            layer.activate_layer()


    # Getters
    def get_layers(self):
        return self.__layers

    def get_loss_function(self):
        return self.__loss_function

    def get_optimizer(self):
        return self.__optimizer

    def get_learning_rate(self):
        return self.__learning_rate

    def get_batch_size(self):
        return self.__batch_size

    # Setters
    def set_layers(self, layers):
        if layers is None:
            layers = []
        self.__layers = layers

    def set_loss_function(self, loss_function):
        self.__loss_function = loss_function

    def set_optimizer(self, optimizer):
        self.__optimizer = optimizer

    def set_learning_rate(self, learning_rate):
        self.__learning_rate = learning_rate

    def set_batch_size(self, batch_size):
        self.__batch_size = batch_size
