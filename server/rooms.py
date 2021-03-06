import datetime
import settings
import players
import random
import grid

# Signifies private with the "_"
_room_list = {}
_sid_to_room_id = {}
_current_room_to_assign = None
_room_started = {}
_room_next_color = {}


def get_room(room_id):
    global _room_list
    if room_id not in _room_list:
        return None
    return _room_list[room_id]


# Generate room id. Currently just the time the room was made
def gen_room_id():
    return str(datetime.datetime.now())


def get_available_room_id():
    global _current_room_to_assign
    current_room = get_room(_current_room_to_assign)

    # Needs to check if room has started a game as well
    # Filter out dead players because players who leave the room before it
    # starts are marked dead
    if (not current_room or
        len(current_room) == settings.max_players or
            has_game_started(_current_room_to_assign)):
        _current_room_to_assign = gen_room_id()

    return _current_room_to_assign


# Creates a player for the room with the id passed in.
# Returns true if you are the first player. False if not.
# Returns the room_id as a second value
def assign_room(sid, room_id=None):
    # Can't use function as a default value. It will get evaluated
    # only once. So we have to do it this way
    room_id = room_id if room_id else get_available_room_id()
    _sid_to_room_id[sid] = room_id
    print(sid, "is entering room", room_id)

    room = get_room(room_id)

    if not room:
        room = new_room(room_id)

    player_count = get_total_players(room_id)

    room[sid] = players.create_player(player_count, room_id)

    return len(room) == 1, room_id, room[sid]['num']


def room_to_list(room_id):
    if room_id in _room_list:
        _room = _room_list[room_id]
        return [_room[k] for k in _room]
    else:
        return []


def spawn_players(room_id, with_collision=False):
    _room = get_room(room_id)
    coords = players.calc_player_spawn_coords(len(_room))
    players_in_room = room_to_list(room_id)

    for i, player in enumerate(players_in_room):
        player['x'] = coords[i][0]
        player['y'] = coords[i][1]
        if with_collision:
            grid.mark_loc(room_id, player['x'], player['y'])


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
        # don't associate the sid with the room anymore
        for sid, player in _room_list[room_id].items():
            _sid_to_room_id[sid] = None

        _room_started[room_id] = None
        _room_next_color[room_id] = None
        # Enforcing garbage collection I suppose.
        # Can't hurt to be safe :P, or can it?
        _room_list[room_id].clear()
        del(_room_list[room_id])


def get_total_players(room_id):
    room = get_room(room_id)
    return 0 if room is None else len(room)


# This will reset any existing rooms to an empty state
def new_room(room_id):
    global _room_list
    room = _room_list[room_id] = {}
    _room_next_color[room_id] = random.randrange(0, len(settings.player_colors))
    return room


def mark_room_as_started(room_id):
    _room_started[room_id] = True


def has_game_started(room_id):
    return room_id in _room_started


def sid_to_room_id(sid):
    global _sid_to_room_id
    return _sid_to_room_id[sid]


def get_alive_players(room_id):
    return list(filter(lambda player: player['alive'], room_to_list(room_id)))


def remove_dead_players(room_id):
    room = get_room(room_id)
    filtered_room = {}
    player_count = 0

    sorted_room = sorted(room.items(), key=lambda p: p[1]['num'])
    for sid, player in sorted_room:
        if player['alive']:
            player['num'] = player_count + 1
            filtered_room[sid] = player
            player_count = player_count + 1
        else:
            _sid_to_room_id[sid] = None

    _room_list[room_id] = filtered_room


def get_player(sid):
    room_id = sid_to_room_id(sid)
    return get_room(room_id)[sid] if room_id else None

