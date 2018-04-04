grid = {}

def mark_loc(room_id, x, y):
    if room_id not in grid:
        grid[room_id] = {}

    if not x in grid[room_id]:
        grid[room_id][x] = {}

    if y in grid[room_id][x]:
        grid[room_id][x][y] += 1
    else:
        grid[room_id][x][y] = 1

def mark_val(room_id, x, y):
    if (not room_id in grid or
        not x in grid[room_id] or
        not y in grid[room_id][x]):
        return 0

    return grid[room_id][x][y]
