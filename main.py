import json
import random
import os
import time
import copy


neural_networks = []
start_time = time.time()
last_log_time = start_time

last_best_fitness = 0
last_average_fitness = 0
last_worst_fitness = 0


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
                    try:
                        connections.append(connection["weight"] * sum(find_connections(connection["from"][0], connection["from"][1]), neural_network["nodes"][connection["from"][0]][connection["from"][1]]))
                    except IndexError:
                        print("Index Error line 54 approx")
                        print(neural_network)
                        print(connection)
                        quit()
        return connections
    
    # Starts the recursion function for each output neuron
    for x, output_neuron in enumerate(neural_network["nodes"]["output_layer"]):
        connections = find_connections("output_layer", x)
        # Adds the output of that neuron to the list by adding all the connections and the output bias
        outputs.append(sum(connections, output_neuron))
    return outputs
    


# Saves the Neural Network in a json file if the current iteration is in the saving interval
def saveNN(current_iteration, config_parameters, finished=False):
    if finished:
        prefix = os.path.join(os.getcwd(), config_parameters["storage_info"]["file_prefix"])
        with open(f"{prefix}final_winner.json", "w") as file:
            json.dump(neural_networks[0], file, indent=4)
    
    else:
        if current_iteration % config_parameters["storage_info"]["interval"] == 0:
            prefix = os.path.join(os.getcwd(), config_parameters["storage_info"]["file_prefix"])
            
            
            if "all" in config_parameters["storage_info"]["storage_selection"]:
                for x, neural_network in enumerate(neural_networks):
                    with open(f"{prefix}{current_iteration}_{x}.json", "w") as file:
                        json.dump(neural_network, file, indent=4)
            else: 
                if "best" in config_parameters["storage_info"]["storage_selection"]:
                    with open(f"{prefix}{current_iteration}_best.json", "w") as file:
                        json.dump(neural_networks[0], file, indent=4)
                if "worst" in config_parameters["storage_info"]["storage_selection"]:
                    with open(f"{prefix}{current_iteration}_worst.json", "w") as file:
                        json.dump(neural_networks[-1], file, indent=4)
    


# Checks if we are in the saving interval and saves the desired Neurla Networks
# At the moment it saves the nns, but it should save the outputs, and randoms of the game to do replays
def save_replay(current_iteration, config_parameters, finished=False):
    if finished:
        prefix = os.path.join(os.getcwd(), config_parameters["storage_info"]["file_prefix"])
        with open(f"{prefix}final_winner.json", "w") as file:
            json.dump(neural_networks[0], file, indent=4)
    
    else:
        if current_iteration % config_parameters["replays_info"]["interval"] == 0:
            prefix = os.path.join(os.getcwd(), config_parameters["replays_info"]["file_prefix"])
            
            if "all" in config_parameters["replays_info"]["replay_selection"]:
                for x, neural_network in enumerate(neural_networks):
                    with open(f"{prefix}{current_iteration}_{x}.json", "w") as file:
                        json.dump(neural_network, file, indent=4)
            else: 
                if "best" in config_parameters["replays_info"]["replay_selection"]:
                    with open(f"{prefix}{current_iteration}_best.json", "w") as file:
                        json.dump(neural_networks[0], file, indent=4)
                        
                if "worst" in config_parameters["replays_info"]["replay_selection"]:
                    with open(f"{prefix}{current_iteration}_worst.json", "w") as file:
                        json.dump(neural_networks[-1], file, indent=4)


