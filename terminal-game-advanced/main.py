from blessed import Terminal
import time

term = Terminal()

WALL = term.white("#")
FLOOR = term.black(".")
PLAYER = term.green("@")


def display(dungeon):
    print(term.home + term.clear, end="")
    for row in dungeon:
        print("".join(row))

def create_dungeon(player_x, player_y):
    width = 20
    height = 10

    dungeon = [["" for x in range(width)] for y in range(height)]

    for x in range(width):
        for y in range(height):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                dungeon[y][x] = WALL
            else:
                dungeon[y][x] = FLOOR

    dungeon[player_y][player_x] = PLAYER

    return dungeon

def move_player(dungeon, player_x, player_y, key):
    if key == 'w':
        dungeon[player_y][player_x] = FLOOR
        dungeon[player_y - 1][player_x] = PLAYER 
        return player_x, player_y - 1
    if key == 's':
        dungeon[player_y][player_x] = FLOOR
        dungeon[player_y + 1][player_x] = PLAYER 
        return player_x, player_y + 1
    if key == 'd':
        dungeon[player_y][player_x] = FLOOR
        dungeon[player_y][player_x + 1] = PLAYER 
        return player_x + 1, player_y
    if key == 'a':
        dungeon[player_y][player_x] = FLOOR
        dungeon[player_y][player_x - 1] = PLAYER 
        return player_x - 1, player_y



def run_game(dungeon, player_x, player_y):
    with term.cbreak(), term.hidden_cursor():
        
        while True:
            time.sleep(.1)
            key = term.inkey()
            display(dungeon)
            if key == 'q':
                break

            player_x, player_y = move_player(dungeon, player_x, player_y, key)





dungeon = create_dungeon(2, 2)
display(dungeon)

run_game(dungeon, 2, 2)

