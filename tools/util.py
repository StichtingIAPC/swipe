global ASSERT_COUNT
ASSERT_COUNT = 0


def _assert(truthvalue, errorstring=None):
    import warnings
    global ASSERT_COUNT
    ASSERT_COUNT += 1
    warnings.warn("_assert was used, but is deprecated. "
                  "Use the built-in self.assert<something> for tests, and use raiseif for checks {}".format(ASSERT_COUNT),
                  UserWarning, stacklevel=2)
    if not truthvalue:
        raise AssertionError(errorstring)


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
