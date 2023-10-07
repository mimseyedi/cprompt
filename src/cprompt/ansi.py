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

This file is related to ANSI escape codes. There are ANSI escape code constants in this file
that can be used more easily and with a more regular appearance.
There are also functions to get more complex ANSI escape codes along with special
combinations that can be useful for communicating with the bash terminal.

ANSI escape sequences are a standard for in-band signaling to control cursor location, color,
font styling, and other options on video text terminals and terminal emulators.
Certain sequences of bytes, most starting with an ASCII escape character and a bracket character, are embedded into text.
The terminal interprets these sequences as commands, rather than text to display verbatim.

For more information: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
"""


import re
import sys
import termios
from errors import ReadCursorPositionError


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

    if not isinstance(string, str):
        raise TypeError(f'The string argument must be of the string type, but received: "{type(string)}".')

    return re.compile(ANSI_PATTERN).sub('', string)


def extract_ansi_from_string(string: str) -> list[str]:
    """
    The task of this function is to extract ANSI codes from inside a string.
    This function will return the ANSI escape codes in a list format.

    :param string: A string containing ANSI codes.
    :return: list[str]
    """

    if not isinstance(string, str):
        raise TypeError(f'The string argument must be of the string type, but received: "{type(string)}".')

    return re.compile(ANSI_PATTERN).findall(string)


def extract_non_ansi(string: str) -> tuple[bool, str]:
    """
    The task of this function is to check a string and extract non-ANSI characters.
    If there are no ANSI codes in the string, this function will return a tuple with the value False and the string
    itself, and if there are ANSI codes in the string, it will return a tuple with the value True and the cleaned string.

    :param string: A string containing ANSI codes.
    :return: tuple[bool, str]
    """

    if not isinstance(string, str):
        raise TypeError(f'The string argument must be of the string type, but received: "{type(string)}".')

    compiled_pattern = re.compile(ANSI_PATTERN)

    if compiled_pattern.findall(string):
        return True, compiled_pattern.sub('', string)

    return False, string


def get_graphic_cell(*args) -> str:
    """
    The task of this function is to return an ANSI graphics cell
    according to the graphic arguments, in the form of a string.
    For more information: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#colors--graphics-mode

    :param args: ANSI graphic codes
    :return: str
    """

    try:
        graphic_codes: list = list(map(int, args))
    except ValueError:
        raise TypeError('All graphic codes must be int type or have the ability to convert to int.')

    return ESC + CSI + ';'.join(map(lambda x: x.__str__(), graphic_codes)) + 'm'


def get_256_color_cell(color_code: int, color_type: str) -> str:
    """
    The task of this function is to return a color graphic cell
    based on color codes between 0 and 255.
    For more information: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#256-colors

    :param color_code: A color code between 0 and 255.
    :param color_type: A color type between 'bg' for background or 'fg' for foreground.
    :return: str
    """

    if not isinstance(color_code, int):
        raise TypeError(f'The type of the color_code argument must be a int, but received "{type(color_code)}".')

    if not 0 <= color_code <= 255:
        raise ValueError(f'The color code must be between 0 and 255. Received code: {color_code}')

    if not isinstance(color_type, str):
        raise TypeError(f'The type of the color_type argument must be a string, but received "{type(color_type)}".')

    if color_type not in ('bg', 'fg',):
        raise ValueError(f'The value of the color_type argument must be between "bg" and "fg", but received: "{color_type}".')

    if color_type == 'bg':
        return ESC + CSI + '48;5;' + color_code.__str__() + 'm'

    return ESC + CSI + '38;5;' + color_code.__str__() + 'm'


def get_rgb_color_cell(r: int, g: int, b: int, color_type: str) -> str:
    """
    The task of this function is to return a color graphic cell based on 'rgb' codes.
    For more information: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#rgb-colors

    :param r: Red color code based on rgb.
    :param g: Green color code based on rgb.
    :param b: Blue color code base on rgb.
    :param color_type: A color type between 'bg' for background or 'fg' for foreground.
    :return: str
    """

    if not isinstance(r, int):
        raise TypeError(f'The type of the "r" argument must be an integer, but received "{type(r)}"')

    if not isinstance(g, int):
        raise TypeError(f'The type of the "g" argument must be an integer, but received "{type(g)}"')

    if not isinstance(b, int):
        raise TypeError(f'The type of the "b" argument must be an integer, but received "{type(b)}"')

    if not isinstance(color_type, str):
        raise TypeError(f'The type of the color_type argument must be a string, but received "{type(color_type)}".')

    if color_type not in ('bg', 'fg',):
        raise ValueError(f'The value of the color_type argument must be between "bg" and "fg", but received: "{color_type}".')

    if color_type == 'bg':
        return ESC + CSI + '48;2;' + ';'.join(map(lambda x: x.__str__, [r, g, b])) + 'm'

    return ESC + CSI + '38;2;' + ';'.join(map(lambda x: x.__str__, [r, g, b])) + 'm'


def move_cursor(row: int, col: int) -> str:
    """
    The task of this function is to move the cursor to the desired coordinates.
    This function will return a string containing the ANSI code of the new cursor position.

    :param row: The desired line to move the cursor to the point.
    :param col: The desired column to move the cursor to the point.
    :return: str
    """

    if not isinstance(row, int):
        raise TypeError(f'The type of the "row" argument must be an integer, but received "{type(row)}"')

    if not isinstance(col, int):
        raise TypeError(f'The type of the "col" argument must be an integer, but received "{type(col)}"')

    return ESC + CSI + row.__str__() + ';' + col.__str__() + 'H'


def move_cursor_to_column(col: int) -> str:
    """
    The task of this function is to move the cursor to the desired column.
    This function will return a string containing the ANSI code to move the cursor to the specified column.

    :param col: The desired column to move the cursor to the point.
    :return: str
    """

    if not isinstance(col, int):
        raise TypeError(f'The type of the "col" argument must be an integer, but received "{type(col)}"')

    return ESC + CSI + col.__str__() + 'G'


def move_cursor_up(lines: int) -> str:
    """
    The task of this function is to move up the cursor to the number of lines it receives from the lines argument.
    The output of this function is a string containing the ANSI code for moving up the cursor.

    :param lines: The number of lines where the cursor is supposed to go up.
    :return: str
    """

    if not isinstance(lines, int):
        raise TypeError(f'The type of the "lines" argument must be an integer, but received "{type(lines)}"')

    return ESC + CSI + lines.__str__() + 'A'


def move_cursor_down(lines: int) -> str:
    """
    The task of this function is to move down the cursor by the number of lines it receives from the lines argument.
    The output of this function is a string containing the ANSI code for moving down the cursor.

    :param lines: The number of lines where the cursor is supposed to go down.
    :return: str
    """

    if not isinstance(lines, int):
        raise TypeError(f'The type of the "lines" argument must be an integer, but received "{type(lines)}"')

    return ESC + CSI + lines.__str__() + 'B'


def move_cursor_right(columns: int) -> str:
    """
    The task of this function is to move right the cursor by the number of columns it receives from the columns argument.
    The output of this function is a string containing the ANSI code for moving right the cursor.

    :param columns: The number of columns where the cursor is supposed to go right.
    :return: str
    """

    if not isinstance(columns, int):
        raise TypeError(f'The type of the "columns" argument must be an integer, but received "{type(columns)}"')

    return ESC + CSI + columns.__str__() + 'C'


def move_cursor_left(columns: int) -> str:
    """
    The task of this function is to move left the cursor by the number of columns it receives from the columns argument.
    The output of this function is a string containing the ANSI code for moving left the cursor.

    :param columns: The number of columns where the cursor is supposed to go left.
    :return: str
    """

    if not isinstance(columns, int):
        raise TypeError(f'The type of the "columns" argument must be an integer, but received "{type(columns)}"')

    return ESC + CSI + columns.__str__() + 'D'


def move_cursor_to_next_line(lines_down: int) -> str:
    """
    The task of this function is to move the cursor to the next lines.
    The number of this shift is determined by the lines_down argument.

    :param lines_down: The number of lines where the cursor is supposed to move down.
    :return: str
    """

    if not isinstance(lines_down, int):
        raise TypeError(f'The type of the "lines_down" argument must be an integer, but received "{type(lines_down)}"')

    return ESC + CSI + lines_down.__str__() + 'E'


def move_cursor_to_previous_line(lines_up: int) -> str:
    """
    The task of this function is to move the cursor to the previous lines.
    The number of this shift is determined by the lines_up argument.

    :param lines_up: The number of lines where the cursor is supposed to move up.
    :return: str
    """

    if not isinstance(lines_up, int):
        raise TypeError(f'The type of the "lines_up" argument must be an integer, but received "{type(lines_up)}"')

    return ESC + CSI + lines_up.__str__() + 'F'


def get_cursor_position() -> tuple[int, int]:
    """
    The task of this function is to request the cursor position from the terminal
    by special ANSI escape code and read the position.
    The value that this function returns is a tuple consisting of row and column positions as an integer.

    :return: tuple[int, int]
    """

    old_stdin_mode = termios.tcgetattr(sys.stdin)
    _ = termios.tcgetattr(sys.stdin)
    _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)

    try:
        _ = ""
        sys.stdout.write(REQUEST_CURSOR_POSITION)
        sys.stdout.flush()

        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            ...
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_stdin_mode)

    try:
        row, col = int(res.group("y")), int(res.group("x"))
    except ValueError:
        raise ReadCursorPositionError(
            (f'The cursor position cannot be read or converted. '
            'Obtained position: (row={res.group("y")}, col={res.group("x")})')
        )

    return row, col