def log(current_iteration):
    # Load last fitnesses
    global last_best_fitness
    global last_average_fitness
    global last_worst_fitness
    
    # Calculate the time since the last log and the total runtime
    global last_log_time
    current_time = time.time()
    total_runtime = current_time - start_time
    time_since_last_log = current_time - last_log_time
    last_log_time = current_time

    # Foramt the total runtime
    total_runtime_h = int(total_runtime // 3600)
    total_runtime_min = int((total_runtime % 3600) // 60)
    total_runtime_s = int(total_runtime % 60)
    total_runtime_ms = int((total_runtime % 1) * 1000)

    # Format the time since the last log
    time_since_last_log_h = int(time_since_last_log // 3600)
    time_since_last_log_min = int((time_since_last_log % 3600) // 60)
    time_since_last_log_s = int(time_since_last_log % 60)
    time_since_last_log_ms = int((time_since_last_log % 1) * 1000)

    best_fitness = max([neural_network["fitness"] for neural_network in neural_networks])
    average_fitness = sum([neural_network["fitness"] for neural_network in neural_networks]) / len(neural_networks)
    worst_fitness = min([neural_network["fitness"] for neural_network in neural_networks])
    
    best_increase = best_fitness - last_best_fitness
    average_increase = average_fitness - last_average_fitness
    worst_increase = worst_fitness - last_worst_fitness
    
    last_best_fitness = best_fitness
    last_average_fitness = average_fitness
    last_worst_fitness = worst_fitness
    
    
    # Print the log 
    print(f"""
    \n\nGeneration: {current_iteration}
    ==================================================
    Generation time: {time_since_last_log_h}h {time_since_last_log_min}min {time_since_last_log_s}s {time_since_last_log_ms}ms
    Fitness:
           |              Actual              Increase
    --------------------------------------------------
    Best   |{best_fitness:>20.2f}  {best_increase:>20.2f}
    Average|{average_fitness:>20.2f}  {average_increase:>20.2f}
    Worst  |{worst_fitness:>20.2f}  {worst_increase:>20.2f}
    Total runtime: {total_runtime_h}h {total_runtime_min}min {total_runtime_s}s {total_runtime_ms}ms
    """)

    
    # Stop if we loose best average (just for tests)
    if best_increase < 0:
        print("Best average decreased")
        quit()


def breed(fitnesses, config_parameters):
    global neural_networks
    # Define a new list for the Neural Networks
    new_neural_networks = []
    population_number = config_parameters["general"]["population_number"]
    
    # Save the two best Neural Networks
    new_neural_networks.append(neural_networks[0])
    new_neural_networks.append(neural_networks[1])
    
    # Calculate the average fitness
    average_fitness = sum([neural_network["fitness"] for neural_network in neural_networks]) / len(neural_networks)
    # Count the number of Neural Networks with a fitness above or equal to the average
    above_average = len([neural_network for neural_network in neural_networks if neural_network["fitness"] >= average_fitness])
    # Calculate the species proportion
    graph_species = above_average*(above_average+1)/2
    proportion = (population_number-2) / graph_species
    
    
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
    
    
    # Create mutations for the above average Neural Networks according to the proportion
    counter = 1
    for nn in reversed(neural_networks[:above_average]):
        
        # Best Neural Network -> Create as many mutations as space left in the population
        if counter == above_average:
            iterations = population_number - len(new_neural_networks)
        else:
            iterations = int(proportion * counter)
        
        
        # Create as many mutations as the proportion says
        for i in range(iterations):
            # Get a copy of the Neural Network to avoid connections
            neural_network = copy.deepcopy(nn)
            # Create a new Neural Network with the same input layer and probability randomized output layer
            new_neural_network = {
                "nodes": {
                    "input_layer": neural_network["nodes"]["input_layer"],
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
                            if len(new_neural_network["nodes"][layer]) == 0:
                                del new_neural_network["nodes"][layer]
                            
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
                                    "from": [layer, x] if layer < random_layer else [random_layer, random_node],
                                    "to": [layer, x] if layer > random_layer else [random_layer, random_node],
                                    "weight": random.uniform(min_weight, max_weight)
                                }
                                new_neural_network["connections"].append(new_connection)
                            
                            # Modify bias
                            if random.random() < modify_bias:
                                new_neural_network["nodes"][layer][x] = random.uniform(min_bias, max_bias)
                        

            # Add the newly created Neural Network to the list
            new_neural_networks.append(new_neural_network)
            
            
        counter += 1
        
    
    # Replace the old Neural Networks with the new ones
    neural_networks = copy.deepcopy(new_neural_networks)


def train(config_parameters):
    current_iteration = 0
    while True:

        #play           --> Done
        #savenn         --> Done
        #savereplay     --> In Progress
        #log            --> Done
        #breed          --> Done
        
        # Calculate the fitness of each neural network
        fitnesses = []
        for neural_network in neural_networks:
            # Example of AND gate
            fitness = 0
            outputs = calculate_outputs([0, 0], neural_network)
            if 0.9 < outputs[0] < 1.1:
                fitness += 1
            outputs = calculate_outputs([0, 1], neural_network)
            if -0.1 < outputs[0] < 0.1:
                fitness += 1
            outputs = calculate_outputs([1, 0], neural_network)
            if -0.1 < outputs[0] < 0.1:
                fitness += 1
            outputs = calculate_outputs([1, 1], neural_network)
            if 0.9 < outputs[0] < 1.1:
                fitness += 1
            
            # Apply the fitness
            neural_network["fitness"] = fitness
            
        # Sort the Neural Networks by their fitness
        neural_networks.sort(key=lambda x: x["fitness"], reverse=True)
        
        
        # Save the Neural Networks and Replays if it's hitting the saving interval
        saveNN(current_iteration, config_parameters)
        save_replay(current_iteration, config_parameters)
        
        # Print the log and store it in a file
        log(current_iteration)
        
        # Stop the program if the fitness objective is achieved
        if neural_networks[0]["fitness"] >= config_parameters["general"]["fitness_objective"]:
            print("Fitness objective achieved")
            saveNN(current_iteration, config_parameters, finished=True)
            save_replay(current_iteration, config_parameters, finished=True)
            break
        
        # Breed the Neural Networks
        breed(fitnesses, config_parameters)
        
        
        current_iteration += 1







def run():
    with open('config.json') as config_file:
        config_parameters = json.load(config_file)
    populate(config_parameters)
    
    train(config_parameters)


run()