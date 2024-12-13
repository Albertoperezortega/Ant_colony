import random
import time
import os
from board import Board
from ant import Ant
from fruit import Fruit
from colony import Colony

def clear_console():
    # Clears the terminal screen for better display
    os.system('cls' if os.name == 'nt' else 'clear')

def start(length, width, fruits, ants, colony):
    game_board = Board(length, width)
    game_board.generate_board(fill="_")

    #Fruits
    fruits[0] = Fruit(5, 5)
    fruits[1] = Fruit(6,0)

    #Ants
    ants[0] = Ant(9, 0)
    ants[1] = Ant(0, 9)
    ants[2] = Ant(1,1)

    game_board.update_board(ants, colony, fruits)

    return game_board

def main():
    ants = {}
    fruits = {}
    colony = Colony(0,0)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
    length = 10
    width = 10

    game_board = start(length, width, fruits, ants, colony)
    game_board.display_board()
    


    def loop():
        ant_output = ""
        events_output = ""
        for ant in ants:
            #checks if and to what fruit the ant should move

            #if the ant is carrying food=
            if (ants[ant].food):
                move_x, move_y = ants[ant].direction_towards_object(colony)
                old_x, old_y = ants[ant].get_position()
                if game_board.move_piece_ant(ants[ant], fruits, old_x, old_y, move_x, move_y):
                    game_board.deposit_pheromone(old_x, old_y, amount=5)
                    game_board.update_board(ants, colony, fruits)
                    ant_output += f"Ant {ant}: returning \t"
                #stores the fruit object closest to that ant

            else:
                # Check if there are pheromones to follow
                x, y = ants[ant].get_position()
                dx, dy = game_board.get_highest_pheromone_direction(x, y)


                
                closest_fruit_dst = 9999
                closest_fruit = None
                for fruit in fruits:
                    #if the food is not being taken by another ant =
                    if (fruits[fruit].alive):

                        dist = ants[ant].distance_to_object(fruits[fruit])
                        #if the food is closer than the one before =    
                        if (closest_fruit_dst > dist) and (dist <= ants[ant].smell_radius):
                            
                            closest_fruit_dst = dist
                            closest_fruit = fruits[fruit]

                if closest_fruit:
                    move_x, move_y = ants[ant].direction_towards_object(closest_fruit)
                    old_x, old_y = ants[ant].get_position()
                    if game_board.move_piece_ant(ants[ant], fruits, old_x, old_y, move_x, move_y):
                        game_board.update_board(ants, colony, fruits)
                        ant_output += f"Ant {ant}: found fruit \t"
                elif (dx, dy) != (0, 0):  # Follow pheromone trail
                    old_x, old_y = ants[ant].get_position()
                    if game_board.move_piece_ant(ants[ant], fruits, old_x, old_y, dx, dy):
                        game_board.update_board(ants, colony, fruits)
                        ant_output += f"Ant {ant}: follow pheromone \t"
                else:
                    #this just prompts the ants to move in random directions if there is nothing to follow
                    ant_output += f"Ant {ant}: exploring \t"
                    random.shuffle(directions)

                    for move_x, move_y in directions:
                        old_x, old_y = ants[ant].get_position()
                        new_x, new_y = old_x + move_x, old_y + move_y


                        if (0 <= new_x < length and 0 <= new_y < width) and game_board.is_space_free((new_x, new_y)) == "free":
                            if game_board.move_piece_ant(ants[ant], fruits, old_x, old_y, move_x, move_y):
                                game_board.update_board(ants, colony, fruits)
                                break
            ant_events = game_board.get_events()
            for event in ant_events:
                events_output += f"Ant {ant}: {event}\t"


        game_board.decay_pheromones(decay_rate=0.5)
        return ant_output, events_output

    i = 0
    while True:
        output = ""
        i += 1
        ant_status, events = loop()
        time.sleep(1)
        board_output = game_board.display_board()
        output += f"Turn: {i}\n{board_output}\n{ant_status}\n{events}\n"
        
        clear_console()
        print(output)

        fruits_alive = 0
        for fruit in fruits:
            if fruits[fruit].alive:
                fruits_alive += 1
        if fruits_alive == 0:
            food_moving = 0
            for ant in ants:
                if ants[ant].food:
                    food_moving += 1
            if food_moving == 0:
                print("All fruits are gone!")
                return
                
            


if __name__ == "__main__":
    main()




