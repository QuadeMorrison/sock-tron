import settings
import math

# Calculate how many blocks for the grid dimensions
# so we can scale dynamically
def grid_dimensions(num_players):
    blocks_per_player = settings.area_constant / math.sqrt(num_players)
    return max(blocks_per_player * num_players, settings.min_dimension)

# Settings to be delivered to the client in a form
# thats easily translatable to javascript
def get_as_obj(num_players = settings.min_players):
    return {
        'grid_dim': grid_dimensions(num_players),
        'grid': settings.grid
    }
