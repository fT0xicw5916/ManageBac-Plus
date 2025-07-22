from enum import StrEnum


class ExtendedStrEnum(StrEnum):
    @classmethod
    def tolist(cls):
        return [c for c in cls]


class Colors(ExtendedStrEnum):
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
