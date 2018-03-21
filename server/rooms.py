from collections import OrderedDict
import settings

rooms = OrderedDict([(1, [])])
playerDetails = {}

def assign_room(sid):
    open_room = list(rooms.keys())[-1]
    num_players_in_room = len(rooms.get(open_room))

    if (not num_players_in_room < settings.max_players):
        open_room += 1
        rooms.update({open_room : []})
        num_players_in_room = 0

    player_number = num_players_in_room + 1
    players = rooms.get(open_room).append(settings.get_start_position(player_number))
    settings.player_details[sid] = { 'room': open_room, 'number': player_number }

def get_players(room):
    return rooms.get(room)
