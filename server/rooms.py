from collections import OrderedDict
import settings

# Right now, only one room works, with the illusion that multiple rooms can.

#rooms = OrderedDict([(1, [])])

# Signifies private with the "_"
_room_list = {}
_sid_to_room_id = {}

# Creates a player for the room with the id passed in. 
# Returns true if you are the first player. False if not.
def assign_room(sid, room_id):
    _sid_to_room_id[sid] = room_id

    _room = get_room(room_id)
    player_count = get_total_players(room_id)
    _room[sid] = settings.create_player(player_count)

    return len(_room) == 1

def room_to_list(room_id):
    if room_id in _room_list:
        _room = _room_list[room_id]
        return [_room[k] for k in _room]
    else:
        return []

def spawn_players(room_id):
    _room = get_room(room_id)
    coords = settings.calc_player_spawn_coords(len(_room))
    rooms = room_to_list(room_id)

    for i, val in enumerate(rooms):
        val['x'] = coords[i][0]
        val['y'] = coords[i][1]

# Removes the player from whatever room it may be in.
def remove_player(sid):
    global _sid_to_room_id
    room_id = sid_to_room_id(sid)
    _room = get_room(room_id)

    if sid in _room:
        del(_room[sid])
        del(_sid_to_room_id[sid])

# This function is like a proof of concept or sumthin. It would act like a
# garbage collector, and it should be called every so often that the server is
# alive.
def clean_empty_rooms():
    global _room_list
    for room_id in _room_list:
        if len(_room_list[room_id]) == 0:
            destroy_room(room_id)

def destroy_room(room_id):
    global _room_list
    if room_id in _room_list:
        # Enforcing garbage collection I suppose.
        # Can't hurt to be safe :P, or can it?
        _room_list[room_id].clear()
        del(_room_list[_room_id])

def get_total_players(room_id):
    _room = get_room(room_id)
    return 0 if _room == None else len(_room)

def get_room(room_id):
    global _room_list
    if not room_id in _room_list:
        _room_list[room_id] = {}
    return _room_list[room_id]

def sid_to_room_id(sid):
    global _sid_to_room_id
    return _sid_to_room_id[sid]


def get_player(sid):
    room_id = sid_to_room_id(sid)
    return get_room(room_id)[sid]
