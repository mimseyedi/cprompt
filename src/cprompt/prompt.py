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

from keys import readkey
from ansi import (
    NEW_LINE,
    TERMINAL_BELL,
    ERASE_ENTIRE_LINE,
    extract_non_ansi,
    move_cursor_to_column,
    get_cursor_position as gcp,
)


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
                if self.__text:
                    termcol, _ = os.get_terminal_size()
                    if len(self.__text) + len(self.message) + 1 < termcol:
                        self.__text = self.__text[0:self.__cursor] + char + self.__text[self.__cursor:]
                        self.__cursor += 1
                else:
                    self.__text += char
                    self.__cursor += 1
            else:
                raise ValueError
        else:
            raise TypeError

    def insert_text(self, text: str) -> None:
        """
        The task of this method is to insert a text in the user's input string.
        This method is also responsible for removing ANSI escape codes from
        the user's input string and controlling the text limit.

        :param text: A string containing multiple characters.
        :return: None
        """

        if isinstance(text, str):
            status, string_ = extract_non_ansi(text)

            if status:
                for char in string_:
                    self._write(char)

                self.__formatted[string_] = text
            else:
                for char in text:
                    self._write(char)
        else:
            raise TypeError

    def remove(self) -> None:
        """
        The task of this method is to delete a character from the location of the cursor.
        This function pushes the cursor back and deletes one character from the written input.

        :return: None
        """

        if self.__cursor > 0:
            self.__cursor -= 1
            self.__text = self.__text[:self.__cursor] + self.__text[self.__cursor+1:]
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

        if self.__cursor < len(self.__text):
            self.__cursor += 1
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

        if self.__cursor > 0:
            self.__cursor -= 1
        else:
            sys.stdout.write(TERMINAL_BELL)

    def get_word_before_cursor(self) -> str:
        """
        The task of this method is to return the word before the cursor.
        This method returns only the word and does not count the empty space as part of the word.

        :return: str
        """

        splitted_text: list = self.__text[:self.__cursor].split()
        return splitted_text[-1] if splitted_text else ''

    def get_word_after_cursor(self) -> str:
        """
        The task of this method is to return the word after the cursor.
        This method returns only the word and does not count the empty space as part of the word.

        :return: str
        """

        splitted_text: list = self.__text[self.__cursor:].split()
        return splitted_text[0] if splitted_text else ''

    def get_text_before_cursor(self) -> str:
        """
        The task of this method is to return the text before the cursor.
        This method will return all the characters before the cursor in the form of a string.

        :return: str
        """

        return self.__text[:self.__cursor]

    def get_text_after_cursor(self) -> str:
        """
        The task of this method is to return the text after the cursor.
        This method will return all the characters after the cursor in the form of a string.

        :return: str
        """

        return self.__text[self.__cursor:]

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

        self.__cursor += len_of_word_after_cursor

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

        self.__cursor += len_of_text_after_cursor

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

        return self.__text

    @property
    def cursor(self) -> int:
        """
        A getter method to get the value and current location of the cursor.
        This method returns the cursor location in the form of an integer.

        :return: int
        """

        return self.__cursor

    @property
    def formatted(self) -> dict:
        """
        A getter method to obtain formatted information from user input.
        This method returns the formatted data in the form of a dictionary.

        :return: dict
        """

        return self.__formatted.copy()

    @property
    def last_key(self) -> str:
        """
        A getter method to get the last key entered by the user.
        This method returns the last key entered by the user in the form of a string.

        :return: str
        """

        return self.__last_key

    @text.setter
    def text(self, text_: str) -> None:
        """
        A setter method to change user input to another string.
        The value of the 'text_' argument must be of string type.

        :param text_: The new string that is supposed to replace the user input.
        :return: None
        """

        if isinstance(text_, str):
            self.__text = text_
            self.__cursor = len(self.__text)
        else:
            raise TypeError

    @cursor.setter
    def cursor(self, cursor_: int) -> None:
        """
        A setter method to change cursor position to another location.
        The value of the 'cursor_' argument must be of integer type.

        :param cursor_: The new cursor position in integer format.
        :return: None
        """

        if isinstance(cursor_, int):
            self.__cursor = cursor_
        else:
            raise TypeError

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
                    raise Exception

            self.__formatted = formatted_.copy()
        else:
            raise TypeError

    def clear(self) -> None:
        """
        The task of this method is to delete the input entered by the user.
        This method does not return any value and will be in place.

        :return: None
        """

        self.__text = ""

    def _display(self) -> None:
        """
        The task of this method is to display the user's input live and instantly.

        :return: None
        """

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

    def prompt(self, conditions: tuple=None) -> str:
        """
        The task of this method is to get input from the user.
        This method reads the keyboard with the help of a set of methods of this class
        and side file functions to manage the user's input to display, apply conditions and control the keys.

        This method can independently manage and check its conditions or
        inherit and follow the conditions of its instance.

        :param conditions: Conditions to be checked at the time of entry in the format of a tuple.
        :return: str
        """

        if conditions is None:
            conditions = self.conditions
        else:
            if not isinstance(conditions, tuple):
                raise TypeError

        self._display()

        while True:
            key: str = readkey()
            self.__last_key: str = key
            exit_status: bool = False

            if conditions:
                for func in conditions:
                    try:
                        func(self)
                        continue
                    except SystemExit:
                        exit_status = True
                    except TypeError:
                        raise Exception

            match key:
                case 'ENTER':
                    self._display()
                    sys.stdout.write(NEW_LINE)
                    break

                case 'BACKSPACE':
                    self.remove()

                case 'RIGHT':
                    self.move_cursor_right()

                case 'LEFT':
                    self.move_cursor_left()

                case 'SPACE':
                    self._write(" ")

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
                            self._write(key)

            self._display()

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