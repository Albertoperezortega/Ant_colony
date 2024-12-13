class Fruit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.lives = 3

    def get_position(self):
        return self.x, self.y
    
    def picked_up(self):
        if self.lives > 0:
            self.lives -= 1

        if self.lives == 0:
            self.alive = False
