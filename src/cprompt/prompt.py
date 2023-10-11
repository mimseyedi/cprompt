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


import sys
from base import BaseCprompt
from keys import readkey
from ansi import NEW_LINE, ERASE_ENTIRE_LINE, move_cursor_to_column


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

        if pure_return:
            return self._text

        return self._display(be_returned=True)