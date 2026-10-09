# --- VARIABLES --- #

# Dungeon dimensions
WIDTH = 30  # num cols
HEIGHT = 15 # num rows

# Tile types
WALL = "#"
FLOOR = "."

# Room dimensions
ROOMS = [(2, 2, 4, 4), (8, 8, 6, 6)]


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


if __name__ == "__main__":

    # Create the initial game state, of all walls
    grid = [[WALL for x in range(WIDTH)] for y in range(HEIGHT)]

    for room in ROOMS:
       create_room(grid, *room)

    # center_x = x + width / 2
    # center_y = y + / 2
    point_a = (4, 4)
    point_b = (11, 11)

    connect_rooms(grid, point_a, point_b)

    display(grid)
