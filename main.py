import json
import random
import os
import ExampleGame


neural_networks = []

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
                connections.append(connection["weight"]*sum(find_connections(),))
                # Should multiply the weight by the sum of all connections and the bias of the previous node
    
    # Starts the recursion function for each output neuron
    for x, output_neuron in enumerate(neural_network["nodes"]["output_layer"]):
        connections = find_connections("output_layer", x)
        # Adds the output of that neuron to the list by adding all the connections and the output bias
        outputs.append(sum(connections, output_neuron))
    return outputs
    



def saveNN(neural_network, name, config_parameters):
    with open(name, "w") as file:
        json.dump(neural_network, file, indent=4)

def save_replay():
    pass



def breed():
    pass


def log():
    pass



def train(config_parameters):
    current_iteration = 1
    while True:

        #play
        #savenn
        #log
        #breed
        fitnesses = []
        for neural_network in neural_networks:
            calculate_outputs([00000], neural_network)
        
        
        
        if current_iteration % config_parameters["storage_info"]["interval"] == 0:
            prefix = os.path.join(os.getcwd(), config_parameters["storage_info"]["file_prefix"])
            
            
            if "all" in config_parameters["storage_info"]["storage_selection"]:
                for x, neural_network in enumerate(neural_networks):
                    saveNN(neural_network, f"{prefix}_{current_iteration}_{x}.json", config_parameters)
            else: 
                if "best" in config_parameters["storage_info"]["storage_selection"]:
                    saveNN(neural_networks[fitnesses.index(max(fitnesses))], f"{prefix}_{current_iteration}_best.json", config_parameters)
                if "worst" in config_parameters["storage_info"]["storage_selection"]:
                    saveNN(neural_networks[fitnesses.index(min(fitnesses))], f"{prefix}_{current_iteration}_worst.json", config_parameters)
        
        
        
        
        
        current_iteration += 1







def run():
    with open('config.json') as config_file:
        config_parameters = json.load(config_file)
    populate(config_parameters)
    
    print(neural_networks)
    
    train()


run()