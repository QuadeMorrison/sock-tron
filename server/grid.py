grid = {}

def mark_loc(room_id, x, y):
    if room_id not in grid:
        grid[room_id] = {}

    if not x in grid[room_id]:
        grid[room_id][x] = {}

    grid[room_id][x][y] = True

def is_marked(room_id, x, y):
    if (not room_id in grid or
        not x in grid[room_id] or
        not y in grid[room_id][x]):
        return False

    return grid[room_id][x][y]
