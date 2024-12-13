import random
from board import Board
from ant import Ant
from fruit import Fruit
from colony import Colony

def start(length, width, fruits, ants):
    game_board = Board(length, width)
    game_board.generate_board(fill="_")
    fruit = Fruit(3,2)
    fruits[0] = fruit

    ant = Ant(8,8) 
    ants[0] = (ant)
    return game_board

def main():
    ants = {}
    fruits = {}
    ant1 = Ant(1,1)
    ant1.move_towards_fruit(fruits)
    ant2 = Ant(2,2)
    ant3 = Ant(3,3)
    ants[0] = ant1
    ants[1] = ant2
    ants[2] = ant3

    print(ants.values.get_position())




if __name__ == "__main__":
    main()




