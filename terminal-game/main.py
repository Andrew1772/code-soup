# --- VARIABLES --- #

# Dungeon dimensions
WIDTH = 30  # num cols
HEIGHT = 15 # num rows

# Tile types
WALL = "#"
FLOOR = "."
PLAYER= "@"

# Room dimensions
#ROOMS = [(2, 2, 4, 4), (8, 8, 6, 6)]
ROOMS = [(8, 8, 6, 6), (2, 2, 4, 4), (20, 2, 5, 5)]


def create_room(grid, room_x, room_y, room_width, room_height):
    for x in range(room_x, room_x + room_width):
        for y in range(room_y, room_y + room_height):
            grid[y][x] = FLOOR

def create_horizontal_corridor(grid, x1, x2, y):
    # swap variables
    if x1 > x2:
        x1, x2 = x2, x1

    # create the corridor
    for x in range(x1, x2 + 1):
        grid[y][x] = FLOOR

def create_vertical_corridor(grid, y1, y2, x):
    # swap variables
    if y1 > y2:
        y1, y2 = y2, y1

    # create the corridor
    for y in range(y1, y2 + 1):
        grid[y][x] = FLOOR

def display(grid):
    for row in grid:
        print("".join(row))

def connect_rooms(grid, point_a, point_b):
    x1, y1 = point_a
    x2, y2 = point_b

    create_vertical_corridor(grid, y1, y2, x1)
    create_horizontal_corridor(grid, x1, x2, y2)

def find_center(x, y, height, width):
    return (int(x + width/2), int(y + height/2))


def create_level(height=HEIGHT, width=WIDTH, rooms=ROOMS):
    # Create the initial game state, of all walls
    grid = [[WALL for x in range(width)] for y in range(height)]

    corridors = []
    # add rooms
    for room in rooms:
        create_room(grid, *room)

        corridors.append(find_center(*room))

    # add corridors
    for i in range(len(corridors) - 1):
        connect_rooms(grid, corridors[i - 1], corridors[i])

    # Set player in the first room
    player_coordinates = find_center(*rooms[0])
    x, y = player_coordinates
    grid[y][x] = PLAYER

    # Start the game
    start_game(grid, player_coordinates)

def check_valid_tile(grid, x, y):
    if grid[y][x] == "#":
        return False
    else:
        return True


def move_player_icon(grid, player_input, player_coordinates):
    player_input = player_input.upper()
    x, y = player_coordinates

    match player_input:
        case "W":
            if check_valid_tile(grid, x, y - 1):
                grid[y][x] = FLOOR
                grid[y - 1][x] = PLAYER
                player_coordinates = (x, y - 1)
                return (grid, player_coordinates, "")
            else: 
                return (grid, player_coordinates, "Can't go there")
        case "S":
            if check_valid_tile(grid, x, y + 1):
                grid[y][x] = FLOOR
                grid[y + 1][x] = PLAYER
                player_coordinates = (x, y + 1)
                return (grid, player_coordinates, "")
            else: 
                return (grid, player_coordinates, "Can't go there")
        case "A":
            if check_valid_tile(grid, x - 1, y):
                grid[y][x] = FLOOR
                grid[y][x - 1] = PLAYER
                player_coordinates = (x - 1, y) 
                return (grid, player_coordinates, "")
            else: 
                return (grid, player_coordinates, "Can't go there")
        case "D":
            if check_valid_tile(grid, x + 1, y):
                grid[y][x] = FLOOR
                grid[y][x + 1] = PLAYER
                player_coordinates = (x + 1, y)
                return (grid, player_coordinates, "")
            else: 
                return (grid, player_coordinates, "Can't go there")
        case _:
            return(grid, player_coordinates, "Invaild Input")


def start_game(grid, player_coordinates):
    display(grid)
    while True:
        player_input = input("move with 'W' 'A' 'S' 'D'\n")
        grid, player_coordinates, comment = move_player_icon(grid, player_input, player_coordinates)
        display(grid)
        if comment:
            print(comment)
            comment = ""


if __name__ == "__main__":
    create_level()

