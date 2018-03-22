__all__ = ['create_object']
import math

# Takes in max_players as well, for different room maxes as a future option.
# This is BROKEN!!! Please fix me.
def create_player(player_count):
    # The position is calculated when the match actually starts.
    global player_colors
    # Left is the default for now.
    return { 'color': player_colors[player_count], 'x': 0, 'y': 0, 'dir': 'left', 'alive': True }

# Figures out starting positions in a variable manner.
def calc_player_spawn_coords(num_of_players):
    global window, window_xpad, window_ypad

    spawn_w = window['width']  - window_xpad * 2
    spawn_h = window['height'] - window_ypad * 2

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
            x = math.floor(j*spawn_w / col_len + spawn_w / (2*col_len) + window_xpad)
            y = math.floor(i*spawn_h / row_len + spawn_h / (2*row_len) + window_ypad)

            coords.append( (x, y) )

    return coords
    print(coords)

    return { 'color': "red", 'x': 0, 'y': 0 }

# 17 colors for now. These are all very basic colors.
player_colors = ["#FF0000", "#00FFFF", "#C0C0C0", "#0000FF", "#808080", "#0000A0", "#000000", "#ADD8E6", "#FFA500", "#800080", "#A52A2A", "#FFFF00", "#800000", "#00FF00", "#008000", "#FF00FF", "#808000"]

window = { 'height': 50, 'width': 50 }

# Measured in blocks (NOT PIXELS!)
# The padding of the player spawn.
window_xpad = 2
window_ypad = 2

player_direction = "up"
player_details = []
max_players = 17 # Because only 17 colors right now.

def get_settings_obj():
    global window
    return {
        'window': window
    }
