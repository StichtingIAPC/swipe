def raiseif(truthvalue, exception, *args):
    """
    :param truthvalue: Do I raise?
    :type truthvalue: bool
    :param exception: The exception to throw when the truthvalue is true
    :type exception: Type[Exception]
    :param args: arguments to give to the exception
    :return:
    """
    if truthvalue:
        raise exception(*args)


def raiseifnot(truthvalue, exception, *args):
    """
    :param truthvalue: Do I NOT raise?
    :type truthvalue: bool
    :param exception: The exception to throw when the truthvalue is true
    :type exception: Type[Exception]
    :param args: arguments to give to the exception
    :return:
    """
    if not truthvalue:
        raise exception(*args)
