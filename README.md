# ProjectNN




Neural Networks list format (neural_networks):
[                                                               # List with a dictionary for each neural network
    {                                                           # Dictionary for the first neural network
        'nodes':{                                               # A dictionary with the nodes on that nn
            'input_layer': [0, 0, 0, ...],                      # A list with the input biases
            'output_layer': [1.345240592, 3.92934, ...],        # A list with the output biases
            'layer_n': [2.39401394, -34.09724, ...]             # A list with the n-layer biases
        },
        'connections':[                                         # List for the connections on that nn
            {                                                   # A dictionary for each connection
                'from': ['layer_n', x],                         # The info of the start of that connection
                'to': ['layer_n', x],                           # The info of the end of that connection
                'weight': 4.10347123                            # The weight of the connection
            },
            {...}, ...
        ]
    },
    {...}, ...
]