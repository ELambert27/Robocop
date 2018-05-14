from hardware import *
import time
class Map(object):
    def __init__(self, cur_node):
        self.grid_map = {}
        self.grid_map[cur_node.position] = cur_node
        self.grid_map[cur_node.position].status_value = 2
        self.node_path_stack = []
        self.node_path_stack.append(cur_node.position)

    def add_node(self, map_node):
        self.grid_map[map_node.position] = map_node
        self.node_path_stack.append(map_node.position)
    
    def all_children_visited(self, map_node):
        for node in map_node.cardinal_available:
            if node == None:
                continue
            elif self.grid_map[node].status_value == 0:
                return False
        return True

    def set_node(self, map_node):
        self.grid_map[map_node.position] = map_node

    def get_node(self, pos):
        return self.grid_map[pos]
        
    def find_path(self, cur_node, checked=[]):
        next_node = self.grid_map[self.node_path_stack.pop()]
        if next_node.status_value == 2:
            print("We're done, we've gone everywhere")
            return []
        elif next_node.status_value == 1:
            return self.find_path(next_node, [next_node])
        elif next_node.status_value == 0:
            return [next_node]        

    def analyze(self, dist_sensor):
        valid_moves = dist_sensor.get_possible_movements()

    def print(self):
        print(self.grid_map)
        print(self.orientation)

    def __repr__(self):
        return str(self.grid_map) + str(self.node_path_stack)

    def __str__(self):
        return str(self.grid_map) + str(self.node_path_stack)
        
class Map_Node():

    #This one should be used :)
    def __init__(self, pos, parent_node=None):
        if(parent_node == None):
            self.position = pos
            #NORTH, EAST, SOUTH, WEST
            self.cardinal_available = [None, None, None, None]
            self.visited = True
            self.status_value = 0
                #status_value is a 0 if the node is unchecked, 1 if it's been passed through,
                #or 2 if it and all of its associated nodes have been passed through.
                #a value of 2 means that this node should never be passed through again

        else:
            self.position = pos
            self.cardinal_available = [None, None, None, None]
            
            p_pos = parent_node.position

            #If x is greater, we are going EAST
            if(pos[0] > p_pos[0]):
                self.cardinal_available[WEST] = p_pos

            #If x is less, we are going WEST
            elif(pos[0] < p_pos[0]):
                self.cardinal_available[EAST] = p_pos

            #If y is greater, we are going NORTH
            elif(pos[1] > p_pos[1]):
                self.cardinal_available[SOUTH] = p_pos
            
            #If y is less than, we are going SOUTH
            elif(pos[1] < p_pos[1]):
                self.cardinal_available[NORTH] = p_pos

            self.visited = False
            self.status_value = 0

    def __repr__(self):
        #return "Node <", self.northAvailable, self.northTraveled, self.eastAvailable, self.eastTraveled, self.southAvailable, self.southTraveled, self.westAvailable, self.westTraveled, ">"
        return str(self.position)

    def __eq__(self, other):
        return isinstance(other, Map_Node) and self.position == other.position

    def __hash__(self):
        print("GAAAH")
        return hash(self.position)
