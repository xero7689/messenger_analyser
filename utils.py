import random

class GruvBox:
    bg = "#282828"
    fg = "#ebdbb2"
    red = "#cc241d"
    yellow = "#98971a"
    green = "#d79921"
    blue = "#458588"
    purple = "#b16286"
    orange = "#d65d0e"
    aqua = "#689d6a"
    gray = "#a89984"

class ColorScheme:
    gruvbox = GruvBox

def convert_fb_str(s):
    return s.encode('latin1').decode('utf8')

def random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

