import random


class Board:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.board = []
        self.events = []

        self.pheromones = [[0 for _ in range(self.width)] for _ in range(self.length)]

    def generate_board(self, fill=None):
        self.board = [[fill for _ in range(self.width)] for _ in range(self.length)]
        return self.board
    
    def update_board(self, ants, colony, fruits):

        self.generate_board(fill="_")

        for i, value_i in enumerate(self.pheromones):
            for j, value_j in enumerate(value_i):
                if value_j:
                    self.board[i][j] = "#" 

        x, y = colony.get_position()
        self.board[x][y] = "C"

        for fruit in fruits.values():
            if fruit.alive:  
                x, y = fruit.get_position()
                self.board[x][y] = "F"


        for ant in ants.values():
            x, y = ant.get_position()
            self.board[x][y] = "A"

    def display_board(self):
        output = ""
        for row in self.board:
            output += (" ".join(row) + "\n")
        return output
    
    def get_events(self):
        self.events, events = [], self.events
        return events

    def deposit_pheromone(self, x, y, amount):
        if 0 <= x < self.length and 0 <= y < self.width:
            self.pheromones[x][y] += amount


    def decay_pheromones(self, decay_rate=0.1):

        for x in range(self.length):
            for y in range(self.width):
                self.pheromones[x][y] = max(0, self.pheromones[x][y] - decay_rate)
    
    
    def get_highest_pheromone_direction(self, x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1,1), (-1,1), (1,-1), (-1,-1)]  
        min_pheromone = 999
        best_direction = (0, 0)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.length and 0 <= ny < self.width:
                if 0 < self.pheromones[nx][ny] < min_pheromone:
                    min_pheromone = self.pheromones[nx][ny]
                    best_direction = (dx, dy)

        return best_direction
    

    def is_space_free(self, location):
        x, y = location
        if x < 0 or x >= self.length or y < 0 or y >= self.width:
            return False  
        elif (self.board[x][y] == "_") or (self.board[x][y] == "#"):
            return "free"
        elif self.board[x][y] == "F":
            return "fruit"   
        elif self.board[x][y] == "A":
            return "ant"
        elif self.board[x][y] == "C":
            return "colony"


    def move_piece_ant(self, ant, fruits, original_x, original_y, add_x, add_y):

        new_x = original_x + add_x
        new_y = original_y + add_y

        if not (0 <= new_x < self.length and 0 <= new_y < self.width):
            return False

        new_position_status = self.is_space_free((new_x, new_y))
        if new_position_status == "free":
        #if the position is free, move the ant there
            self.board[original_x][original_y] = "_"
            self.board[new_x][new_y] = "A"
            ant.move_ant(new_x, new_y) 

        elif new_position_status == "ant":
            if not ant.food:
            #moves to a random location if colliding with another ant
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
                for x, y in directions:
                    alt_x, alt_y = original_x + x, original_y + y
                    if (0 <= alt_x < self.length and 0 <= alt_y < self.width) and self.is_space_free((alt_x, alt_y)) == "free":
                        self.board[original_x][original_y] = "_"
                        self.board[alt_x][alt_y] = "A"
                        ant.move_ant(alt_x, alt_y)
                        return True 
            else:
                self.board[original_x][original_y] = "_"
                self.board[new_x][new_y] = "A"
                ant.move_ant(new_x, new_y) 


            
        elif new_position_status == "fruit":
        #if there is a fruit, the ant grabs it
            self.events.append("found fruit!")

            for fruit in fruits.values(): 
                #check the fruit its going to pick
                #print(fruit) 
                if fruit.get_position() == (new_x, new_y) and fruit.alive:
                    #grab the fruit its foing to pick
                    fruit.picked_up()
                    if not (fruit.alive):
                        self.board[new_x][new_y] = "_"  
                    break

            ant.grab_fruit()
            self.board[new_x][new_y] = "A"
            ant.move_ant(new_x, new_y)

        elif new_position_status == "colony":
        #if there is a colony, the ant places the food back
            self.events.append("returned to colony!")  
            ant.food = False
            ant.move_ant(new_x, new_y)

        return True