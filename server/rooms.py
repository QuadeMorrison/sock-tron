from collections import OrderedDict
import settings

#rooms = OrderedDict([(1, [])])

# Signifies private with the "_"
_room = {}

# Creates a player for the room, and returns the id of the room that the player
# was assigned to.
def assign_room(sid):
    # open_room = list(rooms.keys())[-1]
    # num_players_in_room = len(rooms.get(open_room))

    # if (not num_players_in_room < settings.max_players):
        # open_room += 1
        # rooms.update({open_room : []})
        # num_players_in_room = 0

    player_count = get_total_players(1)
    _room[sid] = settings.create_player(player_count, settings.max_players)

    return 1

# Returns false if that player didn't even exist in the first place.
# May want to change that to an exception instead...
def remove_player(sid):
    if sid in _room:
        del(_room[sid])
        return True
    else:
        return False

def get_total_players(room_ind):
    return len(_room)

def get_room(room_ind):
    return _room
