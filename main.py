import json
import random
import os
import time
import ExampleGame


neural_networks = []
start_time = time.time()
last_log_time = start_time

def populate(config_parameters):
    for i in range(config_parameters["general"]["population_number"]):
        neural_network = {
            "nodes": {
                "input_layer": [0 for ii in range(config_parameters["inputs_&_outputs"]["inputs_number"])], 
                "output_layer": [random.uniform(config_parameters["inputs_&_outputs"]["min_weight"], config_parameters["inputs_&_outputs"]["max_weight"]) for iii in range(config_parameters["inputs_&_outputs"]["outputs_number"])]
                }, 
            "connections": [
            ]
            }
        
        for x in range(len(neural_network["nodes"]["input_layer"])):
            for y in range(len(neural_network["nodes"]["output_layer"])):
                neural_network["connections"].append({
                    "from": ["input_layer", x],
                    "to": ["output_layer", y],
                    "weight": random.uniform(config_parameters["inputs_&_outputs"]["min_weight"], config_parameters["inputs_&_outputs"]["max_weight"])
                    })
        
        neural_networks.append(neural_network)




# Given a certain neural network and its inputs, returns the outputs
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
    


# Saves the Neural Network in a json file if the current iteration is in the saving interval
def saveNN(current_iteration, config_parameters, fitnesses):
    
    if current_iteration % config_parameters["storage_info"]["interval"] == 0:
        prefix = os.path.join(os.getcwd(), config_parameters["storage_info"]["file_prefix"])
        
        
        if "all" in config_parameters["storage_info"]["storage_selection"]:
            for x, neural_network in enumerate(neural_networks):
                with open(f"{prefix}{current_iteration}_{x}.json", "w") as file:
                    json.dump(neural_network, file, indent=4)
        else: 
            if "best" in config_parameters["storage_info"]["storage_selection"]:
                with open(f"{prefix}{current_iteration}_best.json", "w") as file:
                    json.dump(neural_networks[fitnesses.index(max(fitnesses))], file, indent=4)
            if "worst" in config_parameters["storage_info"]["storage_selection"]:
                with open(f"{prefix}{current_iteration}_worst.json", "w") as file:
                    json.dump(neural_networks[fitnesses.index(min(fitnesses))], file, indent=4)
    


# Checks if we are in the saving interval and saves the desired Neurla Networks
# At the moment it saves the nns, but it should save the outputs, and randoms of the game to do replays
def save_replay(current_iteration, config_parameters, fitnesses):
    if current_iteration % config_parameters["replays_info"]["interval"] == 0:
        prefix = os.path.join(os.getcwd(), config_parameters["replays_info"]["file_prefix"])
        
        if "all" in config_parameters["replays_info"]["replay_selection"]:
            for x, neural_network in enumerate(neural_networks):
                with open(f"{prefix}{current_iteration}_{x}.json", "w") as file:
                    json.dump(neural_network, file, indent=4)
        else: 
            if "best" in config_parameters["replays_info"]["replay_selection"]:
                with open(f"{prefix}{current_iteration}_best.json", "w") as file:
                    json.dump(neural_networks[fitnesses.index(max(fitnesses))], file, indent=4)
                    
            if "worst" in config_parameters["replays_info"]["replay_selection"]:
                with open(f"{prefix}{current_iteration}_worst.json", "w") as file:
                    json.dump(neural_networks[fitnesses.index(min(fitnesses))], file, indent=4)


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


