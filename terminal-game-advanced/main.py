from blessed import Terminal
import random
import sys

term = Terminal()

WALL = term.white("#")
FLOOR = term.black(".")
PLAYER = term.green("@")
DOOR = term.cyan("^")
ENEMY = term.red("&")
LEVEL_NUM = 0


def display(dungeon):
    print(term.home + term.clear, end="")
    for row in dungeon:
        print("".join(row))

def create_dungeon():
    width = 20
    height = 10
    global LEVEL_NUM

    dungeon = [["" for x in range(width)] for y in range(height)]

    for x in range(width):
        for y in range(height):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                dungeon[y][x] = WALL
            else:
                dungeon[y][x] = FLOOR

    player_x = random.randint(1, 18)
    player_y = random.randint(1, 8)

    for i in range(0, LEVEL_NUM):
        dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = ENEMY

    dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = DOOR
    dungeon[player_y][player_x] = PLAYER

    return dungeon, player_x, player_y

def check_tile(dungeon, player_x, player_y):
    if dungeon[player_y][player_x] == WALL:
        return False

    if dungeon[player_y][player_x] == ENEMY:
        game_over()

    if dungeon[player_y][player_x] == DOOR:
        finish_level()

    return True

def move_player(dungeon, player_x, player_y, key):
    if key == 'w':
        if check_tile(dungeon, player_x, player_y - 1):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y - 1][player_x] = PLAYER 
            return player_x, player_y - 1
        return player_x, player_y
    if key == 's':
        if check_tile(dungeon, player_x, player_y + 1):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y + 1][player_x] = PLAYER 
            return player_x, player_y + 1
        return player_x, player_y
    if key == 'd':
        if check_tile(dungeon, player_x + 1, player_y):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y][player_x + 1] = PLAYER 
            return player_x + 1, player_y
        return player_x, player_y
    if key == 'a':
        if check_tile(dungeon, player_x - 1, player_y):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y][player_x - 1] = PLAYER 
            return player_x - 1, player_y
        return player_x, player_y
    return player_x, player_y

def finish_level():
    global LEVEL_NUM
    LEVEL_NUM += 1

    new_dungeon, player_x, player_y = create_dungeon()
    run_game(new_dungeon, player_x, player_y)

def game_over():
    print(LEVEL_NUM)
    sys.exit()


def run_game(dungeon, player_x, player_y):
    with term.cbreak(), term.hidden_cursor():
        display(dungeon)

        while True:
            key = term.inkey()

            if key == 'q':
                break
            player_x, player_y = move_player(dungeon, player_x, player_y, key)
            display(dungeon)


dungeon, player_x, player_y = create_dungeon()
display(dungeon)

run_game(dungeon, player_x, player_y)

