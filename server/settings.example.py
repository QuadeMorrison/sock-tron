# A buffer for how far away from the edge should players spawn.
spawn_padding = 4

# How big the client should render the blocks.
# should measure in viewports maybe???
grid = 10

# The port!
port = 8888

# Scales the grid_w and grid_h. How many blocks per player.
blocks_per_player = 12

# We don't want to scale too small, put a limit.
# Measured in blocks.
min_dimension = 50

# Measured in snakes.
max_players = 10

# Start the countdown once we atleast have.
# this many players.
min_players = 2

# The Area Constant!!!!
area_constant = 20

# How often we should check that another player has joined the room.
polling_rate = 1

# How often each snake moves. The lower the number the faster.
# ie 0.1 would be 10 times a second.
snake_speed = 0.1

# Measured in seconds.
time_to_start_game = 3

# How many seconds to add if a new player joins the game before it starts.
# Measured in seconds.
time_padding = 3

# 17 colors for now. These are all very basic colors.
player_colors = [
    "#FF0000",
    "#00FFFF",
    "Green",
    "Yellow",
    "Purple",
    "#3C78D8",
    "Mint",
    "Orange",
    "Magenta",
    "Teal",
    "#A52A2A",
    "#FFFF00",
    "#800000",
    "#00FF00",
    "#008000",
    "#FF00FF",
    "#808000"
]
