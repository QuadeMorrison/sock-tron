__all__ = ['create_object']

def create_object(height = 0, width = 0):
    return { height: height, width: width }

player = create_object()
window = create_object()

def get_start_position():
    def calc_position(dimension):
        return window[dimension] / 2 - player[dimension] / 2

    return { 'x': calc_position("width"), 'y': calc_position("height") }
