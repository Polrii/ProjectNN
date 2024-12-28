import timeit
import time
import random


# Test calculate_outputs()
"""
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




inputs = [1, 3]
network = {
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
}

# timeit returns the total time (in seconds) to run the function x times (where x is number=x)
elapsed_time = timeit.timeit(lambda: calculate_outputs(inputs, network), number=1) # 5s -> 1.000.000
outputs = calculate_outputs(inputs, network)
print(elapsed_time)
print(outputs)
"""











# Test log()
start_time = time.time()
last_log_time = start_time

def log():
    global last_log_time
    current_time = time.time()
    total_runtime = current_time - start_time
    time_since_last_log = current_time - last_log_time
    last_log_time = current_time

    total_runtime_h = int(total_runtime // 3600)
    total_runtime_min = int((total_runtime % 3600) // 60)
    total_runtime_s = int(total_runtime % 60)

    time_since_last_log_h = int(time_since_last_log // 3600)
    time_since_last_log_min = int((time_since_last_log % 3600) // 60)
    time_since_last_log_s = int(time_since_last_log % 60)

    print(f"Total runtime: {total_runtime_h}h {total_runtime_min}min {total_runtime_s}s")
    print(f"Time since last log: {time_since_last_log_h}h {time_since_last_log_min}min {time_since_last_log_s}s")


for i in range(100):
    log()
    time.sleep(random.randint(1, 5))