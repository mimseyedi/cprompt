"""
 ██████╗██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ████████╗
██╔════╝██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝
██║     ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝   ██║
██║     ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██╔═══╝    ██║
╚██████╗██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║        ██║
 ╚═════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝

cprompt Github repository: https://github.com/mimseyedi/cprompt
"""


import sys
import tty
import termios


KEYS: dict = {
    'up'         : 'A',
    'down'       : 'B',
    'right'      : 'C',
    'left'       : 'D',
    'shift-right': '1;2C',
    'shift-left' : '1;2D',

    'escape'     : '\x1b',
    'backspace'  : '\x7f',
    'enter'      : '\r',
    'tab'        : '\t',
    'space'      : ' ',
    'insert'     : '2~',
    'delete'     : '3~',

    'home'       : 'H',
    'end'        : 'F',
    'page_up'    : '5',
    'page_down'  : '6',

    'ctrl-a'     : '\x01',
    'ctrl-b'     : '\x02',
    'ctrl-c'     : '\x03',
    'ctrl-d'     : '\x04',
    'ctrl-e'     : '\x05',
    'ctrl-f'     : '\x06',
    'ctrl-g'     : '\x07',
    'ctrl-h'     : '\x08',
    'ctrl-j'     : '\x0a',
    'ctrl-k'     : '\x0b',
    'ctrl-l'     : '\x0c',
    'ctrl-n'     : '\x0e',
    'ctrl-o'     : '\x0f',
    'ctrl-p'     : '\x10',
    'ctrl-q'     : '\x11',
    'ctrl-r'     : '\x12',
    'ctrl-s'     : '\x13',
    'ctrl-t'     : '\x14',
    'ctrl-u'     : '\x15',
    'ctrl-v'     : '\x16',
    'ctrl-w'     : '\x17',
    'ctrl-x'     : '\x18',
    'ctrl-y'     : '\x19',
    'ctrl-z'     : '\x1a',
    'ctrl-\\'    : '\x1c',
    'ctrl-]'     : '\x1d',
}


def getchar() -> str:
    """
    The task of this function is to read a character from the input entered in the terminal.
    This function will return the character read from the terminal in the form of a string of length one.

    :return: str
    """

    fd: int = sys.stdin.fileno()
    attr: list = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, attr)