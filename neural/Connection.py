from neural.Neuron import Neuron

class Connection:
    __in_neuron = None
    __out_neuron = None
    __weight = None

    def __init__(self, in_neuron=None, out_neuron=None):
        self.set_in_neuron(in_neuron)
        self.set_out_neuron(out_neuron)
        self.set_weight(0)

    # Helpers

    # Getters
    def get_in_neuron(self):
        return self.__in_neuron

    def get_out_neuron(self):
        return self.__out_neuron

    def get_weight(self):
        return self.__weight

    # Setters
    def set_in_neuron(self, in_neuron):
        if in_neuron is None:
            in_neuron = Neuron()
        self.__in_neuron = in_neuron

    def set_out_neuron(self, out_neuron):
        if out_neuron is None:
            out_neuron = Neuron()
        self.__out_neuron = out_neuron

    def set_weight(self, weight):
        self.__weight = weight