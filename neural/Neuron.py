

class Neuron:
    __activated_value = None
    __value = None
    __connections = None
    __bias = None
    __is_input_neuron = None

    def __init__(self, value=0, connections=None, bias=0, is_input_neuron=False):
        self.set_value(value)
        self.set_activated_value(value)
        self.set_connections(connections)
        self.set_bias(bias)
        self.set_is_input_neuron(is_input_neuron)

    # Helpers
    def get_in_connections(self):
        if self.get_is_input_neuron():
            # print("Cannot get connections for input neuron")
            return []
        in_connections = []
        for connection in self.get_connections():
            if connection.get_out_neuron() == self:
                in_connections.append(connection)
        return in_connections

    def get_out_connections(self):
        out_connections = []
        for connection in self.get_connections():
            if connection.get_in_neuron() == self:
                out_connections.append(connection)
        return out_connections

    def compute_value(self):
        if self.get_is_input_neuron():
            print("Input neuron computed value is just the current value")
            self.set_activated_value(self.get_value())
            return self.get_value()

        total_incoming = 0
        for connection in self.get_in_connections():
            incoming_value = connection.get_in_neuron().get_activated_value()

            incoming_weighted_value = incoming_value * connection.get_weight()
            total_incoming += incoming_weighted_value

        computed_value  = total_incoming + self.get_bias()
        self.set_value(computed_value)
        return computed_value

    def add_connection(self, connection):
        self.get_connections().append(connection)


    # Getters
    def get_value(self):
        return self.__value

    def get_connections(self):
        return self.__connections

    def get_bias(self):
        return self.__bias

    def get_activated_value(self):
        return self.__activated_value

    def get_is_input_neuron(self):
        return self.__is_input_neuron

    # Setters
    def set_value(self, value):
        if self.get_is_input_neuron():
            self.set_activated_value(value)
        self.__value = value

    def set_connections(self, connections):
        if connections is None:
            connections = []
        self.__connections = connections

    def set_bias(self, bias):
        self.__bias = bias

    def set_activated_value(self, activated_value):
        self.__activated_value = activated_value

    def set_is_input_neuron(self, is_input_neuron):
        self.__is_input_neuron = is_input_neuron

    def __str__(self) -> str:
        return (
              "Value: " + str(self.get_value()) + "\n"
            + "Activated Value: " + str(self.get_activated_value()) + "\n"
            + "Connection Count: " + str(len(self.get_connections())) + "\n"
            + "Is Input Neuron: " + str(self.get_is_input_neuron()) + "\n"
                              )