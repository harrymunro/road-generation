'''
Create a road network.
Options
1. Deterministic
- Suitable for modelling existing road networks

2. Stochastic
- Can create random road networks
- Why is this a good thing?
- Can brute force optimise a complex road network
- Or could use to train a ML algorithm to learn how to build optimal networks

To start with:
Simple function to generate network manually.
Each node needs 3x cartesian coordinates.
Each node needs a unique identified (i.e. 0, 1, 2, 3)
''' 

import random
import numpy as np

# Create a node object
# n_nodes = how many nodes to make
# start = starting cartesian coordinates for first node
class Network():
    def __init__(self):
        
        # create dictionary of nodes
        self.dict_nodes = {'node_coords':[], 'node_num':[]}
        self.dict_edges = {'node_edges':[]}
        
       # generate new network data 
    def generate_node(self, coordinates, node_id):
        self.dict_nodes['node_coords'].append(coordinates)
        self.dict_nodes['node_num'].append(node_id)
        
    def generate_edge(self, edge):
        a = edge[0]
        b = edge[1]
        self.dict_edges['node_edges'].append([a, b])
        
    def return_node_numbers(self):
        return self.dict_nodes['node_num']
        
    def return_edges(self):
        return self.dict_edges['node_edges']
    
    # Code below attempts to find nearest node
    # NOT CURRENTLY WORKING
    def return_nearest_node(self, node_id):
        index = self.dict_nodes['node_num'].index(node_id)
        x = self.dict_nodes['node_coords'][index][0]
        y = self.dict_nodes['node_coords'][index][1]
        z = self.dict_nodes['node_coords'][index][2]
        
        # compute vectors of all other nodes
        new_list = []
        for node in self.dict_nodes['node_coords']:
            # calculate absolute distances for currently selected node
            a = abs(node[0] - x)
            b = abs(node[1] - y)
            new_list.append([np.sqrt(a**2 + b**2),node])
        
        # delete the same node
        for item in new_list:
            if item[0] == 0:
                del new_list[new_list.index(item)]
    
        # find nearest    
        x = new_list[0]
        for item in new_list[1:]:
            if item[0] < x[0]:
                x = item
        
        index = self.dict_nodes['node_coords'].index(x[1])
        
        return self.dict_nodes['node_num'][0]
        
                
        # print network
    def print_network(self):
        # print results - convert to write results later for export
        for c in self.dict_nodes['node_coords']:
            print(c)

        for e in self.dict_edges['node_edges']:
            print(e)

    # write network
    def write_network(self, filename):
        with open(filename, 'w') as file:
            for c in self.dict_nodes['node_coords']:
                file.write('%r, %r, %r\n' % (c[0], c[1], c[2]))

            for e in self.dict_edges['node_edges']:
                file.write('%r, %r\n' % (e[0], e[1]))
                
                
        
        

'''
Nodes across a city will be normally distributed.
Concentrated at center.
Populate nodes first.
Then systematically go through and connect nodes together.
'''

tn = Network()

# create a 5x5 grid of nodes

n = 0
z = 0
x_length = 20
y_length = 20
for y in range(y_length):
    for x in range(x_length):
        node_x = random.triangular(x-1, x, x-0.5) # pick a random x value from grid
        node_y = random.triangular(y-1, y, y-0.5) # pick a random y value from grid
        node_z = random.triangular(z-0.001, z+0.001, z) # pick a random z value
        tn.generate_node([node_x, node_y, node_z], n)
        
        
        # remainder
        r_x = x % x_length
        r_y = y % y_length
        # now assign edges
        # bottom left
        if n == 0:
            tn.generate_edge([n,n+1])
            tn.generate_edge([n,x_length])
        # bottom right
        elif n == x_length - 1:
            tn.generate_edge([n,n-1])
            tn.generate_edge([n,n+x_length])            
        # top left
        elif n == (x_length * y_length - 1) - (x_length - 1):
            tn.generate_edge([n,n+1])
            tn.generate_edge([n,n-x_length])
            
        # top right
        elif n == (x_length * y_length - 1):
            tn.generate_edge([n,n-1])
            tn.generate_edge([n,n-x_length])
        # bottom edge
        elif r_y == 0 and r_x > 0:
            tn.generate_edge([n,n-1])
            tn.generate_edge([n,n+1])
            tn.generate_edge([n,n+x_length])
        # left edge
        elif r_x == 0 and r_y > 0:
            tn.generate_edge([n,n+1])
            tn.generate_edge([n,n+x_length])
            tn.generate_edge([n,n-x_length])
        # right edge
        elif x == (x_length-1) and y > 0:
            tn.generate_edge([n,n-1])
            tn.generate_edge([n,n+x_length])
            tn.generate_edge([n,n-x_length])
        # top edge
        elif y == (y_length-1) and x > 0:
            tn.generate_edge([n,n-1])
            tn.generate_edge([n,n+1])
            tn.generate_edge([n,n-x_length])
        # surrounded
        else:
            tn.generate_edge([n,n-1])
            tn.generate_edge([n,n+1])
            tn.generate_edge([n,n+x_length])
            tn.generate_edge([n,n-x_length])
        
        n = n + 1
        
        
tn.write_network('output.txt')