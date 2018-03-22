from aiohttp import web
import socketio
import asyncio
import settings
import rooms
import sys

# Important.
# Right now, only room_main works, but you can add new rooms.

# Taken from: https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

sio = socketio.AsyncServer()

@sio.on('connect')
async def connect(sid, environ):
    # What does await emit do, does it wait for a verification to come from the
    # client? If not, then that await is pointless, right?
    await sio.emit('init_settings', settings.get_settings_obj())
    print('Connected', sid)

# Room test
@sio.on('enter_room')
def enter_room(sid, room_id):
    print(sid, "is entering room", room_id)

    # Join room
    is_new_room = rooms.assign_room(sid, room_id)

    # Spawn
    rooms.spawn_players(room_id)

    # Update will work.
    sio.enter_room(sid, room_id)

    # Wanna create a new room if there is a new one!
    if not is_new_room:
        print("Starting match with room", room_id)
        sio.start_background_task(update_players, room_id)

def exit_match(sid):
    pl = rooms.get_player(sid)
    pl['alive'] = False

    print(sid, "Leaving room")
    room_id = rooms.sid_to_room_id(sid)
    sio.leave_room(sid, room_id)

@sio.on('leave room')
async def leave_room(sid, data):
    exit_match(sid)

@sio.on('disconnect')
async def disconnect(sid):
    exit_match(sid)

@sio.on('keydown')
async def keydown(sid, key):
    room_id = rooms.sid_to_room_id(sid)
    pl = rooms.get_player(sid)
    prev_key = pl['dir']
    if (not (key == 'left'  and prev_key == 'right') and
        not (key == 'right' and prev_key == 'left')  and
        not (key == 'up'    and prev_key == 'down')  and
        not (key == 'down'  and prev_key == 'up')):
        pl['dir'] = key
        # print("%s: Turned %s." % (sid, key))

# This function can assume just one room.
async def update_players(room_ind):
    room = rooms.get_room(room_ind)

    while True:
        for k, v in room.items():
            dir = v['dir']
            dimension = "x" if (dir == "left" or dir == "right") else "y"
            move_by = 1 if (dir == "right" or dir == "down") else -1
            axis = "x" if (dimension == "x") else "y"

            v[axis] += move_by

        # Don't want to emit the sid of each client.
        emitted_list = rooms.room_to_list(room_ind)
        await asyncio.sleep(0.1)
        await sio.emit('update_players', emitted_list, room="main_room")

        # If everyone leaves the room, we don't need this thread anymore.
        leave = False
        for k, pl in room.items():
            if pl['alive']:
                leave = False
                break

        if leave or len(room) <= 0:
            break

    print("All players left room %d." % room_ind)
    rooms.destroy_room(room_ind)

if __name__ == '__main__':
    app = web.Application()
    sio.attach(app)
    web.run_app(app, port=8888)
