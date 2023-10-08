"""
 ██████╗██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ████████╗
██╔════╝██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝
██║     ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝   ██║
██║     ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██╔═══╝    ██║
╚██████╗██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║        ██║
 ╚═════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝

cprompt is a package for creating live and customized one-line prompts that can
be used to manage and personalize input from the user in the terminal (bash) environment.

cprompt Github repository: https://github.com/mimseyedi/cprompt

This file is related to keyboard keys and their special codes in low level style.
In this file, there are specified keys in the KEYS constant, which can be read from
the keyboard to the terminal with the help of two functions, readkey and getchar.

For more information:
https://stackoverflow.com/questions/64035952/how-to-key-press-detection-on-a-linux-terminal-low-level-style-in-python
"""


import sys
import tty
import termios
from ansi import ESC, CSI


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


def readkey() -> str:
    """
    The task of this function is to read the key pressed by the user with the help of the getchar function.
    This function connects the entered input to the corresponding keys and finally returns the name of the entered key.

    :return: str
    """

    char: str = getchar()

    if char == ESC:
        if getchar() == CSI:
            _ = getchar()
            if _ == '1':
                if getchar() == ';':
                    if getchar() == '2':
                        _ = getchar()
                        match _:
                            case 'C':
                                return 'SHIFT+RIGHT'
                            case 'D':
                                return 'SHIFT+LEFT'
            elif _ == '2':
                if getchar() == '~':
                    return 'INSERT'
            elif _ == '3':
                if getchar() == '~':
                    return 'DELETE'
            elif _ == '5':
                return 'PAGE_UP'
            elif _ == '6':
                return 'PAGE_DOWN'

            elif _ == 'H':
                return 'HOME'
            elif _ == 'F':
                return 'END'
            elif _ == 'A':
                return 'UP'
            elif _ == 'B':
                return 'DOWN'
            elif _ == 'C':
                return 'RIGHT'
            elif _ == 'D':
                return 'LEFT'
    else:
        if char == KEYS.get('escape'):
            return 'ESCAPE'
        elif char == KEYS.get('backspace'):
            return 'BACKSPACE'
        elif char == KEYS.get('enter'):
            return 'ENTER'
        elif char == KEYS.get('tab'):
            return 'TAB'
        else:
            for key, value in KEYS.items():
                if char == value and char not in (
                    'A',
                    'B',
                    'C',
                    'D',
                    'H',
                    'F',
                ):
                    return key.upper()

        return char