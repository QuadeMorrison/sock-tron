from collections import OrderedDict
import settings

# Right now, only one room works, with the illusion that multiple rooms can.

#rooms = OrderedDict([(1, [])])

# Signifies private with the "_"
_room = None
sid_to_room_id = {}

# Creates a player for the room, and returns the id of the room that the player
# was assigned to. Also returns a boolean of whether or not the room is brand new.
def assign_room(sid):
    global _room
    room_ind = 1

    sid_to_room_id[sid] = room_ind

    is_room_new = False
    if _room == None:
        _room = {}
        is_room_new = True

    player_count = get_total_players(room_ind)
    _room[sid] = settings.create_player(player_count)

    return room_ind, is_room_new

def room_to_list(room_ind):
    if _room != None:
        return [_room[k] for k in _room]
    else:
        return []

def spawn_players(room_ind):
    coords = settings.calc_player_spawn_coords(len(_room))
    rooms = room_to_list(room_ind)

    for i, val in enumerate(rooms):
        val['x'] = coords[i][0]
        val['y'] = coords[i][1]

# Returns false if that player didn't even exist in the first place.
# May want to change that to an exception instead...
def remove_player(sid):
    global _room
    if sid in _room:
        del(_room[sid])
        del(sid_to_room_id[sid])
        return True
    else:
        return False

def destroy_room(room_ind):
    global _room
    if _room != None:
        # Enforcing garbage collection I suppose.
        # Can't hurt to be safe :P, or can it?
        _room.clear()
        _room = None

def get_total_players(room_ind):
    global _room
    return 0 if _room == None else len(_room)

def get_room(room_ind):
    global _room
    return _room
