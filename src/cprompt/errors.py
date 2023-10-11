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

This file is related to the errors/exceptions that are generated in the cprompt package
so that the errors can be categorized and it will be easier to deal with them in the end.
"""


class CpromptError(Exception):
    """
    A basic error for the Cprompt collection that all errors are based on.
    """


class ReadCursorPositionError(CpromptError):
    """
    This error is to specify the errors related to reading the cursor position.
    """


class LimitError(CpromptError):
    """
    This error is to specify errors that are related to the range of user input in input line.
    """


class ConditionIsNotCallableError(CpromptError):
    """
    This error is to specify the errors that are related to the conditions prompt reads them at the time of execution.
    (These terms must be functions/callable)
    """


class FormattedTypeError(CpromptError):
    """
    This error is to specify errors related to the type of keys and the values of the formatted attribute.
    (formatted: dict = {str: str, ...})
    """