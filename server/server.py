#!/usr/bin/env python3
from aiohttp import web
import socketio
import asyncio
import settingtools
import settings
import players
import grid
import rooms
import sys


# Taken from:
# https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


sio = socketio.AsyncServer()


@sio.on('connect')
async def connect(sid, environ):
    # What does await emit do, does it wait for a verification to come from the
    # client? If not, then that await is pointless, right?
    await sio.emit('init_settings', settingtools.get_as_obj(), room=sid)
    print('Connected', sid)


# Add client to a room
@sio.on('enter_room')
async def enter_room(sid):
    # Join room
    is_new_room, room_id, player_num = rooms.assign_room(sid)

    # Connect sid to room so events emitted to clients in
    # the room are emitted to the socket with sid
    sio.enter_room(sid, room_id)

    # Let the client know which player they are

    # Wanna create a new room if there is a new one!
    if is_new_room:
        print("Starting match with room", room_id)
        sio.start_background_task(new_game, room_id)


def exit_match(sid):
    player = rooms.get_player(sid)
    if player is not None:
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
    player = rooms.get_player(sid)

    if player:
        players.change_dir(player, key)

async def search_for_players(room_id):
    # Life cycle hook for the client
    await sio.emit('searching_for_players')

    prev_num_players = -1
    # Wait forever until we have enough players to start
    while True:
        rooms.remove_dead_players(room_id)

        await asyncio.sleep(settings.polling_rate)
        num_players = len(rooms.room_to_list(room_id))
        prev_num_players = -1

        if num_players >= settings.min_players:
            i = 0
            while i < settings.time_to_start_game:
                rooms.remove_dead_players(room_id)
                rooms.spawn_players(room_id)
                room = rooms.get_room(room_id)

                for sid, player in room.items():
                    await sio.emit('player_num', player['num'], room=sid)

                players = rooms.room_to_list(room_id)
                settings_obj = settingtools.get_as_obj(num_players)
                count_down = settings.time_to_start_game - i

                payload = {
                    'count_down': count_down,
                    'players': players,
                    'settings': settings_obj
                }

                await sio.emit('game_starts_in', payload, room=room_id)
                await asyncio.sleep(1)
                i += 1

                # we don't have enough players go back to searching
                num_players_alive = len(rooms.get_alive_players(room_id))
                if num_players_alive < settings.min_players:
                    print("Restart!")
                    await sio.emit('restart_search', room=room_id)
                    prev_num_players = 0
                    break

                # Have to check how many players there are every
                # iteration of the loop
                num_players = len(rooms.get_alive_players(room_id))

                if num_players > prev_num_players and prev_num_players > -1:
                    i = i - settings.time_padding

                prev_num_players = num_players

            # The game is ready to start
            if i == settings.time_to_start_game:
                rooms.mark_room_as_started(room_id)
                break

async def play(room_id):
    # Life cycle hook for the client
    rooms.spawn_players(room_id, with_collision=True)
    
    await sio.emit('start_game', rooms.room_to_list(room_id), room=room_id)


    while True:
        players_in_room = rooms.room_to_list(room_id)

        # Collision detection is built into move
        # We need to check for collision before we mark locations on the grid
        def alive_func(pl): return pl['alive']

        # for ties.
        prev_alive_players = list(filter(alive_func, players_in_room))

        for player in players_in_room:
            if players.should_update(player):
                players.move(room_id, player)

        for player in players_in_room:
            if players.should_update(player):
                grid.mark_loc(room_id, player['x'], player['y'])

        # after the players have moved, fix up the dir list.
        for player in players_in_room:
            players.trim_dir_list(player)

        await asyncio.sleep(settings.snake_speed)
        await sio.emit('update_players', players_in_room, room=room_id)

        alive_players = list(filter(lambda pl: pl['alive'], players_in_room))

        if len(alive_players) == 1:
            # Some dude (the greatest of dudes) won.
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
