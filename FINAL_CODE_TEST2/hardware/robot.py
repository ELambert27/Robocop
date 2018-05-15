from hardware import *
import time
import math

class robot(object):
    def __init__(self):
        self.gpg = easygopigo3.EasyGoPiGo3()
        self.wc = Wheel_Controller(self.gpg)
        self.ds = Distance_Sensor(self.gpg)
        self.orientation = NORTH
        self.position = (0,0)
        self.map = Map()
        self.map.add_node_basic(self.position)                
        self.location_stack = []

    def go(self):
        flag = True
        while flag:
        
            print('---------------- loop start ----------------\n')
            print('current position:', self.position)
            if self.orientation == 0:
                to_print = '0-north'
            elif self.orientation == 1:
                to_print = '1-east'
            elif self.orientation == 2:
                to_print = '2-south'
            elif self.orientation == 3:
                to_print = '3-west'
            print('current orientation:', to_print)
            print('location stack:', self.location_stack)
            print()
            
            if self.map.nodes[self.position].is_visited != 2:
                print('>>>>>> open node <<<<<<')
                forward_dist = self.move_and_correct(14)
                print('***move forward:', forward_dist)
                print()
                if forward_dist == 14:
                    available_directions = self.ds.get_valid_directions()
                    new_node = self.map.add_node(self.position, self.orientation)
                    available_directions = self.remove_extra_directions(available_directions)
                    for i in range(len(available_directions)):
                        if available_directions[i] == 'left':
                            available_directions[i] = (self.orientation - 1) % 4
                        elif available_directions[i] == 'straight':
                            available_directions[i] = self.orientation
                        elif available_directions[i] == "right":
                            available_directions[i] = (self.orientation + 1) % 4
                    
                    self.map.nodes[new_node].available_directions = available_directions
                    self.move_and_correct(14)
                    self.position = new_node
                    self.map.nodes[self.position].is_visited = 1
                    self.location_stack.append(self.position)
                    print('***move to:', self.position)
                else:
                    self.move_and_correct(14)
                    print('***stay in the same node')
                    
                print('available directions:', self.map.nodes[self.position].available_directions)
                
                if len(available_directions) == 0:
                    self.wc.rotate_left(180)
                    print('***turn back')
                    self.orientation = (self.orientation - 2) % 4
                    self.map.nodes[self.position].is_visited = 2
                else:
                    next_direction = available_directions[0]
                    self.turn_to_direction(next_direction)
                    available_directions.remove(next_direction)
                    
                    if next_direction == 0:
                        to_print = 'north'
                    elif next_direction == 1:
                        to_print = 'east'
                    elif next_direction == 2:
                        to_print = 'south'
                    elif next_direction == 3:
                        to_print = 'west'
                    print('***turn to:', to_print)

            else:
                print('>>>>>> closed node <<<<<<')
                previous_node = self.location_stack.pop()
                if len(self.location_stack) == 0:
                    print("We're done")
                    flag = False
                else:
                    even_previous_node = self.location_stack[len(self.location_stack) - 1]
                    self.turn(previous_node, even_previous_node)
                    self.move_and_correct(14)
                    self.move_and_correct(14)
                    self.position = even_previous_node
                    
                    # if len(self.map.nodes[self.position].available_direction) != 0:
                    #     print(self.position, 'is an open node\n availabe directions:', self.map.nodes[self.position].available_direction)
                    #     next_direction = self.map.nodes[self.position].available_direction[0]
                    #     self.turn_to_direction(next_direction)
                    #     self.map.nodes[self.position].available_direction.remove(next_direction)

                    #     if next_direction == 0:
                    #         to_print = 'north'
                    #     elif next_direction == 1:
                    #         to_print = 'east'
                    #     elif next_direction == 2:
                    #         to_print = 'south'
                    #     elif next_direction == 3:
                    #         to_print = 'west'
                    #     print('***turn to:', to_print)
                        
                    # else:
                    #     print(self.position, 'is a closed node')
                    #     self.map.nodes[self.position].is_visited = 2
                    
            print('---------------- loop done ----------------\n')
            #time.sleep(3)            

    def remove_extra_directions(self, available_directions):
        if self.orientation == NORTH:
            try:
                available_directions['left']
                if self.map.nodes[(self.position[0] - 1, self.position[1] + 1)].is_visited > 0:
                    available_directions.remove('left')
            except:
                time.sleep(0)
            try:
                available_directions['straight']
                if self.map.nodes[(self.position[0], self.position[1] + 2)].is_visited > 0:
                    available_directions.remove('straight')
            except:                                                                                                  
                time.sleep(0)
            try:
                available_directions['right']
                if self.map.nodes[(self.position[0] + 1, self.position[1] + 1)].is_visited > 0:
                    available_directions.remove('right')
            except:                                                                                                              
                time.sleep(0)
        if self.orientation == EAST:
            try:
                available_directions['left']
                if self.map.nodes[(self.position[0] + 1, self.position[1] + 1)].is_visited > 0:
                    available_directions.remove('left')
            except:
                time.sleep(0)
            try:
                available_directions['straight']
                if self.map.nodes[(self.position[0] + 2, self.position[1])].is_visited > 0:
                    available_directions.remove('straight')
            except:
                time.sleep(0)
            try:
                available_directions['right']
                if self.map.nodes[(self.position[0] + 1, self.position[1] - 1)].is_visited > 0:
                    available_directions.remove('right')
            except:
                time.sleep(0)

        if self.orientation == SOUTH:
            try:
                available_directions['left']
                if self.map.nodes[(self.position[0] + 1, self.position[1] - 1)].is_visited > 0:
                    available_directions.remove('left')
            except:
                time.sleep(0)
            try:
                available_directions['straight']
                if self.map.nodes[(self.position[0], self.position[1] - 2)].is_visited > 0:
                    available_directions.remove('straight')
            except:
                time.sleep(0)
            try:
                available_directions['right']
                if self.map.nodes[(self.position[0] - 1, self.position[1] - 1)].is_visited > 0:
                    available_directions.remove('right')
            except:
                time.sleep(0)        
        
        if self.orientation == WEST:
            try:
                available_directions['left']
                if self.map.nodes[(self.position[0] - 1, self.position[1] - 1)].is_visited > 0:
                    available_directions.remove('left')
            except:
                time.sleep(0)
            try:
                available_directions['straight']
                if self.map.nodes[(self.position[0] - 2, self.position[1])].is_visited > 0:
                    available_directions.remove('straight')
            except:
                time.sleep(0)
            try:
                available_directions['right']
                if self.map.nodes[(self.position[0] - 1, self.position[1] + 1)].is_visited > 0:
                    available_directions.remove('right')
            except:
                time.sleep(0)

        return available_directions

    def move_and_correct(self, distance_threshold):
        self.ds.set_angle(180)
        first_dist_reading = self.ds.get_distance()

        self.ds.set_angle(90)
        forward_dist = self.ds.get_distance()

        if(forward_dist < distance_threshold + 2):
            forward_dist = forward_dist - 2
        else:
            forward_dist = distance_threshold

        self.wc.move_cm(forward_dist)
        self.ds.set_angle(180)
        
        second_dist_reading = self.ds.get_distance()
       
        if abs(second_dist_reading - first_dist_reading) > .25 and abs(second_dist_reading - first_dist_reading) < 7 and forward_dist != 0 and (first_dist_reading < 14 or second_dist_reading < 14):
            angle_in_rads = math.atan(float(second_dist_reading) / (float(forward_dist) + float(-forward_dist) * float(first_dist_reading)) / (float(first_dist_reading) - float(second_dist_reading)))

            angle_in_degrees = angle_in_rads * 180 / math.pi
            if angle_in_degrees > 1:    
                self.wc.move_cm(-forward_dist)
                time.sleep(.25)
                self.wc.rotate_left(angle_in_degrees)
                time.sleep(.25)
                self.wc.move_cm(forward_dist)
                time.sleep(.25)

        self.ds.set_angle(180)
        after_move_reading_left = self.ds.get_distance()
        #print("forward_dist: " + str(forward_dist))
        #print("After move reading left: " + str(after_move_reading_left))
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
        #print("After move reading right: " + str(after_move_reading_right))
        if after_move_reading_right < 11.5:
            offset = distance_threshold - 2.5 - after_move_reading_right
            self.wc.rotate_right(30)
            time.sleep(.25)
            self.wc.move_cm(-(offset / math.sin(math.pi/6)))
            time.sleep(.25)
            self.wc.rotate_left(30)
            time.sleep(.25)
            self.wc.move_cm(offset / math.tan(math.pi/6))
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
            if self.maze_map.all_children_visited(self.current_map_node):
                self.current_map_node.status_value = 2
            else:
                self.current_map_node.status_value = 1
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
            self.move_and_correct(14)
            time.sleep(.25)
            self.current_map_node.visited = True
            if self.maze_map.all_children_visited(self.current_map_node):
                self.current_map_node.status_value = 2
            else:
                self.current_map_node.status_value = 1
            self.current_map_node = node
                        
    def turn(self, previous_node, next_node):
        cur_pos = previous_node
        next_pos = next_node

        #print("Current position is: " + str(cur_pos))
        print('Going back to:', next_pos)
        
        # We need to go west
        if(cur_pos[0] > next_pos[0]):
            print('***turn to: west')
            card_direction = WEST
        # We need to go east
        elif(cur_pos[0] < next_pos[0]):
            print('***turn to: east')
            card_direction = EAST
        # We need to go south
        elif(cur_pos[1] > next_pos[1]):
            print('***turn to: south')
            card_direction = SOUTH
        # We need to go north
        elif(cur_pos[1] < next_pos[1]):
            print('***turn to: north')
            card_direction = NORTH

        #print("orientation: " + str(self.orientation))
        #print("card_direction: " + str(card_direction))
        turn_direction = (card_direction - self.orientation) % 4
        #print(turn_direction)
        if(turn_direction == RIGHT):
            self.wc.rotate_right(90)
            self.orientation = (self.orientation + RIGHT) % 4 
        elif(turn_direction == LEFT):
            self.wc.rotate_left(90)
            self.orientation = (self.orientation + LEFT) % 4
        elif(abs(turn_direction) == BACKWARD):
            self.wc.rotate_left(180)
            self.orientation = (self.orientation + BACKWARD) % 4
            
    def turn_to_direction(self, direction):
            turn_direction = (direction - self.orientation) % 4
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
                self.maze_map.add_node(new_map_node)
                self.current_map_node.cardinal_available[card_left] = new_map_node.position
            except:
                print("Not adding a new node because one already exists")
        if corridor_dists[1] > 17:
            try:
                new_map_node = self.get_new_node(card_straight)
                new_nodes.add(new_map_node)
                self.maze_map.add_node(new_map_node)
                self.current_map_node.cardinal_available[card_straight] = new_map_node.position
            except:
                print("Not adding a new node because one already exists")
        if corridor_dists[2] > 17:
            try:
                new_map_node = self.get_new_node(card_right)
                new_nodes.add(new_map_node)
                self.maze_map.add_node(new_map_node)
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
