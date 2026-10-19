from blessed import Terminal
import random
import sys

term = Terminal()

WALL = term.white("#")
FLOOR = term.gray(".")
# PLAYER = term.green("\U0001f47e") this is the purple dude, he's 2 spaces big
PLAYER = term.green("@")
DOOR = term.cyan("%")
SPIKE = term.red("^")
GOBLIN = term.red("G")
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

def check_tile(dungeon, player_x, player_y):
    if dungeon[player_y][player_x] == WALL:
        return False

    if dungeon[player_y][player_x] == SPIKE or dungeon[player_y][player_x] == GOBLIN:
        game_over()

    if dungeon[player_y][player_x] == DOOR:
        finish_level()

    return True

def move_goblins(dungeon, goblins):

    for i in range(len(goblins)):
        goblin_x, goblin_y, direction = goblins[i]
        if direction == "RIGHT":
            if dungeon[goblin_y][goblin_x + 1] == SPIKE or dungeon[goblin_y][goblin_x + 1] == WALL or dungeon[goblin_y][goblin_x + 1] == DOOR:
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x - 1] = GOBLIN
                goblins[i] = (goblin_x - 1, goblin_y, "LEFT")
            else: 
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x + 1] = GOBLIN
                goblins[i] = (goblin_x + 1, goblin_y, "RIGHT")

        if direction == "LEFT":
            if dungeon[goblin_y][goblin_x - 1] == SPIKE or dungeon[goblin_y][goblin_x - 1] == WALL or dungeon[goblin_y][goblin_x - 1] == DOOR:
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x + 1] = GOBLIN
                goblins[i] = (goblin_x + 1, goblin_y, "RIGHT")
            else: 
                dungeon[goblin_y][goblin_x] = FLOOR
                dungeon[goblin_y][goblin_x - 1] = GOBLIN
                goblins[i] = (goblin_x - 1, goblin_y, "LEFT")
    return dungeon, goblins


def move_player(dungeon, player_coordinates, key, goblins):
    player_x, player_y = player_coordinates
    if goblins:
        dungeon, goblins = move_goblins(dungeon, goblins)

    if key == 'w':
        if check_tile(dungeon, player_x, player_y - 1):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y - 1][player_x] = PLAYER 
            return (player_x, player_y - 1)
        return (player_x, player_y)
    if key == 's':
        if check_tile(dungeon, player_x, player_y + 1):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y + 1][player_x] = PLAYER 
            return (player_x, player_y + 1)
        return (player_x, player_y)
    if key == 'd':
        if check_tile(dungeon, player_x + 1, player_y):
            dungeon[player_y][player_x] = FLOOR
            dungeon[player_y][player_x + 1] = PLAYER 
            return (player_x + 1, player_y)
        return (player_x, player_y)
    if key == 'a':
        if check_tile(dungeon, player_x - 1, player_y):
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
    elif LEVEL_NUM >= 5:# and LEVEL_NUM < 15:
        new_dungeon, player_coordinates, goblins = create_dungeon_medium()
        run_game(new_dungeon, player_coordinates, goblins)


def game_over():
    print(LEVEL_NUM)
    sys.exit()


def run_game(dungeon, player_coordinates, goblins = {}):
    with term.cbreak(), term.hidden_cursor():
        display(dungeon)

        while True:
            key = term.inkey()

            if key == 'q':
                sys.exit()
            player_coordinates = move_player(dungeon, player_coordinates, key, goblins)
            display(dungeon)


dungeon, player_coordinates = create_dungeon_easy()
display(dungeon)

run_game(dungeon, player_coordinates)

