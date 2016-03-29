
class CyclicParenthoodError(ValueError):
    def __init__(self, organisation):
        super(CyclicParenthoodError, self).__init__("Organisation {} has a cyclic parent tree.".format(organisation))
