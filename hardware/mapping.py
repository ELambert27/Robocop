from hardware import *
import time


class Map(object):
    def __init__(self):
        self.nodes = {}

    def add_node_basic(self, position):
        try: 
            self.nodes[position]
        except KeyError:
            self.nodes[position] = Map_Node(position)

    def add_node(self, position, direction):
        if direction == NORTH:
            new_position = (position[0], position[1] + 1)
        elif direction == EAST:
            new_position = (position[0] + 1, position[1])
        elif direction == SOUTH:
            new_position = (position[0], position[1] - 1)
        elif direction == WEST:
            new_position = (position[0] - 1, position[1])
        self.add_node_basic(new_position)
        return new_position

    def __repr__(self):
        return str(self.nodes)

class Map_Node():

    #This one should be used :)
    def __init__(self, pos):
        self.position = pos
        self.is_visited = 0
        self.available_direction = []

    def __repr__(self):
        return str(self.position)
