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


def breed():
    pass




def train(config_parameters):
    current_iteration = 1
    while True:

        #play           --> Done
        #savenn         --> Done
        #savereplay     --> In Progress
        #log            --> To Do
        #breed          --> To Do
        
        # Calculate the fitness of each neural network
        fitnesses = []
        for neural_network in neural_networks:
            calculate_outputs([00000], neural_network)
        
        
        # Save the Neural Networks and Replays if it's hitting the saving interval
        saveNN(current_iteration, config_parameters, fitnesses)
        save_replay(current_iteration, config_parameters, fitnesses)
        
        # Print the log and store it in a file
        log()
        
        
        current_iteration += 1







def run():
    with open('config.json') as config_file:
        config_parameters = json.load(config_file)
    populate(config_parameters)
    
    print(neural_networks)
    
    train(config_parameters)


run()