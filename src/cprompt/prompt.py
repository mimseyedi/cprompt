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
        keys: dict=None,
        conditions: tuple=None,
    ):
        self.message = message

        self.__text: str = ""
        self.__cursor: int = 0
        self.__formatted: dict = {}
        self.__last_key: str = ""

        self.keys = {} if keys is None else keys
        self.conditions = tuple() if conditions is None else conditions

    def write(self, char: str) -> None:
        if isinstance(char, str):
            if self.__text:
                termcol, _ = os.get_terminal_size()
                if len(self.__text) + len(self.message) < termcol:
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
            self.message + ''.join(output) + move_cursor_to_column(col=self.__cursor)
        )
        sys.stdout.flush()

    def prompt(self) -> str:
        pass

    def __ge__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __len__(self):
        pass

    def __bool__(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass