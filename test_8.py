'''
Automatic generation of a city road network

Characteristics of road network:
- Random, but with structure
- Any node should have a path to another node

Plan:
Simple function to generate network manually.
Each node needs 3x cartesian coordinates e.g. [1,1,1].
Each node needs a unique identified (i.e. 0, 1, 2, 3)
Edges connect nodes together in format [0,1]
Write nodes to file or print them in format that visualiser can read.
Create couple of methods to generate nodes.
Function to search for nearest other nodes.
Automatate the application of this function to all nodes.
''' 

# Import modules
import random
import math

# Define a network object
class Network():
    # Define initial parameters
    def __init__(self):
        # Create empty dictionary of nodes
        self.dict_nodes = {'node_coords':[], 'node_num':[]}
        # Create empty dictionary of edges
        self.dict_edges = {'node_edges':[]}
        
        # Track the last node generated
        self.last_node_num = 0
        
    # Function to create nodes
    def generate_node(self, coordinates, node_id):
        self.dict_nodes['node_coords'].append(coordinates)
        self.dict_nodes['node_num'].append(node_id)
     
    # function to create edges
    def generate_edge(self, edge):
        a = edge[0]
        b = edge[1]
        self.dict_edges['node_edges'].append([a, b])
        
### TEST ###
# tn = Network()
# tn.generate_node([1,1,1],0)
# tn.generate_node([2,2,2],1)
# tn.generate_edge([0,1])        
# print(tn.dict_nodes)
# print(tn.dict_edges)


    # Function to write network to correct format
    def write_network(self, filename):
        with open(filename, 'w') as file:
            for c in self.dict_nodes['node_coords']:
                file.write('%r, %r, %r\n' % (c[0], c[1], c[2]))
                print('%r, %r, %r' % (c[0], c[1], c[2]))

            for e in self.dict_edges['node_edges']:
                file.write('%r, %r\n' % (e[0], e[1]))
                print('%r, %r' % (e[0], e[1]))

### TEST ###
# tn.write_network('output.txt')
    
    
        
    # search for routes then delete 
    # sum of unique nodes
    #def search_route():
        
    # Generate a slightly random grid of nodes
    # Grid is of size x * y
    def generate_grid_nodes(self, x_length, y_length):
        # Use for loop to iterate over the "grid"
        for y in range(y_length):
            for x in range(x_length):
                # create random coordinates within the boundaries of each grid square
                # triangular distribution: min, max, mid
                node_x = random.triangular(x-1, x, x-0.5) # pick a random x value from square
                node_y = random.triangular(y-1, y, y-0.5) # pick a random y value from square
                node_z = random.triangular(z-0.001, z+0.001, z) # pick a random z value
                self.generate_node([node_x, node_y, node_z], self.last_node_num)
                self.last_node_num += 1    
                
### TEST ###
#tn.generate_grid_nodes(10, 10)
#tn.write_network('output.txt')
    
    # randomly generate nodes without any edges
    def randomly_generate_nodes(self, n_nodes, x_length, y_length):
        
        for n in range(n_nodes):
            # NOTE could generate different "types" of node
            x = random.gauss(x_length/2, x_length/4)
            y = random.gauss(y_length/2, y_length/4)
            z = random.gauss(0, 0.001)
            
            #x = random.triangular(0, x_length, x_length/2)
            #y = random.triangular(0, y_length, y_length/2)
            
            self.generate_node([x, y, z], self.last_node_num)  
            self.last_node_num += 1              
        
    # Code below attempts to find nearest node
    # Aim to return the indexes of the nearest 6 nodes
    # Provide coordinates of base nose as input
    def return_nearest_nodes(self, coordinates):
        # First calculate vectors for every other node in existence
        # Will allow calculation of nearest nodes
        vector_list = []
        for n in self.dict_nodes['node_coords']:
            # x-y hypotenuse
            xyh = math.sqrt((n[0]-coordinates[0])**2 + (n[1]-coordinates[1])**2)
            # x-y to z hypotenuse
            zh = math.sqrt(xyh**2 + (n[2]-coordinates[2])**2)
            # add the vector to the list
            vector_list.append(zh)
        
        # return cloest six indices
        index_list = []
        
        # initialise the search
        last = 0
        # find the 6 closest nodes
        for n in range(6):  
            # find vector that is greater than the last vector chosen
            index = vector_list.index(min(i for i in vector_list if i > last))
            # append index value to the index list
            index_list.append(self.dict_nodes['node_num'][index])
            # update the "last" vector
            last = vector_list[index]
        # return the index list
        return index_list
        
    # generate equal number of edges for each node
    def generate_near_edges(self, num):
        # initialise node number
        node_num = 0
        # for every node, make a num of nearest connections
        for node in self.dict_nodes['node_coords']:
            for n in range(num):
                # create an edge on the n closest node
                self.generate_edge([node_num, self.return_nearest_nodes(node)[n]])
            node_num += 1

tn = Network()  

# Really complex network:
# tn.linear_grid_nodes(20, 20)
# tn.randomly_generate_nodes_no_edges(1000, 20, 20)    
# tn.generate_near_edges(4)

# Nice neat network
# tn.linear_grid_nodes(20, 20)
# tn.generate_near_edges(4)

#tn.linear_grid_nodes(20, 20)
tn.randomly_generate_nodes(10, 20, 20)    
tn.generate_near_edges(3)

tn.write_network('output.txt')

'''
NOTES
- One problem is road clusters that get generated
as their own "unconnected island"
- Not sure how to eliminate this
- Possible solution: code that looks for open circuits and closes them
- Actual solution - create enough edges for each node
- Using fixed grid node generation gurantees connections


Insight:
- Was generating a random network with probability of different number of node
connections from 1-6
-Problem was that this generated islands (demonstrate this)
'''


