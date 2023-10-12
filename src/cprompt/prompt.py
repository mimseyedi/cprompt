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
from base import BaseCprompt
from keys import KEYS, readkey
from ansi import (
    NEW_LINE,
    ERASE_ENTIRE_LINE,
    move_cursor,
    get_cursor_position,
    move_cursor_to_column,
)
from errors import (
    KeyNotRecognizedError,
)


class Cprompt(BaseCprompt):
    """

    """

    def __init__(
        self,
        message: str="",
        *,
        limit: int=None,
        conditions: tuple=None,
    ):
        super().__init__(
            message,
            limit=limit,
            conditions=conditions,
        )

    def _display(self, be_returned: bool=False) -> None|str:
        """
        The task of this method is to display the user's input live and instantly.

        :param be_returned: Will the formatted user input be returned?
        :return: None
        """

        temp: str = self._text.replace(" ", " - ")

        output: list = []
        for word in temp.split():
            if word in self._formatted.keys():
                output.append(self._formatted[word])
            else:
                if word == '-':
                    output.append(" ")
                else:
                    output.append(word)

        sys.stdout.write(ERASE_ENTIRE_LINE)
        sys.stdout.write(move_cursor_to_column(col=0))

        if be_returned:
            return ''.join(output)

        sys.stdout.write(
            self.message + ''.join(output) + move_cursor_to_column(col=self._cursor+len(self.message)+1)
        )
        sys.stdout.flush()

    def prompt(self, conditions: tuple=None, pure_return: bool=True) -> str:
        """
        The task of this method is to get input from the user.
        This method reads the keyboard with the help of a set of methods of this class
        and side file functions to manage the user's input to display, apply conditions and control the keys.

        This method can independently manage and check its conditions or
        inherit and follow the conditions of its instance.

        :param conditions: Conditions to be checked at the time of entry in the format of a tuple.
        :param pure_return: Is the actual value of the text returned or formatted?
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
            self._last_key: str = key
            exit_status: bool = False

            if conditions:
                for func in conditions:
                    try:
                        self._returned_value = func(self)
                    except SystemExit:
                        exit_status = True
                    except TypeError:
                        raise Exception

            if key not in self.ignored_keys:
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

        if pure_return:
            return self._text

        return self._display(be_returned=True)


class HintPrompt(BaseCprompt):
    """

    """

    def __init__(
        self,
        hint: str,
        message: str="",
        *,
        limit: int=None,
        conditions: tuple=None,
    ):
        super().__init__(
            message,
            limit=limit,
            conditions=conditions,
        )
        if isinstance(hint, str):
            self.hint = hint
        else:
            raise TypeError

    def _display(self, be_returned: bool=False) -> None|str:
        """
        The task of this method is to display the user's input live and instantly.

        :param be_returned: Will the formatted user input be returned?
        :return: None
        """

        temp: str = self._text.replace(" ", " - ")

        output: list = []
        for word in temp.split():
            if word in self._formatted.keys():
                output.append(self._formatted[word])
            else:
                if word == '-':
                    output.append(" ")
                else:
                    output.append(word)

        sys.stdout.write(ERASE_ENTIRE_LINE)
        sys.stdout.write(move_cursor_to_column(col=0))

        if be_returned:
            return ''.join(output)

        if len(self.text) == 0:
            sys.stdout.write(self.message + self.hint + move_cursor_to_column(len(self.message)+1))
            sys.stdout.flush()
        else:
            sys.stdout.write(
                self.message + ''.join(output) + move_cursor_to_column(col=self._cursor+len(self.message)+1)
            )
            sys.stdout.flush()

    def prompt(self, conditions: tuple=None, pure_return: bool=True) -> str:
        """
        The task of this method is to get input from the user.
        This method reads the keyboard with the help of a set of methods of this class
        and side file functions to manage the user's input to display, apply conditions and control the keys.

        This method can independently manage and check its conditions or
        inherit and follow the conditions of its instance.

        :param conditions: Conditions to be checked at the time of entry in the format of a tuple.
        :param pure_return: Is the actual value of the text returned or formatted?
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
            self._last_key: str = key
            exit_status: bool = False

            if conditions:
                for func in conditions:
                    try:
                        self._returned_value = func(self)
                    except SystemExit:
                        exit_status = True
                    except TypeError:
                        raise Exception

            if key not in self.ignored_keys:
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

        if pure_return:
            return self._text

        return self._display(be_returned=True)


class CommandPrompt(BaseCprompt):
    """

    """

    def __init__(
        self,
        message: str = "",
        ckey: str = 'UP',
        *,
        limit: int = None,
        conditions: tuple = None,
    ):
        super().__init__(
            message,
            limit=limit,
            conditions=conditions,
        )

        if isinstance(ckey, str):
            if ckey.lower() in KEYS.keys() or (len(ckey) == 1 and ckey.isalpha()):
                self.ckey = ckey
            else:
                raise KeyNotRecognizedError()
        else:
            raise TypeError

        self.__pre_row, self.__pre_col = get_cursor_position()

    def _display(self, be_returned: bool=False) -> None|str:
        """
        The task of this method is to display the user's input live and instantly.

        :param be_returned: Will the formatted user input be returned?
        :return: None
        """

        temp: str = self._text.replace(" ", " - ")

        output: list = []
        for word in temp.split():
            if word in self._formatted.keys():
                output.append(self._formatted[word])
            else:
                if word == '-':
                    output.append(" ")
                else:
                    output.append(word)

        _, termrow = os.get_terminal_size()

        sys.stdout.write(move_cursor(termrow, 0))
        sys.stdout.write(ERASE_ENTIRE_LINE)
        sys.stdout.write(move_cursor_to_column(col=0))

        if be_returned:
            return ''.join(output)

        sys.stdout.write(
            self.message + ''.join(output) + move_cursor_to_column(col=self._cursor+len(self.message)+1)
        )
        sys.stdout.flush()

    def prompt(self, conditions: tuple=None, pure_return: bool=True) -> str:
        """
        The task of this method is to get input from the user.
        This method reads the keyboard with the help of a set of methods of this class
        and side file functions to manage the user's input to display, apply conditions and control the keys.

        This method can independently manage and check its conditions or
        inherit and follow the conditions of its instance.

        :param conditions: Conditions to be checked at the time of entry in the format of a tuple.
        :param pure_return: Is the actual value of the text returned or formatted?
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
            self._last_key: str = key
            exit_status: bool = False

            if conditions:
                for func in conditions:
                    try:
                        self._returned_value = func(self)
                    except SystemExit:
                        exit_status = True
                    except TypeError:
                        raise Exception

            if key not in self.ignored_keys:
                match key:
                    case 'ENTER':
                        sys.stdout.write(ERASE_ENTIRE_LINE)
                        sys.stdout.write(move_cursor(self.__pre_row, self.__pre_col))
                        sys.stdout.flush()
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

        if pure_return:
            return self._text

        return self._display(be_returned=True)

    def show(self, prompt: BaseCprompt) -> str:
        """
        The task of this method is to prepare and execute the desired prompt
        in the case of a condition for another prompt.

        :param prompt: A BaseCprompt object.
        :return: str
        """

        prompt.ignored_keys.append(self.ckey)

        if prompt.last_key == self.ckey:
            return self.prompt()