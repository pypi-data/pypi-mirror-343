# This is a basic handler for custom data in elements.
from bstokenizer.maptokenizer import TokenType
from bstokenizer.heck.utils import beatwalls_coords_to_basegame # CustomData coords are beatwalls coords.
from typing import Dict, Any
import logging
import copy

# Designed for v3 only, use bstokenizer.mapconvert.convert for any other version.

def warn(msg: str = "No message") -> None:
    """
    Log a warning message.
    """
    logging.warning(msg)

def parse_custom_data(object_type: Any, object_data) -> Dict:
    """
    Parses customData from a given object and updates coordinates.
    
    Args:
        object_type: Type of the token (e.g., TokenType.COLOR_NOTE)
        object_data: Data object containing customData
        
    Returns:
        Updated object data with processed customData
    """
    if not object_data:
        return {}
    
    result = copy.deepcopy(object_data)
    
    if object_type == TokenType.BASIC_EVENT:
        warn("Custom data is not supported for basic events yet. (Coming soon)")
        return result
    
    # Handle coordinate conversion for supported types
    supported_types = [TokenType.BOMB_NOTE, TokenType.COLOR_NOTE, TokenType.OBSTACLE]
    if object_type in supported_types and result.get("customData") and result["customData"].get("coordinates"):
        coords = result["customData"]["coordinates"]
        x = coords[0] if coords else result.get("x", 0) - 2
        y = coords[1] if coords else result.get("y", 0)
        x, y = beatwalls_coords_to_basegame(x, y)
        
        result["x"] = x
        result["y"] = y
        
        # Clean up empty customData
        if not result["customData"]:
            del result["customData"]
    
    return result
