from hardware import *
import time
class Map(object):
    def __init__(self, cur_node):
        self.grid_map = {}
        self.grid_map[cur_node.position] = cur_node
        self.checked = []
        self.unchecked = []

    def set_node(self, map_node):
        self.grid_map[map_node.position] = map_node

    def get_node(self, pos):
        return self.grid_map[pos]

    def update_nodes(self):
        for node in self.grid_map:
            if self.grid_map[node].visited == True:
                self.checked.append(node)
            else:
                self.unchecked.append(node)
        
    def find_path(self, cur_node, checked=[]):
        checked.append(cur_node.position)
        print(checked)
        for node in cur_node.cardinal_available:
            if node in checked:
                print("We in here")
                continue
            try:
                next_node = self.grid_map[node]
            except:
                continue
            if next_node.visited == False:
                print(str(next_node) + " has not been visited yet :)")
                return [next_node]
            else:
                return [cur_node].extend(self.find_path(next_node, checked))
        return []

#    def find_path(self, cur_node, recursive=False):
#        print("At current node: " + str(cur_node))
#        if not recursive:
#            self.update_nodes()
#        time.sleep(0.01)
#        while True:
#            try:
#                node = self.unchecked.pop()
#                print(node)
#                if (self.grid_map[cur_node].position[0] - self.grid_map[node].position[0] + self.grid_map[cur_node].position[1] - self.grid_map[node].position[1]) == 1:
#                    #i.e. this node is 1 away from the current node
#                    return [node]
#                else:
#                    return [node].extend(self.find_path(node, True))
#            except IndexError:
#                break
#        return []

    def analyze(self, dist_sensor):
        valid_moves = dist_sensor.get_possible_movements()

    def print(self):
        print(self.grid_map)
        print(self.orientation)
        
class Map_Node():

    #This one should be used :)
    def __init__(self, pos, parent_node=None):
        if(parent_node == None):
            self.position = pos
            #NORTH, EAST, SOUTH, WEST
            self.cardinal_available = [None, None, None, None]
            self.visited = True

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

    def __repr__(self):
        #return "Node <", self.northAvailable, self.northTraveled, self.eastAvailable, self.eastTraveled, self.southAvailable, self.southTraveled, self.westAvailable, self.westTraveled, ">"
        return str(self.position)

    def __eq__(self, other):
        return isinstance(other, Map_Node) and self.position == other.position

    def __hash__(self):
        print("GAAAH")
        return hash(self.position)
