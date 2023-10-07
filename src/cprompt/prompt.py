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
        pass

    def insert_text(self, text: str) -> None:
        pass

    def remove(self) -> None:
        pass

    def move_cursor_right(self) -> None:
        pass

    def move_cursor_left(self) -> None:
        pass

    def get_cursor_position(self) -> tuple[int, int]:
        pass

    def set_cursor_position(self, col: int, row: int=None) -> None:
        pass

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

    def get_lastkey(self) -> str:
        pass

    def clear(self) -> None:
        pass

    def display(self) -> None:
        pass

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