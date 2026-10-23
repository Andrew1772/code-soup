from blessed import Terminal
import random
import sys
import math
import argparse

import time

term = Terminal()

WALL = term.white("#")
FLOOR = term.gray(".")
PLAYER = term.gold("@")
DOOR = term.cyan("%")
SPIKE = term.red("^")
GOBLIN = term.red("G")
BOSS = term.green("B")

SWORD_HP = 3
LEVEL_NUM = 0


def display(dungeon):
    print(term.home + term.clear, end="")
    for row in dungeon:
        print("".join(row))

def create_dungeon_easy():
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

    player_x = random.randint(1, width - 2)
    player_y = random.randint(1, height - 2)

    for i in range(0, int(LEVEL_NUM * 2)):
        dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = SPIKE

    dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = DOOR
    dungeon[player_y][player_x] = PLAYER

    return dungeon, (player_x, player_y)

def create_dungeon_medium():
    width = 25
    height = 10
    global LEVEL_NUM
    goblins = {}

    dungeon = [["" for x in range(width)] for y in range(height)]

    for x in range(width):
        for y in range(height):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                dungeon[y][x] = WALL
            else:
                dungeon[y][x] = FLOOR

    player_x = random.randint(1, width - 2)
    player_y = random.randint(1, height - 2)

    for i in range(0, int(LEVEL_NUM * 2)):
        dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = SPIKE

    for i in range(0, int(LEVEL_NUM - 4)):
        goblin_x = random.randint(1, width - 2)
        goblin_y = random.randint(1, height - 2)

        dungeon[goblin_y][goblin_x] = GOBLIN
        goblins.update({i: (goblin_x, goblin_y, "RIGHT")})

    dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = DOOR
    dungeon[player_y][player_x] = PLAYER

    return dungeon, (player_x, player_y), goblins

def create_dungeon_hard():
    width = 35
    height = 15
    global LEVEL_NUM
    goblins = {}
    bosses = {}

    dungeon = [["" for x in range(width)] for y in range(height)]

    for x in range(width):
        for y in range(height):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                dungeon[y][x] = WALL
            else:
                dungeon[y][x] = FLOOR

    player_x = random.randint(1, width - 2)
    player_y = random.randint(1, height - 2)

    for i in range(0, int(LEVEL_NUM * 5)):
        dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = SPIKE

    for i in range(0, LEVEL_NUM * 2):
        goblin_x = random.randint(1, width - 2)
        goblin_y = random.randint(1, height - 2)

        dungeon[goblin_y][goblin_x] = GOBLIN
        goblins.update({i: (goblin_x, goblin_y, "RIGHT")})

    for i in range(0, int(LEVEL_NUM / 4)):
        boss_x = random.randint(1, width - 2)
        boss_y = random.randint(1, height - 2)

        dungeon[boss_y][boss_x] = BOSS
        bosses.update({i: (boss_x, boss_y)})

    dungeon[random.randint(1, height - 2)][random.randint(1, width - 2)] = DOOR
    dungeon[player_y][player_x] = PLAYER

    return dungeon, (player_x, player_y), goblins, bosses

def fight_boss(dungeon, player_x, player_y, key, goblins, bosses):
    global SWORD_HP

    if SWORD_HP >= 0:

        # Find the first key where the second element of the list matches target_coords
        boss = next((boss for boss, coords in bosses.items() if coords == (player_x, player_y)), None)

        bosses.pop(boss)
        SWORD_HP =- 1

        return True
    else:
        game_over("boss killed you")
    

def check_tile(dungeon, player_x, player_y, key = "", goblins = {}, bosses = {}):
    if dungeon[player_y][player_x] == WALL:
        return False

    if dungeon[player_y][player_x] == SPIKE:
        game_over("Spikes hurt!")

    if dungeon[player_y][player_x] == GOBLIN:
        # combat(dungeon, player_x, player_y)
        game_over("A Goblin killed you")

    if dungeon[player_y][player_x] == BOSS:
        return fight_boss(dungeon, player_x, player_y, key, goblins, bosses)

    if dungeon[player_y][player_x] == DOOR:
        SWORD_HP = 3
        finish_level()

    return True

def check_tile_boss(dungeon, boss_x, boss_y):
    if dungeon[boss_y][boss_x] != FLOOR:
        return False
    return True


def check_tile_goblin(dungeon, goblin_x, goblin_y):
    if dungeon[goblin_y][goblin_x] == SPIKE:
        return False
    if dungeon[goblin_y][goblin_x] == WALL: 
        return False
    if dungeon[goblin_y][goblin_x] == DOOR:
        return False
    if dungeon[goblin_y][goblin_x] == GOBLIN:
        return False
    if dungeon[goblin_y][goblin_x] == BOSS:
        return False
    
    return True


