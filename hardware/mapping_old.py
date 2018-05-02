from hardware import NORTH, SOUTH, WEST, EAST

class Map(object):
    def __init__(self):
        self.grid_map = {}
        self.current_position = (0,0)    
        self.orientation = NORTH
        self.grid_map[self.current_position] = MapNode()
        self.grid_map[self.current_position].set_available(NORTH, 'straight')

    def set_node(self, position, dire):
        self.current_position.add_child(map_node, dire)

    def analyze(self, dist_sensor):
        valid_moves = dist_sensor.get_possible_movements()

    def print(self):
        print(self.grid_map)
        print(self.current_position)
        print(self.orientation)
        
class MapNode():
    def __init__(self):
        self.northAvailable = False
        self.northTraveled = False
        self.eastAvailable = False
        self.eastTraveled = False
        self.southAvailable = False
        self.southTraveled = False
        self.westAvailable = False
        self.westTraveled = False

    def __repr__(self):
        #return "Node <", self.northAvailable, self.northTraveled, self.eastAvailable, self.eastTraveled, self.southAvailable, self.southTraveled, self.westAvailable, self.westTraveled, ">"
        return "NODE"

    def set_available(self, orientation, direction):
        if orientation == NORTH:
            if direction == 'left':
                self.westAvailable = True
            elif direction == 'straight':
                self.northAvailable = True
            elif direction == 'right':
                self.eastAvailable = True
        elif orientation == EAST:
            if direction == 'left':
                self.northAvailable = True
            elif direction == 'straight':
                self.eastAvailable = True
            elif direction == 'right':
                self.southAvailable = True
        elif orientation == SOUTH:
            if direction == 'left':
                self.eastAvailable = True
            elif direction == 'straight':
                self.southAvailable = True
            elif direction == 'right':
                self.westAvailable = True
        elif orientation == WEST:
            if direction == 'left':
                self.southAvailable = True
            elif direction == 'straight':
                self.westAvailable = True
            elif direction == 'right':
                self.northAvailable = True

    def get_neighbors(self, orientation):
        toreturn = []
        if orientation == NORTH:
            if self.westAvailable:
                toreturn.append('left')
            if self.northAvailable:
                toreturn.append('straight')
            if self.eastAvailable:
                toreturn.append('right')
        elif orientation == EAST:
            if self.northAvailable:
                toreturn.append('left')
            if self.eastAvailable:
                toreturn.append('straight')
            if self.southAvailable:
                toreturn.append('right')
        elif orientation == SOUTH:
            if self.eastAvailable:
                toreturn.append('left')
            if self.southAvailable:
                toreturn.append('straight')
            if self.westAvailable:
                toreturn.append('right')
        else: #orientation == WEST, presumably
            if self.southAvailable:
                toreturn.append('left')
            if self.westAvailable:
                toreturn.append('straight')
            if self.northAvailable:
                toreturn.append('right')
        return toreturn

