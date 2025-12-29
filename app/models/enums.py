import enum

class Frequency(enum.Enum):
    ONCE = "once"
    WEEKLY = "weekly"
    WEEK_A = "weekA"
    WEEK_B = "weekB"

class Color(enum.Enum):
    BLUE = "BLUE"
    GREEN = "GREEN"
    RED = "RED"
    YELLOW = "YELLOW"
    PURPLE = "PURPLE"
    ORANGE = "ORANGE"
    GRAY = "GRAY"

class Grade(enum.Enum):
    SECONDE = 10
    PREMIERE = 11
    TERMINALE = 12
    CPGE1 = 13
    CPGE2 = 14