# this moves the goblins right or left and change when they hit something
def move_goblins(dungeon, goblins):

    for i in range(len(goblins)):
        goblin_x, goblin_y, direction = goblins[i]
        if direction == "RIGHT":
            if check_tile_goblin(dungeon, goblin_x + 1, goblin_y):
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x + 1] = GOBLIN
                goblins[i] = (goblin_x + 1, goblin_y, "RIGHT")
            elif check_tile_goblin(dungeon, goblin_x - 1, goblin_y):
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x - 1] = GOBLIN
                goblins[i] = (goblin_x - 1, goblin_y, "LEFT")


        if direction == "LEFT":
            if check_tile_goblin(dungeon, goblin_x - 1, goblin_y):
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x - 1] = GOBLIN
                goblins[i] = (goblin_x - 1, goblin_y, "LEFT")
            elif check_tile_goblin(dungeon, goblin_x + 1, goblin_y):
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x + 1] = GOBLIN
                goblins[i] = (goblin_x + 1, goblin_y, "RIGHT")

    return dungeon, goblins

# bosses will attempt to catch the player
def move_bosses(dungeon, player_coordinates, bosses):
    player_x, player_y = player_coordinates

    for i in range(len(bosses)):
        if i in bosses:
            boss_x, boss_y = bosses[i]
            dx = player_x - boss_x
            dy = player_y - boss_y

            if dx > 0:
                if check_tile_boss(dungeon, boss_x + 1, boss_y):
                    dungeon[boss_y][boss_x] = FLOOR
                    dungeon[boss_y][boss_x + 1] = BOSS
                    bosses[i] = (boss_x + 1, boss_y)
                    continue
            if dx < 0:
                if check_tile_boss(dungeon, boss_x - 1, boss_y):
                    dungeon[boss_y][boss_x] = FLOOR
                    dungeon[boss_y][boss_x - 1] = BOSS
                    bosses[i] = (boss_x - 1, boss_y)
                    continue
            if dy > 0:
                if check_tile_boss(dungeon, boss_x, boss_y + 1):
                    dungeon[boss_y][boss_x] = FLOOR
                    dungeon[boss_y + 1][boss_x] = BOSS
                    bosses[i] = (boss_x, boss_y + 1)
                    continue
            if dy < 0:
                if check_tile_boss(dungeon, boss_x, boss_y - 1):
                    dungeon[boss_y][boss_x] = FLOOR
                    dungeon[boss_y - 1][boss_x] = BOSS
                    bosses[i] = (boss_x, boss_y - 1)

    return dungeon, bosses



    return dungeon, bosses
def move_player(dungeon, player_coordinates, key, goblins, bosses):
    player_x, player_y = player_coordinates
    if goblins:
        dungeon, goblins = move_goblins(dungeon, goblins)

    if bosses:
        dungeon, bosses = move_bosses(dungeon, player_coordinates, bosses)

    if key == 'w':
        if check_tile(dungeon, player_x, player_y - 1, key, goblins, bosses):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y - 1][player_x] = PLAYER 
            return (player_x, player_y - 1)
        return (player_x, player_y)
    if key == 's':
        if check_tile(dungeon, player_x, player_y + 1, key, goblins, bosses):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y + 1][player_x] = PLAYER 
            return (player_x, player_y + 1)
        return (player_x, player_y)
    if key == 'd':
        if check_tile(dungeon, player_x + 1, player_y, key, goblins, bosses):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y][player_x + 1] = PLAYER 
            return (player_x + 1, player_y)
        return (player_x, player_y)
    if key == 'a':
        if check_tile(dungeon, player_x - 1, player_y, key, goblins, bosses):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y][player_x - 1] = PLAYER 
            return (player_x - 1, player_y)
        return (player_x, player_y)
    return (player_x, player_y)

def finish_level():
    global LEVEL_NUM
    LEVEL_NUM += 1

    if LEVEL_NUM < 5:
        new_dungeon, player_coordinates = create_dungeon_easy()
        run_game(new_dungeon, player_coordinates)
    elif LEVEL_NUM >= 5 and LEVEL_NUM < 15:
        new_dungeon, player_coordinates, goblins = create_dungeon_medium()
        run_game(new_dungeon, player_coordinates, goblins)
    elif LEVEL_NUM >= 15:
        new_dungeon, player_coordinates, goblins, bosses = create_dungeon_hard()
        run_game(new_dungeon, player_coordinates, goblins, bosses)



def game_over(message = ""):
    print(message, LEVEL_NUM)
    sys.exit()


def run_game(dungeon, player_coordinates, goblins = {}, bosses = {}):
    with term.cbreak(), term.hidden_cursor():
        display(dungeon)

        while True:
            key = term.inkey()

            if key == 'q':
                game_over()

            player_coordinates = move_player(dungeon, player_coordinates, key, goblins, bosses)
            display(dungeon)


# Starting the game
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--level', '-l',
        type=int,
        default=0,
        help="Input the level you want to start at (default=0)"
    )

    args = parser.parse_args()
    print(args)

    if args.level > 0:
        LEVEL_NUM = args.level - 1

    finish_level()
    display(dungeon)
    
    run_game(dungeon, player_coordinates)

