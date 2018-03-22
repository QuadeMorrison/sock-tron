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
    # Is this function thread safe? And how/why?
    # We don't need the room_num right now, prob in the future though.
    room_num = rooms.assign_room(sid)
    print('Connected', sid)

    # What does await emit do, does it wait for a verification to come from the
    # client? If not, then that await is pointless, right?
    await sio.emit('init_settings', settings.get_settings_obj())

@sio.on('disconnect')
async def disconnect(sid):
    if rooms.remove_player(sid):
        print('Disconnected: ', sid)
    else:
        eprint("WARNING: Disconnect without initial connect.")

@sio.on('keydown')
async def keydown(sid, key):
    dir = settings.player_direction
    print(dir, key)
    if (not (dir == 'left' and key == 'right') and
        not (dir == 'right' and key == 'left') and
        not (dir == 'up' and key == 'down') and
        not (dir == 'down' and key == 'up')):
        settings.player_direction = key

# This function can assume just one room.
async def update_players(room_ind):
    room = rooms.get_room(room_ind)

    while True:
        for k, v in room:
            player = v
            direction = settings.player_direction
            dimension = "width" if (direction == "left" or direction == "right") else "height"
            move_by = 1 if (direction == "right" or direction == "down") else -1
            axis = "x" if (dimension == "width") else "y"

            room[k][axis] += move_by

        await asyncio.sleep(0.1)
        sio.emit('update_players', room)
        print(room)

        # If everyone leaves the room, we don't need this thread anymore.
        if len(room) <= 0:
            print("All players left room %d." % room_ind)
            break

if __name__ == '__main__':
    app = web.Application()
    sio.attach(app)
    sio.start_background_task(update_players, 1)
    web.run_app(app, port=8888)


