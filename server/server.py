from aiohttp import web
import socketio
import asyncio
import settings
import rooms
import sys

# Taken from: https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

sio = socketio.AsyncServer()

@sio.on('connect')
async def connect(sid, environ):
    room_ind, is_new_room = rooms.assign_room(sid)
    rooms.spawn_players(room_ind)
    print('Connected', sid)

    # What does await emit do, does it wait for a verification to come from the
    # client? If not, then that await is pointless, right?
    await sio.emit('init_settings', settings.get_settings_obj())

    # Wanna create a new room if there is a new one!
    if is_new_room:
        sio.start_background_task(update_players, room_ind)

@sio.on('disconnect')
async def disconnect(sid):
    if rooms.remove_player(sid):
        print('Disconnected: ', sid)
    else:
        eprint("WARNING: Disconnect without initial connect.")

@sio.on('keydown')
async def keydown(sid, key):
    room_id = rooms.sid_to_room_id[sid]
    room = rooms.get_room(room_id)
    prev_key = room[sid]['dir']
    if (not (key == 'left'  and prev_key == 'right') and
        not (key == 'right' and prev_key == 'left')  and
        not (key == 'up'    and prev_key == 'down')  and
        not (key == 'down'  and prev_key == 'up')):
        room[sid]['dir'] = key
        print("%s: Turned %s." % (sid, key))

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
        await sio.emit('update_players', emitted_list)
        # print(emitted_list)

        # If everyone leaves the room, we don't need this thread anymore.
        if len(room) <= 0:
            break

    print("All players left room %d." % room_ind)
    rooms.destroy_room(room_ind)

if __name__ == '__main__':
    app = web.Application()
    sio.attach(app)
    web.run_app(app, port=8888)


