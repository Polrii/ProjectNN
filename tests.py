# Test calculate_outputs()
def calculate_outputs(inputs, neural_network):
    outputs = []
    
    # Recursion function to go through all the connections from the outputs to the inputs
    def find_connections(layer, position):
        connections = []
        for connection in neural_network["connections"]:
            if connection["to"] == [layer, position]:
                if connection["from"][0] == "input_layer":
                    connections.append(connection["weight"] * inputs[connection["from"][1]])
                else:
                    connections.append(connection["weight"] * sum(find_connections(connection["from"][0], connection["from"][1]), neural_network["nodes"][connection["from"][0]][connection["from"][1]]))
        return connections
    
    # Starts the recursion function for each output neuron
    for x, output_neuron in enumerate(neural_network["nodes"]["output_layer"]):
        connections = find_connections("output_layer", x)
        # Adds the output of that neuron to the list by adding all the connections and the output bias
        outputs.append(sum(connections, output_neuron))
    return outputs


outputs = calculate_outputs([1, 3], {
    "nodes":{
        "input_layer": [0, 0],
        "output_layer": [0, 5, -8],
        "layer_1": [3, -2]
    },
    "connections": [
        {
            "from": ["input_layer", 0],
            "to": ["layer_1", 0],
            "weight": -1
        },
        {
            "from": ["input_layer", 0],
            "to": ["layer_1", 1],
            "weight": 4
        },
        {
            "from": ["input_layer", 1],
            "to": ["layer_1", 1],
            "weight": 15
        },
        {
            "from": ["input_layer", 1],
            "to": ["output_layer", 2],
            "weight": -2
        },
        {
            "from": ["layer_1", 0],
            "to": ["output_layer", 0],
            "weight": 3
        },
        {
            "from": ["layer_1", 0],
            "to": ["output_layer", 1],
            "weight": -7
        },
        {
            "from": ["layer_1", 0],
            "to": ["output_layer", 2],
            "weight": 3.3
        },
        {
            "from": ["layer_1", 1],
            "to": ["output_layer", 1],
            "weight": 1.5
        },
        {
            "from": ["layer_1", 1],
            "to": ["output_layer", 2],
            "weight": -5
        }
        
    ]
    })
print(outputs)