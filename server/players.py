import settings
import grid
import rooms
import math


def create_player(player_count, dir='left'):
    # The position is calculated when the match actually starts.
    return {
        'color': settings.player_colors[player_count % settings.max_players],
        'x': 0,
        'y': 0,
        'dir': dir,
        'alive': True,
        'num': player_count + 1
    }


# Figures out starting positions in a variable manner.
def calc_player_spawn_coords(num_of_players):
    sp = settings.spawn_padding

    spawn_dim = settings.grid_dimensions(num_of_players) - sp * 2

    # Figure out how many rows and columns for each row.
    row_len = max(1, math.ceil(math.sqrt(num_of_players)))
    column_list = []
    col_bas = math.floor(num_of_players / row_len)
    row_ext = num_of_players % row_len

    for i in range(0, row_ext):
        column_list.append(col_bas + 1)

    for i in range(row_ext, row_len):
        column_list.append(col_bas)

    coords = []

    for i, col_len in enumerate(column_list):
        for j in range(col_len):
            x = math.floor(j*spawn_dim / col_len + spawn_dim / (2*col_len) + sp)
            y = math.floor(i*spawn_dim / row_len + spawn_dim / (2*row_len) + sp)

            coords.append((x, y))

    return coords
    print(coords)

    return {'color': "red", 'x': 0, 'y': 0}


def change_dir(player, key):
    prev_key = player['dir']
    if (not (key == 'left' and prev_key == 'right') and
        not (key == 'right' and prev_key == 'left') and
        not (key == 'up' and prev_key == 'down') and
            not (key == 'down' and prev_key == 'up')):
        player['dir'] = key


def move(room_id, player):
    dir = player['dir']
    dimension = "x" if (dir == "left" or dir == "right") else "y"
    move_by = 1 if (dir == "right" or dir == "down") else -1
    axis = "x" if (dimension == "x") else "y"

    player[axis] += move_by
    check_collision(room_id, player)
    check_out_of_bounds(room_id, player)


def check_collision(room_id, player):
    if (grid.is_marked(room_id, player['x'], player['y'])):
        player['alive'] = False


def check_out_of_bounds(room_id, player):
    room = rooms.room_to_list(room_id)
    x = player['x']
    y = player['y']

    x_lower_bound = 0
    y_lower_bound = 0
    upper_bound = settings.grid_dimensions(len(room))

    # Use >= for the upperbound otherwise the player stops a block later
    # than for the lower bound
    if (x <= x_lower_bound or x > upper_bound or
            y <= y_lower_bound or y > upper_bound):
        player['alive'] = False


def should_update(player):
    return player['alive']  # and not player['win']

