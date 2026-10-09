from blessed import Terminal

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


def run_game(dungeon, player_x, player_y):
    with term.cbreak(), term.hidden_cursor():
        key = term.inkey()
        print(key)

        while True:
            display(dungeon)
            if key == 'q':
                break
            else: 
                move_player(dungeon, player_x, player_y, key)



dungeon = create_dungeon(2, 2)
display(dungeon)

run_game(dungeon, 2, 2)

