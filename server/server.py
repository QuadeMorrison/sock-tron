from aiohttp import web
import socketio
import asyncio
import settings
import rooms

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on('connect')
async def connect(sid, environ):
    rooms.assign_room(sid)
    print('connected')
    await sio.emit('init_settings', settings.get_settings_obj())
    sio.start_background_task(move_player, sid)

@sio.on('disconnect')
async def disconnect(sid):
    print('disconnected')
    settings.player_disconnected = True

@sio.on('keydown')
async def keydown(sid, key):
    dir = settings.player_direction
    print(dir, key)
    if (not (dir == 'left' and key == 'right') and
        not (dir == 'right' and key == 'left') and
        not (dir == 'up' and key == 'down') and
        not (dir == 'down' and key == 'up')):
        settings.player_direction = key

async def move_player(sid):
    while True:
        player = settings.player_details[sid]
        room_players = rooms.get_players(player['room'])
        index = player['number'] - 1
        direction = settings.player_direction
        dimension = "width" if (direction == "left" or direction == "right") else "height"
        player_size = settings.player[dimension]
        move_by = player_size if (direction == "right" or direction == "down") else 0 - player_size
        axis = "x" if (dimension == "width") else "y"

        if (axis == "x"):
            room_players[index]['head_x'] += move_by
            head_x = room_players[index]['head_x']
            room_players[index][head_x] = []
            room_players[index][head_x].append(room_players[index]['head_y'])
        else:
            room_players[index]['head_y'] += move_by
            room_players[index][room_players[index]['head_x']].append(room_players[index]['head_y'])

        await asyncio.sleep(0.1)
        await sio.emit('move_player', room_players[index])


if __name__ == '__main__':
    web.run_app(app, port=8888)
