import math

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food = False
        self.smell_radius = 2

    def get_position(self):
        return self.x, self.y
    
    def distance_to_object(self, object):
        x, y = object.get_position()
        #using manhattan distance to calculate total distance by usign the absolute value between both xs and ys
        return abs(self.x - x) + abs(self.y - y)

    
    def direction_towards_object(self, object):
        x, y = object.get_position()
        move_x = 0
        move_y = 0

        if self.x < x:
            move_x += 1
        elif self.x > x:
            move_x -= 1
        else:
            pass


        if self.y < y:
            move_y += 1
        elif self.y > y:
            move_y -= 1
        else:
            pass

        return move_x, move_y
    
    def move_ant(self, x, y):
        self.x = x
        self.y = y

    def grab_fruit(self):
        self.food = True





    

