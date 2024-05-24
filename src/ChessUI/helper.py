def get_opposite_color(color):
    return 'black' if color == 'white' else 'white'


def highlight_color(color):
    r, g, b = color
    if r == 234:
        return 255, 255, 150 # yellowish green
    else:
        return 181, 201, 82 # green limeish
