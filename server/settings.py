__all__ = ['create_object']
import math

def create_object(height = 0, width = 0):
    return { 'height': height, 'width': width }

def get_start_position(player_num):
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
    return { 'color': color, 'head_x': x, 'head_y': y, x: [y] }

player_colors = ['red','cyan','lime','yellow']
player = create_object(10, 10)
window = create_object(500, 500)
player_direction = "up"
player_disconnected = False
player_details = {}
max_players = 4

def get_settings_obj():
    global player
    global window
    return {
        'player': player,
        'window': window
    }
