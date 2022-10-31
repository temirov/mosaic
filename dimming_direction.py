from enum import Enum


class DimmingDirection(Enum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1
    TOP_TO_BOTTOM = 2
    BOTTOM_TO_TOP = 3
    LEFT_BOTTOM_CORNER_TO_RIGHT_TOP_CORNER = 4
    LEFT_TOP_CORNER_TO_RIGHT_BOTTOM_CORNER = 5
    UNIFORMED = 6
