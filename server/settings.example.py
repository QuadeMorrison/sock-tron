# A buffer for how far away from the edge should players spawn.
spawn_padding = 4

# How big the client should render the blocks
# should measure in viewports maybe???
grid = 10

# The port!
port = 8888

# Scales the grid_w and grid_h. How many blocks per player
blocks_per_player = 12

# We don't want to scale too small, put a limit
# Measured in blocks
min_dimension = 50

# Measured in snakes
max_players = 10

# Start the countdown once we atleast have
# this many players
min_players = 2

# The Area Constant!!!!
area_constant = 20

# How often we should check that another player has joined the room
polling_rate = 1

# How often each snake moves. The lower the number the faster
# ie 0.1 would be 10 times a second
snake_speed = 0.1

# Measured in seconds
time_to_start_game = 3

# How many seconds to add if a new player joins the game before it starts
# Measured in seconds
time_padding = 3

# 17 colors for now. These are all very basic colors.
player_colors = [
    "#FF0000",  # Red
    "#00FFFF",  # Blue
    "#66FF66",  # Green
    "#FFEB00",  # Yellow
    "#9C51B6",  # Purple
    "#FF6037",  # Orange
    "#FEFEFE",  # Basically white
    "#E12C2C",  # Red
    "#2243B6",  # Blue
    "#FF6EFF",  # Pink
    "#29AB87",  # Green
    "#FD0E35",  # Red
    "#C8C8CD",  # Grey
    "#FF681F",  # Orange
    "#33CC99",  # Green
]

