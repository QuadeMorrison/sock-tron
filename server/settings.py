# A buffer for how far away from the edge should players spawn.
spawn_padding = 4

# How big the client should render the blocks
# should measure in viewports maybe???
grid = 10

# Scales the grid_w and grid_h. How many blocks per player
blocks_per_player = 12

# We don't want to scale too small, put a limit
# Measured in blocks
min_dimension = 50

# Measured in snakes
max_players = 8

# Start the countdown once we atleast have
# this many players
min_players = 2

# How often we should check that another player has joined the room
polling_rate = 1

# How often each snake moves. The lower the number the faster
# ie 0.1 would be 10 times a second
snake_speed = 0.1

# Measured in seconds
time_to_start_game = 15

# How many seconds to add if a new player joins the game before it starts
# Measured in seconds
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


# Calculate how many blocks for the grid dimensions
# so we can scale dynamically
def grid_dimensions(num_players):
    return max(blocks_per_player * num_players, min_dimension)


# Settings to be delivered to the client in a form
# thats easily translatable to javascript
def get_as_obj(num_players = min_players):
    global grid_w, grid_h, grid
    return {
        'grid_dim': grid_dimensions(num_players),
        'grid': grid
    }
