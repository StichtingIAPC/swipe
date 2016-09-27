

def _assert(truthvalue, errorstring=None):
    if not truthvalue:
        raise AssertionError(errorstring)
