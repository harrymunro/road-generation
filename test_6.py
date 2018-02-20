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

    
    # Code below attempts to find nearest node
    # NOT CURRENTLY WORKING
    def return_nearest_node(self, coordinates):
        vector_list = []
        
        for n in self.dict_nodes['node_coords']:
            xyh = np.sqrt((n[0]-coordinates[0])**2 + (n[1]-coordinates[1])**2)
            zh = np.sqrt(xyh**2 + (n[2]-coordinates[2])**2)
            vector_list.append(zh)
        
        # return cloest six indices
        index_list = []
        last = 0
        for n in range(6):    
            index = vector_list.index(min(i for i in vector_list if i > last))
            index_list.append(self.dict_nodes['node_num'][index])
            last = vector_list[index]
    
        return index_list
        
    # search for routes then delete 
    # sum of unique nodes
    def search_route():
        
                
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



# create a 5x5 grid of nodes
def linear_grid(x_length, y_length):
    n = 0
    z = 0
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
 
tn = Network()        
 
# now create a bunch of nodes with normal distribution
def randomly_generate_nodes(n_nodes):
    for n in range(n_nodes):
        # could generate different "types" of node
        x = random.gauss(0, 10)
        y = random.gauss(0, 10)
        z = random.gauss(0, 0.001)
        
        x = random.triangular(0, 10, 5)
        y = random.triangular(0, 10, 5)
        
        tn.generate_node([x, y, z], n)
        
    # then use edge search to create the edges
    node_num = 0
    for node in tn.dict_nodes['node_coords']:
        # probability rules for 2-5 connections
        rand = random.random()
        if rand < 0.3:
            num = 1
        elif rand >= 0.3 and rand < 0.6:
            num = 2
        elif rand >= 0.6 and rand < 0.8:
            num = 3
        elif rand >= 0.8 and rand < 0.9:
            num = 4
        elif rand >= 0.9 and rand < 0.95:
            num = 5
        else:
            num = 6
            
        for n in range(num):
            tn.generate_edge([node_num, tn.return_nearest_node(node)[n]])
        node_num += 1
    # use probability rules to assign 1-5 edges to each node
    

randomly_generate_nodes(1000)      
tn.write_network('output.txt')


'''
NOTES
- One problem is road clusters that get generated
as their own "unconnected island"
- Not sure how to eliminate this
- Possible solution: code that looks for open circuits and closes them

'''