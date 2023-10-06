"""
 ██████╗██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ████████╗
██╔════╝██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝
██║     ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝   ██║
██║     ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██╔═══╝    ██║
╚██████╗██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║        ██║
 ╚═════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝

cprompt Github repository: https://github.com/mimseyedi/cprompt

resource: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
"""


import re


# Base ANSI
ESC = '\033'
CSI = '['

# General ASCII codes
TERMINAL_BELL = '\x07'
BACKSPACE = '\x08'
HORIZONTAL_TAB = '\x09'
NEW_LINE = '\x0a'
VERTICAL_TAB = '\x0b'
NEW_PAGE = '\x0c'
CARRIAGE_RETURN = '\x0d'

# Cursor control
HOME_POSITION_0_0 = '\033[H'
MOVE_CURSOR_UP = '\033[A'
MOVE_CURSOR_DOWN = '\033[B'
MOVE_CURSOR_RIGHT = '\033[C'
MOVE_CURSOR_LEFT = '\033[D'
MOVE_CURSOR_TO_NEXT_LINE = '\033[E'
MOVE_CURSOR_TO_PREVIOUS_LINE = '\033[F'
REQUEST_CURSOR_POSITION = '\033[6n'
SAVE_CURSOR_POSITION = '\033[s'
RESTORE_CURSOR = '\033[u'

# Erase functions
ERASE_FROM_CURSOR_TO_END_OF_SCREEN = '\033[0J'
ERASE_FROM_CURSOR_TO_BEGINNING_OF_SCREEN = '\033[1J'
ERASE_ENTIRE_SCREEN = '\033[2J'
ERASE_SAVED_LINES = '\033[3J'
ERASE_FROM_CURSOR_TO_END_OF_LINE = '\033[0K'
ERASE_START_OF_LINE_TO_CURSOR = '\033[1K'
ERASE_ENTIRE_LINE = '\033[2K'

# Graphics mode
RESET = '\033[0m'
BOLD = '\033[1m'
FAINT = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
INVERSE_REVERSE = '\033[7m'
HIDDEN_VISIBLE = '\033[8m'

# Colors mode
FG_BLACK = '\033[30m'
FG_RED = '\033[31m'
FG_GREEN = '\033[32m'
FG_YELLOW = '\033[33m'
FG_BLUE = '\033[34m'
FG_MAGENTA = '\033[35m'
FG_CYAN = '\033[36m'
FG_WHITE = '\033[37m'
FG_DEFAULT = '\033[39m'

BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'
BG_WHITE = '\033[47m'
BG_DEFAULT = '\033[49m'

FG_BRIGHT_BLACK = '\033[90m'
FG_BRIGHT_RED = '\033[91m'
FG_BRIGHT_GREEN = '\033[92m'
FG_BRIGHT_YELLOW = '\033[93m'
FG_BRIGHT_BLUE = '\033[94m'
FG_BRIGHT_MAGENTA = '\033[95m'
FG_BRIGHT_CYAN = '\033[96m'
FG_BRIGHT_WHITE = '\033[97m'

BG_BRIGHT_BLACK = '\033[100m'
BG_BRIGHT_RED = '\033[101m'
BG_BRIGHT_GREEN = '\033[102m'
BG_BRIGHT_YELLOW = '\033[103m'
BG_BRIGHT_BLUE = '\033[104m'
BG_BRIGHT_MAGENTA = '\033[105m'
BG_BRIGHT_CYAN = '\033[106m'
BG_BRIGHT_WHITE = '\033[107m'

# Private modes
CURSOR_VISIBLE = '\033[?25h'
CURSOR_INVISIBLE = '\033[?25l'
SAVE_SCREEN = '\033[?47h'
RESTORE_SCREEN = '\033[?47l'
ENABLE_ALTERNATIVE_BUFFER = '\033[?1049h'
DISABLE_ALTERNATIVE_BUFFER = '\033[?1049l'

# Regex pattern
ANSI_PATTERN = r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'


def remove_ansi_from_string(string: str) -> str:
    """
    The task of this function is to remove ANSI codes from inside a string.
    This function will return the cleared string.

    :param string: A string containing ANSI codes.
    :return: str
    """

    return re.compile(ANSI_PATTERN).sub('', string)


def extract_ansi_from_string(string: str) -> list[str]:
    """
    The task of this function is to extract ANSI codes from inside a string.
    This function will return the ANSI escape codes in a list format.

    :param string: A string containing ANSI codes.
    :return: list[str]
    """

    return re.compile(ANSI_PATTERN).findall(string)


def extract_non_ansi(string: str) -> tuple[bool, str]:
    """
    The task of this function is to check a string and extract non-ANSI characters.
    If there are no ANSI codes in the string, this function will return a tuple with the value False and the string
    itself, and if there are ANSI codes in the string, it will return a tuple with the value True and the cleaned string.

    :param string: A string containing ANSI codes.
    :return: tuple[bool, str]
    """

    compiled_pattern = re.compile(ANSI_PATTERN)

    if compiled_pattern.findall(string):
        return True, compiled_pattern.sub('', string)

    return False, string


def get_graphics_cell(*args) -> str:
    """
    The task of this function is to return an ANSI graphics cell
    according to the graphic arguments, in the form of a string.
    For more information: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#colors--graphics-mode

    :param args: ANSI graphic codes
    :return: str
    """

    return ESC + CSI + ';'.join(map(lambda x: x.__str__(), args)) + 'm'
