"""
Contains handy functions written for this project
"""
# IMPORTS


# FUNCTIONS
def infinite_sequence():
    """
    Yields an infinite sequence of numbers

    Yield
    -----
    num : int
        A number starting from 0 with three leading zeros
    """
    num = 0
    while True:
        yield f"{num:04d}"
        num += 1


def mklist(n):
    """
    Quick empty list assignment

    Parameters
    ----------
    n : str
        number of

    Yield
    -----
    empty_list : list
        Empty list
    """
    for i in range(n):
        empty_list = []

        yield empty_list


# VARIABLES


# EXECUTION


# OUTPUT


# END OF FILE
