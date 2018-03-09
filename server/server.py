import settings
from aiohttp import web
import socketio

START_POS = { 'x': 245, 'y': 245 }

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on('connect')
async def connect(sid, environ):
    print("connect ", sid)

@sio.on('init_game')
async def init_game(sid, window, player):
    settings.window = window
    settings.player = player

    await send_position(settings.get_start_position())

@sio.on('keydown')
async def keydown(sid, key, position):
    print("keydown: ", key, position)
    dimension = "width" if (key == "left" or key == "right") else "height"
    player_size = settings.player[dimension]
    move_by = player_size if (key == "left" or key == "up") else 0 - player_size
    position["x" if (dimension == "width") else "y"] -= move_by

    await send_position(position)


async def send_position(position):
    await sio.emit("update_position", position)

if __name__ == '__main__':
    web.run_app(app)
