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
"""


import os
import sys

from ansi import (
    NEW_LINE,
    TERMINAL_BELL,
    ERASE_ENTIRE_LINE,
    move_cursor_to_column,
    get_cursor_position as gcp,
)
from keys import KEYS, readkey


class Cprompt:
    """

    """

    def __init__(
        self,
        message: str="",
        *,
        conditions: tuple=None,
    ):
        self.message = message

        self.__text: str = ""
        self.__cursor: int = 0
        self.__formatted: dict = {}
        self.__last_key: str = ""

        self.conditions = tuple() if conditions is None else conditions

    def write(self, char: str) -> None:
        if isinstance(char, str):
            if self.__text:
                termcol, _ = os.get_terminal_size()
                if len(self.__text) + len(self.message) + 1 < termcol:
                    self.__text = self.__text[0:self.__cursor] + char + self.__text[self.__cursor:]
                    self.__cursor += 1
            else:
                self.__text += char
                self.__cursor += 1
        else:
            raise TypeError

    def insert_text(self, text: str) -> None:
        if isinstance(text, str):
            for char in text:
                self.write(char)
        else:
            raise TypeError

    def remove(self) -> None:
        if self.__cursor > 0:
            self.__cursor -= 1
            self.__text = self.__text[:self.__cursor] + self.__text[self.__cursor+1:]
        else:
            sys.stdout.write(TERMINAL_BELL)

    def move_cursor_right(self) -> None:
        if self.__cursor < len(self.__text):
            self.__cursor += 1
        else:
            sys.stdout.write(TERMINAL_BELL)

    def move_cursor_left(self) -> None:
        if self.__cursor > 0:
            self.__cursor -= 1
        else:
            sys.stdout.write(TERMINAL_BELL)

    def get_word_before_cursor(self) -> str:
        pass

    def get_word_after_cursor(self) -> str:
        pass

    def get_text_before_cursor(self) -> str:
        pass

    def get_text_after_cursor(self) -> str:
        pass

    def del_word_before_cursor(self) -> None:
        pass

    def del_word_after_cursor(self) -> None:
        pass

    def del_text_before_cursor(self) -> None:
        pass

    def del_text_after_cursor(self) -> None:
        pass

    @staticmethod
    def get_cursor_position() -> tuple[int, int]:
        return gcp()

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text_: str) -> None:
        if isinstance(text_, str):
            self.__text = text_
            self.__cursor = len(self.__text)
        else:
            raise TypeError

    @property
    def cursor(self) -> int:
        return self.__cursor

    @cursor.setter
    def cursor(self, cursor_: int) -> None:
        if isinstance(cursor_, int):
            self.__cursor = cursor_
        else:
            raise TypeError

    @property
    def formatted(self) -> dict:
        return self.__formatted.copy()

    @formatted.setter
    def formatted(self, formatted_: dict) -> None:
        if isinstance(formatted_, dict):
            for key, value in formatted_.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise Exception

            self.__formatted = formatted_.copy()
        else:
            raise TypeError

    @property
    def last_key(self) -> str:
        return self.__last_key

    def clear(self) -> None:
        self.__text = ""

    def display(self) -> None:
        temp: str = self.__text.replace(" ", " - ")

        output: list = []
        for word in temp.split():
            if word in self.__formatted.keys():
                output.append(self.__formatted[word])
            else:
                if word == '-':
                    output.append(" ")
                else:
                    output.append(word)

        sys.stdout.write(ERASE_ENTIRE_LINE)
        sys.stdout.write(move_cursor_to_column(col=0))

        sys.stdout.write(
            self.message + ''.join(output) + move_cursor_to_column(col=self.__cursor+len(self.message)+1)
        )
        sys.stdout.flush()

    def prompt(self) -> str:
        sys.stdout.write(self.message)
        sys.stdout.flush()

        while True:
            key: str = readkey()
            self.__last_key: str = key
            exit_status: bool = False

            if self.conditions:
                for func in self.conditions:
                    try:
                        func(self)
                        continue
                    except SystemExit:
                        exit_status = True
                    except TypeError:
                        raise Exception

            match key:
                case 'ENTER':
                    self.display()
                    sys.stdout.write(NEW_LINE)
                    break

                case 'BACKSPACE':
                    self.remove()

                case 'RIGHT':
                    self.move_cursor_right()

                case 'LEFT':
                    self.move_cursor_left()

                case 'SPACE':
                    self.write(" ")

                case _:
                    special_keys: tuple = (
                        'UP',
                        'DOWN',
                        'SHIFT+RIGHT',
                        'SHIFT+LEFT',
                        'ESCAPE',
                        'TAB',
                        'INSERT',
                        'DELETE',
                        'PAGE_UP',
                        'PAGE_DOWN',
                        'HOME',
                        'END',
                    )
                    if key is not None:
                        if not key.startswith('CTRL') and key not in special_keys:
                            self.write(key)

            self.display()

            if exit_status:
                sys.stdout.write(NEW_LINE)
                sys.stdout.flush()
                break

        return self.__text

    def __ge__(self, other):
        if isinstance(other, Cprompt):
            return len(self.__text) >= len(other.__text)

        elif isinstance(other, str):
            return len(self.__text) >= len(other)

        raise TypeError

    def __gt__(self, other):
        if isinstance(other, Cprompt):
            return len(self.__text) > len(other.__text)

        elif isinstance(other, str):
            return len(self.__text) > len(other)

        raise TypeError

    def __eq__(self, other):
        if isinstance(other, Cprompt):
            return len(self.__text) == len(other.__text)

        elif isinstance(other, str):
            return len(self.__text) == len(other)

        elif isinstance(other, bool):
            return True if self.__text else False

        raise TypeError

    def __len__(self):
        return len(self.__text)

    def __bool__(self):
        return True if len(self.__text) > 0 else False

    def __str__(self):
        return self.__text.__str__()

    def __repr__(self):
        return (
            'Cprompt('
            f'message={self.message}, '
            f'conditions={self.conditions}, '
            f'text={self.__text}, '
            f'cursor={self.__cursor}, '
            f'formatted={self.__formatted})'
        )