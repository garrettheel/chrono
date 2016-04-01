class Level(object):
    class Enum(object):
        def __init__(self, name, order):
            self.name = name
            self.order = order

        def __cmp__(self, other):
            if other is None:
                return 1
            elif not isinstance(other, self.__class__):
                raise ValueError("Can't compare types: {}, {}".format(
                                 self.__class__, other.__class__))
            return cmp(self.order, other.order)

        def __repr__(self):
            return "Level<{}>".format(self.name)

        def to_json(self):
            return self.name

    @classmethod
    def from_string(clz, level):
        return getattr(clz, level.upper())

    UNKNOWN = Enum('unknown', -1)
    NORMAL = Enum('normal', 0)
    WARNING = Enum('warning', 1)
    CRITICAL = Enum('critical', 2)
