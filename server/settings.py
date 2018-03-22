__all__ = ['create_object']
import math

def create_object(height = 0, width = 0):
    return { 'height': height, 'width': width }

# Takes in max_players as well, for different room maxes as a future option.
def create_player(player_num, max_players):
    num_players_in_y = math.floor(math.sqrt(max_players))
    num_players_in_x = max_players / num_players_in_y

    def calc_position(dimension, players_in_axis, player_num):
        player_num = player_num if players_in_axis > 1 else 1
        bound_end = 0 + window[dimension] * player_num / players_in_axis
        bound_end = bound_end if bound_end <= window[dimension] else window[dimension] / 2
        distance_from_bound_end = window[dimension] / players_in_axis / 2
        return bound_end - distance_from_bound_end

    x_player_num = player_num % num_players_in_x
    x = calc_position("width", num_players_in_x, x_player_num if x_player_num != 0 else num_players_in_x)
    y = calc_position("height", num_players_in_y, math.ceil(player_num / num_players_in_y))
    color = player_colors[player_num % len(player_colors) - 1]
    return { 'color': color, 'x': x, 'y': y }

player_colors = ['red','cyan','lime','yellow']
window = create_object(50, 50)
player_direction = "up"
player_details = []
max_players = 4

def get_settings_obj():
    global window
    return {
        'window': window
    }
