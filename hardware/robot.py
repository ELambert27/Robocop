from hardware import *
import time
import math

class robot(object):
    def __init__(self):
        self.gpg = easygopigo3.EasyGoPiGo3()
        self.wc = Wheel_Controller(self.gpg)
        self.ds = Distance_Sensor(self.gpg)
        self.orientation = NORTH
        self.current_map_node = Map_Node((0,0))
        self.maze_map = Map(self.current_map_node)
        self.unvisited_nodes = set()

    def go(self):
        self.move_and_correct(14)
        while(True):
            self.update_map()
            path = self.maze_map.find_path(self.current_map_node)
            print("Following path: " + str(path))
            time.sleep(.25)
            self.follow_path(path)
#            input("Press enter to continue") 

    def move_and_correct(self, distance_threshold):
        self.ds.set_angle(180)
        first_dist_reading = self.ds.get_distance()

        self.ds.set_angle(90)
        forward_dist = self.ds.get_distance()

        if(forward_dist < distance_threshold):
            forward_dist = forward_dist - 2
        else:
            forward_dist = distance_threshold

        self.wc.move_cm(forward_dist)
        self.ds.set_angle(180)
        
        second_dist_reading = self.ds.get_distance()
       
        if abs(second_dist_reading - first_dist_reading) > .25 and abs(second_dist_reading - first_dist_reading) < 6 and forward_dist != 0 and (first_dist_reading < 14 or second_dist_reading < 14):
            angle_in_rads = math.atan(float(second_dist_reading) / (float(forward_dist) + float(-forward_dist) * float(first_dist_reading)) / (float(first_dist_reading) - float(second_dist_reading)))

            angle_in_degrees = angle_in_rads * 180 / math.pi
            if angle_in_degrees > 10:    
                self.wc.move_cm(-forward_dist)
                self.wc.rotate_left(angle_in_degrees)
                self.wc.move_cm(forward_dist)

        self.ds.set_angle(180)
        after_move_reading_left = self.ds.get_distance()
        print("forward_dist: " + str(forward_dist))
        print("After move reading left: " + str(after_move_reading_left))
        if after_move_reading_left < 11.5:
            offset = distance_threshold - 2.5 - after_move_reading_left
            self.wc.rotate_left(30)
            time.sleep(.25)
            self.wc.move_cm(-(offset / math.sin(math.pi/6)))
            time.sleep(.25)
            self.wc.rotate_right(30)
            time.sleep(.25)
            self.wc.move_cm(offset / math.tan(math.pi/6))
        self.ds.set_angle(0) #0 is really 15 degrees 'cause of bad robot build
        after_move_reading_right = self.ds.get_distance() * math.cos(math.pi/12)
        print("After move reading right: " + str(after_move_reading_right))
        if after_move_reading_right < 11.5:
            offset = distance_threshold - 2.5 - after_move_reading_right
            self.wc.rotate_right(30)
            time.sleep(.25)
            self.wc.move_cm(-(offset / math.sin(math.pi/6)))
            time.sleep(.25)
            self.wc.rotate_left(30)
            time.sleep(.25)
            self.wc.move_cm(offset / math.tan(math.pi/6))
        #if after_move_reading_left > 13 and after_move_reading_left < 28:
        #    offset = after_move_reading_left - distance_threshold
        #    self.wc.rotate_right(30)
        #    time.sleep(.25)
        #    self.wc.move_cm(-(offset / math.sin(math.pi/6)))
        #    time.sleep(.25)
        #    self.wc.rotate_left(30)
        #    time.sleep(.25)
        #    self.wc.move_cm(offset / math.tan(math.pi/6))
        return forward_dist

    def follow_path(self, path):
        if len(path) == 0:
            #there is no valid path, so we turn around
            self.move_and_correct(14)
            self.wc.rotate_left(180)
            self.orientation = (self.orientation + BACKWARD) % 4
            time.sleep(.25)
            self.move_and_correct(14)
            time.sleep(.25)
            self.current_map_node.visited = True
            current_position = self.current_map_node.position
            current_position_x = current_position[0]
            current_position_y = current_position[1]
            if self.orientation == NORTH:
                current_position_x = current_position_x + 1
            elif self.orientation == EAST:
                current_position_y = current_position_y + 1
            elif self.orientation == SOUTH:
                current_position_x = current_position_y - 1
            elif self.orientation == WEST:
                current_position_x = current_position_x - 1
            self.current_map_node = self.maze_map.get_node(current_position)
        for node in path:
            self.move_and_correct(14)
            print("Turning")
            self.turn(node)
            time.sleep(.25)
            print("Moving and correcting")
            distance_moved = self.move_and_correct(14)
            time.sleep(.25)
            #if distance_moved > 13:
            self.current_map_node.visited = True
            self.current_map_node = node
                        
    def turn(self, next_node):
        cur_pos = self.current_map_node.position
        next_pos = next_node.position

        print("Current position is: " + str(cur_pos))
        print("Next positions is: " + str(next_pos))

        # We need to go west
        if(cur_pos[0] > next_pos[0]):
            print("Going west")
            card_direction = WEST
        # We need to go east
        elif(cur_pos[0] < next_pos[0]):
            print("Going east")
            card_direction = EAST
        # We need to go south
        elif(cur_pos[1] > next_pos[1]):
            print("going south")
            card_direction = SOUTH
        # We need to go north
        elif(cur_pos[1] < next_pos[1]):
            print("going north")
            card_direction = NORTH

        print("orientation: " + str(self.orientation))
        print("card_direction: " + str(card_direction))
        turn_direction = (card_direction - self.orientation) % 4
        print(turn_direction)
        if(turn_direction == RIGHT):
            self.wc.rotate_right(90)
            self.orientation = (self.orientation + RIGHT) % 4 
        elif(turn_direction == LEFT):
            self.wc.rotate_left(90)
            self.orientation = (self.orientation + LEFT) % 4
        elif(abs(turn_direction) == BACKWARD):
            self.wc.rotate_left(180)
            self.orientation = (self.orientation + BACKWARD) % 4

    def update_map(self):
        print("Currently at node ", self.current_map_node.position)
        print("We have " + str(self.current_map_node.cardinal_available) + " options")
        self.current_map_node.visited = True

        corridor_dists = self.ds.get_corridor_measurements()

        # Get the absolute directions
        card_left = (self.orientation - 1) % 4
        card_straight = (card_left + 1) % 4
        card_right = (card_straight + 1) % 4 
        new_nodes = set()
        if corridor_dists[0] > 17:
            try:
                new_map_node = self.get_new_node(card_left)
                new_nodes.add(new_map_node)
                self.maze_map.set_node(new_map_node)
                self.current_map_node.cardinal_available[card_left] = new_map_node.position
            except:
                print("Not adding a new node because one already exists")
        if corridor_dists[1] > 17:
            try:
                new_map_node = self.get_new_node(card_straight)
                new_nodes.add(new_map_node)
                self.maze_map.set_node(new_map_node)
                self.current_map_node.cardinal_available[card_straight] = new_map_node.position
            except:
                print("Not adding a new node because one already exists")
        if corridor_dists[2] > 17:
            try:
                new_map_node = self.get_new_node(card_right)
                new_nodes.add(new_map_node)
                self.maze_map.set_node(new_map_node)
                self.current_map_node.cardinal_available[card_right] = new_map_node.position
            except:
                print("Not adding a new node because one already exists")
        print("We now have " + str(self.current_map_node.cardinal_available) + " options")

    def get_new_node(self, direction):
        position = self.current_map_node.position
        if(direction == NORTH):
            print("New node to the north")
            new_pos = (position[0], position[1] + 1)
        elif(direction == EAST):
            print("New node to the east")
            new_pos = (position[0] + 1, position[1])
        elif(direction == SOUTH):
            print("New node to the south")
            new_pos = (position[0], position[1] - 1)
        else:
            print("New node to the west")
            new_pos = (position[0] - 1, position[1]) 
        
        try:
            map_node_to_return = self.maze_map.get_node(new_pos)
        except:
            return Map_Node(new_pos, self.current_map_node)