def breed(fitnesses, config_parameters):
    # Define a new list for the Neural Networks
    new_neural_networks = []
    population_number = config_parameters["general"]["population_number"]
    # Sort the Neural Networks by their fitness
    for x, neural_network in enumerate(neural_networks):
        neural_network["fitness"] = fitnesses[x]
    neural_networks.sort(key=lambda x: x["fitness"], reverse=True)
    
    # Save the two best Neural Networks
    new_neural_networks.append(neural_networks[0])
    new_neural_networks.append(neural_networks[1])
    
    
    # Load config parameters for faster access
    max_bias = config_parameters["inputs_&_outputs"]["max_bias"]
    min_bias = config_parameters["inputs_&_outputs"]["min_bias"]
    max_weight = config_parameters["inputs_&_outputs"]["max_weight"]
    min_weight = config_parameters["inputs_&_outputs"]["min_weight"]
    
    modify_weight = config_parameters["mutation_probabilities"]["modify_weight"]
    modify_bias = config_parameters["mutation_probabilities"]["modify_bias"]
    add_node = config_parameters["mutation_probabilities"]["add_node"]
    remove_node = config_parameters["mutation_probabilities"]["remove_node"]
    add_connection = config_parameters["mutation_probabilities"]["add_connection"]
    remove_connection = config_parameters["mutation_probabilities"]["remove_connection"]
    add_layer = config_parameters["mutation_probabilities"]["add_layer"]
    remove_layer = config_parameters["mutation_probabilities"]["remove_layer"]
    
    
    # Create random variations of other Neural Networks
    while len(new_neural_networks) < population_number:
        
        # Select a random Neural Network
        neural_network = random.choice(neural_networks)
        # Create a new Neural Network with the same input layer and probability randomized output layer
        new_neural_network = {
            "nodes": {
                "input_layer": [neural_network["nodes"]["input_layer"]],
                "output_layer": [random.uniform(min_bias, max_bias) if random.random() < modify_bias else output_node for output_node in neural_network["nodes"]["output_layer"]]
            },
            "connections": []
        }
        
        # Iterate through the connections
        for connection in neural_network["connections"]:
            if not random.random() < remove_connection:
                # The connection is not removed (we keep it)
                new_neural_network["connections"].append(connection)
            elif random.random() < modify_weight:
                # The connection is modified (we change the weight)
                new_connection = connection
                new_connection["weight"] = random.uniform(min_weight, max_weight)
                new_neural_network["connections"].append(new_connection)

        
        # Iterate through the layers
        for layer in neural_network["nodes"]:
            # Work only on the hidden layers
            if layer != "input_layer" and layer != "output_layer":
                # Check if we keep the layer
                if not random.random() < remove_layer:
                    new_neural_network["nodes"][layer] = neural_network["nodes"][layer]
                    # Add node if probability says so
                    if random.random() < add_node:
                        new_neural_network["nodes"][layer].append(random.uniform(min_bias, max_bias))
                # If we remove the layer, we remove the connections
                else:
                    for x, connection in enumerate(new_neural_network["connections"]):
                        if connection["from"][0] == layer or connection["to"][0] == layer:
                            del new_neural_network["connections"][x]
        
        
        # Check if we add layer
        if random.random() < add_layer:
            layer_counter = 1
            while True:
                new_layer_name = f"layer_{layer_counter}"
                if new_layer_name not in new_neural_network["nodes"]:
                    new_neural_network["nodes"][new_layer_name] = [random.uniform(min_bias, max_bias)]
                    break
                layer_counter += 1

        
        # Iterate through the nodes
        for layer in new_neural_network["nodes"]:
            # Input layer -> add connection
            if layer == "input_layer":
                for x, node in enumerate(new_neural_network["nodes"][layer]):
                    # Add a connection
                    if random.random() < add_connection:
                        # Get a list of the layers and remove the input layer
                        layers_list = list(new_neural_network["nodes"].keys())
                        layers_list.remove(layer)
                        
                        # Get a random layer and node number
                        random_layer = random.choice(layers_list)
                        random_node = random.randint(0, len(new_neural_network["nodes"][random_layer])-1)
                        
                        # Create and add the new connection
                        new_connection = {
                            "from": ["input_layer", x],
                            "to": [random_layer, random_node],
                            "weight": random.uniform(min_weight, max_weight)
                        }
                        new_neural_network["connections"].append(new_connection)
            
            # Output layer -> add connection, modify bias
            elif layer == "output_layer":
                for x, node in enumerate(new_neural_network["nodes"][layer]):
                    # Add a connection
                    if random.random() < add_connection:
                        # Get a list of the layers and remove the input layer
                        layers_list = list(new_neural_network["nodes"].keys())
                        layers_list.remove(layer)
                        
                        # Get a random layer and node number
                        random_layer = random.choice(layers_list)
                        random_node = random.randint(0, len(new_neural_network["nodes"][random_layer])-1)
                        
                        # Create and add the new connection
                        new_connection = {
                            "from": [random_layer, random_node],
                            "to": ["output_layer", x],
                            "weight": random.uniform(min_weight, max_weight)
                        }
                        new_neural_network["connections"].append(new_connection)
                    
                    # Modify bias
                    if random.random() < modify_bias:
                        new_neural_network["nodes"][layer][x] = random.uniform(min_bias, max_bias)
            
            # Other layers -> add connection, modify bias, remove nodes
            else:
                for x, node in enumerate(new_neural_network["nodes"][layer]):
                    # Remove node
                    if random.random() < remove_node:
                        del new_neural_network["nodes"][layer][x]
                        
                        # Remove connections to that node and modify the references
                        for y, connection in enumerate(new_neural_network["connections"]):
                            if connection["from"] == [layer, x] or connection["to"] == [layer, x]:
                                del new_neural_network["connections"][y]
                            elif connection["from"][0] == layer:
                                if connection["from"][1] > x:
                                    connection["from"][1] -= 1
                            elif connection["to"][0] == layer:
                                if connection["to"][1] > x:
                                    connection["to"][1] -= 1

                        
                    else: 
                        # Add a connection
                        if random.random() < add_connection:
                            # Get a list of the layers and remove the input layer
                            layers_list = list(new_neural_network["nodes"].keys())
                            layers_list.remove(layer)
                            
                            # Get a random layer and node number
                            random_layer = random.choice(layers_list)
                            random_node = random.randint(0, len(new_neural_network["nodes"][random_layer])-1)
                            
                            # Create and add the new connection
                            new_connection = {
                                "from": [layer, x if layer < random_layer else random_layer, random_node],
                                "to": [layer, x if layer > random_layer else random_layer, random_node],
                                "weight": random.uniform(min_weight, max_weight)
                            }
                            new_neural_network["connections"].append(new_connection)
                        
                        # Modify bias
                        if random.random() < modify_bias:
                            new_neural_network["nodes"][layer][x] = random.uniform(min_bias, max_bias)
                    

        # Add the newly created Neural Network to the list
        new_neural_networks.append(new_neural_network)
        
        




def train(config_parameters):
    current_iteration = 1
    while True:

        #play           --> Done
        #savenn         --> Done
        #savereplay     --> In Progress
        #log            --> In Progress
        #breed          --> In Progress
        
        # Calculate the fitness of each neural network
        fitnesses = []
        for neural_network in neural_networks:
            calculate_outputs([00000], neural_network)
        
        
        # Save the Neural Networks and Replays if it's hitting the saving interval
        saveNN(current_iteration, config_parameters, fitnesses)
        save_replay(current_iteration, config_parameters, fitnesses)
        
        # Print the log and store it in a file
        log()
        
        # Breed the Neural Networks
        breed(fitnesses, config_parameters)
        
        
        current_iteration += 1







def run():
    with open('config.json') as config_file:
        config_parameters = json.load(config_file)
    populate(config_parameters)
    
    print(neural_networks)
    
    train(config_parameters)


run()