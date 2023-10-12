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
from typing import Callable
from abc import ABC, abstractmethod

from ansi import (
    TERMINAL_BELL,
    extract_non_ansi,
    get_cursor_position as gcp,
)
from errors import (
    LimitError,
    FormattedTypeError,
    ConditionIsNotCallableError,
)


class BaseCprompt(ABC):
    """

    """

    def __init__(
        self,
        message: str="",
        *,
        limit: int=None,
        conditions: tuple=None,
    ):
        self._text: str = ""
        self._cursor: int = 0
        self._formatted: dict = {}
        self._last_key: str = ""
        self._ignored_keys: list = []
        self._returned_value: str|None = None

        if isinstance(message, str):
            self.message = message
        else:
            raise TypeError(
                ('The message attribute must be of string type, '
                 f'but received "{type(message)}".')
            )

        if conditions is None:
            self.conditions = tuple()
        else:
            if isinstance(conditions, tuple):
                for func in conditions:
                    if not isinstance(func, Callable):
                        raise ConditionIsNotCallableError(
                            f'All conditions must be callable, but received "{type(func)}".'
                        )

                self.conditions = conditions
            else:
                raise TypeError(
                    ('The conditions attribute must be of tuple[callable,...] type, '
                     f'but received "{type(conditions)}".')
                )

        termcol, _ = os.get_terminal_size()

        if limit is None:
            self.limit = termcol
        else:
            if isinstance(limit, int) and limit <= termcol:
                self.limit = limit
            else:
                raise LimitError(
                    ('The limit attribute must be of int type and '
                     'within the width of the terminal screen. '
                     f'limit={limit}, terminal width={termcol}')
                )

    def _write(self, char: str) -> None:
        """
        The task of this method is to write a character in the user's input string.
        This method is also responsible for removing ANSI escape codes from
        the user's input string and controlling the write limit.

        :param char: A string containing a single character.
        :return: None
        """

        if isinstance(char, str):
            if len(char) == 1:
                if self._text:
                    if len(self._text) + len(self.message) + 1 < self.limit:
                        self._text = self._text[0:self._cursor] + char + self._text[self._cursor:]
                        self._cursor += 1
                    else:
                        sys.stdout.write(TERMINAL_BELL)
                else:
                    self._text += char
                    self._cursor += 1
            else:
                raise ValueError(
                    f'The length of the char argument should be 1, but received {len(char)}.'
                )
        else:
            raise TypeError(
                f'The type of char argument must be string, but received "{type(char)}".'
            )

    def insert_text(self, text: str) -> None:
        """
        The task of this method is to insert a text in the user's input string.
        This method is also responsible for removing ANSI escape codes from
        the user's input string and controlling the text limit.

        :param text: A string containing multiple characters.
        :return: None
        """

        if isinstance(text, str):
            if len(text) <= self.limit:
                status, string_ = extract_non_ansi(text)

                if status:
                    for char in string_:
                        self._write(char)

                    self._formatted[string_] = text
                else:
                    for char in text:
                        self._write(char)
            else:
                raise LimitError(
                    ('The text length is greater than limit. '
                     f'text length={len(text)}, limit={self.limit}')
                )
        else:
            raise TypeError(
                f'The type of text argument must be string, but received "{type(text)}".'
            )

    def remove(self) -> None:
        """
        The task of this method is to delete a character from the location of the cursor.
        This function pushes the cursor back and deletes one character from the written input.

        :return: None
        """

        if self._cursor > 0:
            self._cursor -= 1
            self._text = self._text[:self._cursor] + self._text[self._cursor + 1:]
        else:
            sys.stdout.write(TERMINAL_BELL)

    def move_cursor_right(self) -> None:
        """
        The task of this method is to move the cursor one unit to the 'right'.
        (Here unit means one column in the terminal which is equivalent to one character)

        With the help of this method and relating it to a key, you can easily move
        to the 'right' among the user's input strings.

        :return: None
        """

        if self._cursor < len(self._text):
            self._cursor += 1
        else:
            sys.stdout.write(TERMINAL_BELL)

    def move_cursor_left(self) -> None:
        """
        The task of this method is to move the cursor one unit to the 'left'.
        (Here unit means one column in the terminal which is equivalent to one character)

        With the help of this method and relating it to a key, you can easily move
        to the 'left' among the user's input strings.

        :return: None
        """

        if self._cursor > 0:
            self._cursor -= 1
        else:
            sys.stdout.write(TERMINAL_BELL)

    def get_word_before_cursor(self) -> str:
        """
        The task of this method is to return the word before the cursor.
        This method returns only the word and does not count the empty space as part of the word.

        :return: str
        """

        splitted_text: list = self._text[:self._cursor].split()
        return splitted_text[-1] if splitted_text else ''

    def get_word_after_cursor(self) -> str:
        """
        The task of this method is to return the word after the cursor.
        This method returns only the word and does not count the empty space as part of the word.

        :return: str
        """

        splitted_text: list = self._text[self._cursor:].split()
        return splitted_text[0] if splitted_text else ''

    def get_text_before_cursor(self) -> str:
        """
        The task of this method is to return the text before the cursor.
        This method will return all the characters before the cursor in the form of a string.

        :return: str
        """

        return self._text[:self._cursor]

    def get_text_after_cursor(self) -> str:
        """
        The task of this method is to return the text after the cursor.
        This method will return all the characters after the cursor in the form of a string.

        :return: str
        """

        return self._text[self._cursor:]

    def del_word_before_cursor(self) -> None:
        """
        The task of this method is to delete the word that is
        before the cursor from the input string.

        This method does not return any value and will be in place.

        :return: None
        """

        for _ in range(len(self.get_word_before_cursor()) + 1):
            self.remove()

    def remove_word_after_cursor(self) -> None:
        """
        The task of this method is to delete the word that is
        after the cursor from the input string.

        This method does not return any value and will be in place.

        :return: None
        """

        len_of_word_after_cursor: int = len(self.get_word_after_cursor()) + 1

        self._cursor += len_of_word_after_cursor

        for _ in range(len_of_word_after_cursor):
            self.remove()

    def remove_text_before_cursor(self) -> None:
        """
        The task of this method is to delete the text that is
        before the cursor from the input string.

        This method does not return any value and will be in place.

        :return: None
        """

        for _ in range(len(self.get_text_before_cursor())):
            self.remove()

    def remove_text_after_cursor(self) -> None:
        """
        The task of this method is to delete the text that is
        after the cursor from the input string.

        This method does not return any value and will be in place.

        :return: None
        """

        len_of_text_after_cursor: int = len(self.get_text_after_cursor()) + 1

        self._cursor += len_of_text_after_cursor

        for _ in range(len_of_text_after_cursor):
            self.remove()

    @staticmethod
    def get_cursor_position() -> tuple[int, int]:
        """
        The task of this method is to read the cursor coordinates from
        the terminal screen using a special ANSI escape code.

        This method refers to a function with the same name in -> .keys.get_cursor_position()

        :return: tuple[int, int]
        """

        return gcp()

    @property
    def text(self) -> str:
        """
        A getter method to get the user input value.
        This method returns the input entered by the user in the form of a string.

        :return: str
        """

        return self._text

    @property
    def cursor(self) -> int:
        """
        A getter method to get the value and current location of the cursor.
        This method returns the cursor location in the form of an integer.

        :return: int
        """

        return self._cursor

    @property
    def formatted(self) -> dict:
        """
        A getter method to obtain formatted information from user input.
        This method returns the formatted data in the form of a dictionary.

        :return: dict
        """

        return self._formatted.copy()

    @property
    def last_key(self) -> str:
        """
        A getter method to get the last key entered by the user.
        This method returns the last key entered by the user in the form of a string.

        :return: str
        """

        return self._last_key

    @property
    def returned_value(self) -> str:
        """
        A getter method to get the returned value from conditions.
        This method returns the returned value from conditions in prompt.

        :return: str
        """

        return self._returned_value

    @property
    def ignored_keys(self) -> list:
        """
        A getter method to get the ignored keys data.
        This method returns all keys that were ignored in prompt process.

        :return: list
        """

        return self._ignored_keys

    @cursor.setter
    def cursor(self, cursor_: int) -> None:
        """
        A setter method to change cursor position to another location.
        The value of the 'cursor_' argument must be of integer type.

        :param cursor_: The new cursor position in integer format.
        :return: None
        """

        if isinstance(cursor_, int):
            if cursor_ <= self.limit:
                self._cursor = cursor_
            else:
                raise LimitError(
                    ('The value of the cursor is greater than the limit. '
                     f'cursor={cursor_}, limit={self.limit}')
                )
        else:
            raise TypeError(
                (f'The type of cursor_ argument must be integer, '
                 'but received "{type(cursor_)}".')
            )

    @formatted.setter
    def formatted(self, formatted_: dict) -> None:
        """
        A setter method to change formatted data to another format or style.
        The value of the 'formatted_' argument must be of dictionary type.

        :param formatted_: The new formatted data in dictionary type.
        :return: None
        """

        if isinstance(formatted_, dict):
            for key, value in formatted_.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise FormattedTypeError(
                        ('The type of key and value must be string, '
                         f'but received key="{type(key)}", value="{type(value)}".')
                    )

            self._formatted = formatted_.copy()
        else:
            raise TypeError(
                ('The type of formatted_ argument must be dictionary, '
                 f'but received "{type(formatted_)}".')
            )

    @ignored_keys.setter
    def ignored_keys(self, ignored_keys_: list) -> None:
        """
        A setter method to change ignored_keys data to add keys in it.
        The value of the 'ignored_keys_' argument must be of list type.

        :param ignored_keys_: The new ignored_keys list.
        :return: None
        """

        self._ignored_keys = ignored_keys_.copy()

    def clear(self) -> None:
        """
        The task of this method is to delete the input entered by the user.
        This method does not return any value and will be in place.

        :return: None
        """

        self._text = ""
        self._cursor = 0

    @abstractmethod
    def _display(self, be_returned: bool = False) -> None | str:
        pass

    @abstractmethod
    def prompt(self, conditions: tuple = None, pure_return: bool = True) -> str:
        pass

    def __ge__(self, other):
        if isinstance(other, BaseCprompt):
            return len(self._text) >= len(other._text)

        elif isinstance(other, str):
            return len(self._text) >= len(other)

        raise TypeError

    def __gt__(self, other):
        if isinstance(other, BaseCprompt):
            return len(self._text) > len(other._text)

        elif isinstance(other, str):
            return len(self._text) > len(other)

        raise TypeError

    def __eq__(self, other):
        if isinstance(other, BaseCprompt):
            return len(self._text) == len(other._text)

        elif isinstance(other, str):
            return len(self._text) == len(other)

        elif isinstance(other, bool):
            return True if self._text else False

        raise TypeError

    def __len__(self):
        return len(self._text)

    def __bool__(self):
        return True if len(self._text) > 0 else False

    def __str__(self):
        return self._text.__str__()

    def __repr__(self):
        return (
            f'{self.__class__}('
            f'message={self.message}, '
            f'conditions={self.conditions}, '
            f'text={self._text}, '
            f'cursor={self._cursor}, '
            f'formatted={self._formatted}, '
            f'limit={self.limit})'
        )