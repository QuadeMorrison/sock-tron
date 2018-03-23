from aiohttp import web
import socketio
import asyncio
import settings
import players
import grid
import rooms
import sys

# Taken from: https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

sio = socketio.AsyncServer()

@sio.on('connect')
async def connect(sid, environ):
    # What does await emit do, does it wait for a verification to come from the
    # client? If not, then that await is pointless, right?
    await sio.emit('init_settings', settings.get_as_obj())
    print('Connected', sid)

# Add client to a room
@sio.on('enter_room')
def enter_room(sid):
    # Join room
    is_new_room, room_id = rooms.assign_room(sid)

    # Connect sid to room so events emitted to clients in
    # the room are emitted to the socket with sid
    sio.enter_room(sid, room_id)

    # Wanna create a new room if there is a new one!
    if is_new_room:
        print("Starting match with room", room_id)
        sio.start_background_task(new_game, room_id)

def exit_match(sid):
    player = rooms.get_player(sid)
    if player != None:
        player['alive'] = False

    print(sid, "Leaving room")
    room_id = rooms.sid_to_room_id(sid)
    sio.leave_room(sid, room_id)

@sio.on('leave_room')
async def leave_room(sid, data):
    exit_match(sid)

@sio.on('disconnect')
async def disconnect(sid):
    exit_match(sid)

@sio.on('keydown')
async def keydown(sid, key):
    room_id = rooms.sid_to_room_id(sid)
    player = rooms.get_player(sid)

    if player: players.change_dir(player, key)

async def search_for_players(room_id):
    # Life cycle hook for the client
    await sio.emit('searching_for_players') 
    room = rooms.get_room(room_id)

    # Wait forever until we have enough players to start
    while len(room) > 0:
        await asyncio.sleep(settings.polling_rate)

        if len(room) >= settings.min_players:
            for i in range(settings.time_to_start_game):
                await sio.emit('game_starts_in', settings.time_to_start_game - i)
                await asyncio.sleep(1)

                # we don't have enough players go back to searching
                if len(room) < settings.min_players: break

            # The game is ready to start
            if i == settings.time_to_start_game - 1: break

async def play(room_id):
    # Life cycle hook for the client
    rooms.spawn_players(room_id)
    room = rooms.get_room(room_id)
    await sio.emit('start_game', rooms.room_to_list(room_id), room=room_id)

    while True:
        players_in_room = rooms.room_to_list(room_id)

        # Collision detection is built into move
        # We need to check for collision before we mark locations on the grid
        alive_func = lambda pl: pl['alive']

        # for ties.
        prev_alive_players = list(filter(alive_func, players_in_room))

        for player in players_in_room:
            if players.should_update(player): players.move(room_id, player)

        for player in players_in_room:
            if players.should_update(player): grid.mark_loc(room_id, player['x'], player['y'])

        await asyncio.sleep(settings.snake_speed)
        await sio.emit('update_players', players_in_room, room=room_id)

        alive_players = list(filter(alive_func, players_in_room))

        if len(alive_players) == 1:
            # Some dude won.
            return [alive_players[0]]
        elif len(alive_players) == 0:
            # It was a tie.
            return prev_alive_players

# Creates a game for a given room
async def new_game(room_id):
    await search_for_players(room_id)
    winners = await play(room_id)

    # Life cycle hook for client
    await sio.emit('game_over', winners, room=room_id)

    print("All players left room %s." % room_id)
    rooms.destroy_room(room_id)

if __name__ == '__main__':
    app = web.Application()
    sio.attach(app)
    web.run_app(app, port=8888)
