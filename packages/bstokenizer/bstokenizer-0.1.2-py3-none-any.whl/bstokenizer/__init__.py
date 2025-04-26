"""
BeatSaber Tokenizer - A library for tokenizing and manipulating Beat Saber maps and replays.

Main components:
- BeatSaberMapTokenizer: Converts Beat Saber maps to and from token format
- BeatSaberReplayTokenizer: Converts Beat Saber replays to and from token format
- convert: Utility function to convert between map format versions (v2/v3/v4)

Command line tools:
- bsconvert: Command line tool for converting Beat Saber maps between formats
"""

from .version import __version__

# Import types first to avoid circular imports
from bstokenizer.TokenType import MapTokenType, ReplayTokenType
# Import main tokenizer classes
from bstokenizer.maptokenizer import BeatSaberMapTokenizer
from bstokenizer.replaytokenizer import BeatSaberReplayTokenizer
from bstokenizer.mapconvert import convert

# Make these available at the top level
__all__ = [
    'BeatSaberMapTokenizer',
    'BeatSaberReplayTokenizer',
    'MapTokenType',
    'ReplayTokenType',
    'convert'
]