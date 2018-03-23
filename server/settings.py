# Measured in blocks
window = { 'height': 50, 'width': 50 }
window_padding = 1

# How big the client should render the blocks
# should measure in viewports maybe???
block_scale = 10

# Measured in snakes
max_players = 2

# Start the countdown once we atleast have
# this many players
min_players = 2

# How often we should check that another player has joined the room
polling_rate = 1

# How often each snake moves. The lower the number the faster
# ie 0.1 would be 10 times a second
snake_speed = 0.1

# Measured in seconds
time_to_start_game = 3

# 17 colors for now. These are all very basic colors.
player_colors = [
    "#FF0000",
    "#00FFFF",
    "#C0C0C0",
    "#0000FF",
    "#808080",
    "#0000A0",
    "#000000",
    "#ADD8E6",
    "#FFA500",
    "#800080",
    "#A52A2A",
    "#FFFF00",
    "#800000",
    "#00FF00",
    "#008000",
    "#FF00FF",
    "#808000"
]

# Settings to be deliver to the client in a form
# thats easily translatable to javascript
def get_as_obj():
    global window
    return {
        'window': window,
        'block_scale': block_scale
    }
