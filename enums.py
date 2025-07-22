from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def tolist(cls):
        return [c.value for c in cls]
        # return list(map(lambda c: c.value, cls))


class Colors(ExtendedEnum):
    BLACK   = "black"
    # BROWN   = "brown"
    RED     = "red"
    # TAN     = "tan"
    ORANGE  = "orange"
    # GOLD    = "gold"
    YELLOW  = "yellow"
    GREEN   = "green"
    # CYAN    = "cyan"
    BLUE    = "blue"
    # INDIGO  = "indigo"
    PURPLE  = "purple"
    # MAGENTA = "magenta"
    PINK    = "pink"
