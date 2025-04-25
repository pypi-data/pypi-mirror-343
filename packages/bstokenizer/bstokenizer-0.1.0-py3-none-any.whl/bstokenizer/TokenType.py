from enum import Enum

class MapTokenType(Enum):
    """Enum for different types of elements in a Beat Saber map"""
    BPM = "bpm"
    ROTATION = "rotation"
    COLOR_NOTE = "color_note"
    BOMB_NOTE = "bomb_note"
    OBSTACLE = "obstacle"
    SLIDER = "slider"
    BURST_SLIDER = "burst_slider"
    BASIC_EVENT = "basic_event"
    COLOR_BOOST = "color_boost"
    WAYPOINT = "waypoint"
    LIGHT_COLOR = "light_color"
    LIGHT_ROTATION = "light_rotation"
    LIGHT_TRANSLATION = "light_translation"
    VFX_EVENT = "vfx_event"

class ReplayTokenType(Enum):
    """Enum for different types of elements in a Beat Saber replay"""
    INFO = "info"
    FRAME = "frame"
    NOTE = "note"
    WALL = "wall"
    HEIGHT = "height"
    PAUSE = "pause"
    CONTROLLER_OFFSET = "controller_offset"
    USER_DATA = "user_data"