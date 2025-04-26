import json
import sys
from typing import Dict, Any, Tuple
import logging
import os

# DOES NOT support customdata! the customdata element will be removed from every map element.

# This file is very cluttered but it works. PLEASE do not use this outside of the internals of this project as it will likely change in the future.
# TODO: Clean this up and make it more readable.

def warn(message: str = "No message"):
    """Print a warning message"""
    logging.warning(message)


def convert(map_data: Dict[str, Any], target_version: str) -> Any:
    """
    Convert Beat Saber map between v2, v3, and v4 formats
    
    Args:
        map_data: The map data dictionary
        target_version: The target version ("v2", "v3", "v4", "2", "3", or "4")
    
    Returns:
        Converted map data or tuple of (beatmap, lightshow) for v4 format
    """
    # Determine source version
    if "_version" in map_data:
        source_version = "v2"
    elif map_data.get("version", "").startswith("4"):
        source_version = "v4"
    else:
        source_version = "v3"
    
    # Check for unsupported versions
    if source_version == "v3" and map_data.get("version", "").startswith("4"):
        raise ValueError(f"Map version {map_data.get('version')} has a version format issue")
    
    # Normalize target version format
    target_version = target_version.lower()
    if target_version not in ["v2", "2", "v3", "3", "v4", "4"] or not target_version.startswith(("2", "3", "4", "v2", "v3", "v4")):
        raise ValueError(f"Invalid target version: {target_version}. Expected 'v2', '2', 'v3', '3', 'v4', or '4'")
    
    # Normalize to simple version number
    if target_version in ["v2", "2"]:
        target_version = "v2" 
    elif target_version in ["v3", "3"]:
        target_version = "v3"
    else:
        target_version = "v4"
    
    # If already in target format, return as is
    if source_version == target_version:
        if source_version == "v4":
            warn("Source is already in v4 format. This library can't separate or combine beatmap and lightshow files.")
        return map_data
    
    # Convert based on direction
    if source_version == "v2":
        if target_version == "v3":
            return _convert_v2_to_v3(map_data)
        else:  # v2 to v4
            return _convert_v2_to_v4(map_data)
    elif source_version == "v3":
        if target_version == "v2":
            return _convert_v3_to_v2(map_data)
        else:  # v3 to v4
            return _convert_v3_to_v4(map_data)
    else:  # v4 to others
        if target_version == "v2":
            return _convert_v4_to_v2(map_data)
        else:  # v4 to v3
            return _convert_v4_to_v3(map_data)


def _convert_v2_to_v3(v2_map: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a v2 map format to v3 format"""
    v3_map = {
        "version": "3.3.0",  # Latest v3 version
    }
    
    # Convert notes
    color_notes = []
    bomb_notes = []
    if "_notes" in v2_map:
        for note in v2_map["_notes"]:
            if note.get("_type") == 3:  # Bomb
                bomb_notes.append({
                    "b": note["_time"],
                    "x": note["_lineIndex"],
                    "y": note["_lineLayer"],
                })
            elif note.get("_type") in [0, 1]:  # Red or Blue note
                color_notes.append({
                    "b": note["_time"],
                    "x": note["_lineIndex"],
                    "y": note["_lineLayer"],
                    "c": note["_type"],
                    "d": note["_cutDirection"],
                    "a": 0  # Default angle offset
                })
            else:
                warn(f"Unknown note type {note.get('_type')} at time {note.get('_time')}")
    
    if color_notes:
        v3_map["colorNotes"] = color_notes
    if bomb_notes:
        v3_map["bombNotes"] = bomb_notes
    
    # Convert obstacles
    if "_obstacles" in v2_map:
        obstacles = []
        for obs in v2_map["_obstacles"]:
            obstacles.append({
                "b": obs["_time"],
                "d": obs["_duration"],
                "x": obs["_lineIndex"],
                "y": obs["_lineLayer"],
                "w": obs["_width"],
                "h": obs["_height"]
            })
        if obstacles:
            v3_map["obstacles"] = obstacles
    
    # Convert sliders
    if "_sliders" in v2_map:
        sliders = []
        for slider in v2_map["_sliders"]:
            sliders.append({
                "c": slider["_colorType"],
                "b": slider["_headTime"],
                "x": slider["_headLineIndex"],
                "y": slider["_headLineLayer"],
                "d": slider["_headCutDirection"],
                "mu": slider.get("_headControlPointLengthMultiplier", 1),
                "tb": slider["_tailTime"],
                "tx": slider["_tailLineIndex"],
                "ty": slider["_tailLineLayer"],
                "tc": slider["_tailCutDirection"],
                "tmu": slider.get("_tailControlPointLengthMultiplier", 1),
                "m": slider.get("_sliderMidAnchorMode", 0)
            })
        if sliders:
            v3_map["sliders"] = sliders
    
    # Convert waypoints
    if "_waypoints" in v2_map:
        waypoints = []
        for wp in v2_map["_waypoints"]:
            waypoints.append({
                "b": wp["_time"],
                "x": wp["_lineIndex"],
                "y": wp["_lineLayer"],
                "d": wp["_offsetDirection"]
            })
        if waypoints:
            v3_map["waypoints"] = waypoints
    
    # Convert events
    if "_events" in v2_map:
        basic_events = []
        color_boost_events = []
        rotation_events = []
        bpm_events = []
        
        for event in v2_map["_events"]:
            event_time = event["_time"]
            event_type = event["_type"]
            event_value = event["_value"]
            
            if event_type == 5:  # Color boost events
                color_boost_events.append({
                    "b": event_time,
                    "o": bool(event_value)
                })
            elif event_type in [14, 15]:  # Rotation events
                rotation_events.append({
                    "b": event_time,
                    "e": 1 if event_type == 15 else 0,
                    "r": event_value
                })
            elif event_type == 100:  # BPM change
                bpm_events.append({
                    "b": event_time,
                    "m": event.get("_floatValue", event_value)
                })
            else:  # Basic events
                basic_events.append({
                    "b": event_time,
                    "et": event_type,
                    "i": event_value,
                    "f": event.get("_floatValue", 1)
                })
        
        if basic_events:
            v3_map["basicBeatmapEvents"] = basic_events
        if color_boost_events:
            v3_map["colorBoostBeatmapEvents"] = color_boost_events
        if rotation_events:
            v3_map["rotationEvents"] = rotation_events
        if bpm_events:
            v3_map["bpmEvents"] = bpm_events
    
    # Convert special events keyword filters
    if "_specialEventsKeywordFilters" in v2_map:
        v2_filters = v2_map["_specialEventsKeywordFilters"]
        if "_keywords" in v2_filters and v2_filters["_keywords"]:
            v3_filters = {"d": []}
            
            for keyword_filter in v2_filters["_keywords"]:
                v3_filters["d"].append({
                    "k": keyword_filter["_keyword"],
                    "e": keyword_filter["_specialEvents"]
                })
            
            v3_map["basicEventTypesWithKeywords"] = v3_filters
    
    # Note about missing complex events
    warn("Light event box groups, VFX events, and burst sliders may not be properly converted from v2 to v3")
    
    return v3_map


def _convert_v3_to_v2(v3_map: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a v3 map format to v2 format"""
    v2_map = {
        "_version": "2.6.0",  # Latest v2 version
    }
    
    # Convert color notes and bomb notes to _notes
    notes = []
    if "colorNotes" in v3_map:
        for note in v3_map["colorNotes"]:
            if note.get("a", 0) != 0:
                warn(f"Angle offset {note.get('a')} will be lost in v2 conversion")
            
            notes.append({
                "_time": note["b"],
                "_lineIndex": note["x"],
                "_lineLayer": note["y"],
                "_type": note["c"],
                "_cutDirection": note["d"]
            })
    
    if "bombNotes" in v3_map:
        for bomb in v3_map["bombNotes"]:
            notes.append({
                "_time": bomb["b"],
                "_lineIndex": bomb["x"],
                "_lineLayer": bomb["y"],
                "_type": 3,
                "_cutDirection": 0
            })
    
    if notes:
        v2_map["_notes"] = notes
    
    # Convert obstacles
    if "obstacles" in v3_map:
        obstacles = []
        for obs in v3_map["obstacles"]:
            obstacles.append({
                "_time": obs["b"],
                "_duration": obs["d"],
                "_lineIndex": obs["x"],
                "_lineLayer": obs["y"],
                "_width": obs["w"],
                "_height": obs["h"],
                "_type": 0  # Default type
            })
        if obstacles:
            v2_map["_obstacles"] = obstacles
    
    # Convert sliders
    sliders = []
    if "sliders" in v3_map:
        for slider in v3_map["sliders"]:
            sliders.append({
                "_colorType": slider["c"],
                "_headTime": slider["b"],
                "_headLineIndex": slider["x"],
                "_headLineLayer": slider["y"],
                "_headCutDirection": slider["d"],
                "_headControlPointLengthMultiplier": slider.get("mu", 1),
                "_tailTime": slider["tb"],
                "_tailLineIndex": slider["tx"],
                "_tailLineLayer": slider["ty"],
                "_tailCutDirection": slider["tc"],
                "_tailControlPointLengthMultiplier": slider.get("tmu", 1),
                "_sliderMidAnchorMode": slider.get("m", 0)
            })

    if sliders:
        v2_map["_sliders"] = sliders
    
    if "burstSliders" in v3_map and len(v3_map.get("burstSliders", [])) > 0:
        warn("Burst sliders (Chains) are not supported in v2 format and will be lost.")
    
    # Convert waypoints
    if "waypoints" in v3_map:
        waypoints = []
        for wp in v3_map["waypoints"]:
            waypoints.append({
                "_time": wp["b"],
                "_lineIndex": wp["x"],
                "_lineLayer": wp["y"],
                "_offsetDirection": wp["d"]
            })
        if waypoints:
            v2_map["_waypoints"] = waypoints
    
    # Convert events
    events = []
    
    # Basic beat events
    if "basicBeatmapEvents" in v3_map:
        for event in v3_map["basicBeatmapEvents"]:
            events.append({
                "_time": event["b"],
                "_type": event["et"],
                "_value": event.get("i", event.get("v", 0)),
                "_floatValue": event.get("f", 1)
            })
    
    # Color boost events
    if "colorBoostBeatmapEvents" in v3_map:
        for event in v3_map["colorBoostBeatmapEvents"]:
            events.append({
                "_time": event["b"],
                "_type": 5,
                "_value": 1 if event["o"] else 0,
                "_floatValue": 0
            })
    
    # Rotation events
    if "rotationEvents" in v3_map:
        for event in v3_map["rotationEvents"]:
            events.append({
                "_time": event["b"],
                "_type": 14 if event["e"] == 0 else 15,
                "_value": event["r"],
                "_floatValue": 0
            })
    
    # BPM events
    if "bpmEvents" in v3_map:
        for event in v3_map["bpmEvents"]:
            events.append({
                "_time": event["b"],
                "_type": 100,
                "_value": 0,
                "_floatValue": event["m"]
            })
    
    if events:
        v2_map["_events"] = events
    
    # Convert event keywords
    if "basicEventTypesWithKeywords" in v3_map:
        v3_filters = v3_map["basicEventTypesWithKeywords"]
        v2_filters = {"_keywords": []}
        
        if "d" in v3_filters:
            for keyword_filter in v3_filters["d"]:
                v2_filters["_keywords"].append({
                    "_keyword": keyword_filter["k"],
                    "_specialEvents": keyword_filter["e"]
                })
            
            v2_map["_specialEventsKeywordFilters"] = v2_filters
    
    # Warn about complex v3 features not supported in v2
    if any(key in v3_map for key in ["lightColorEventBoxGroups", "lightRotationEventBoxGroups", 
                                    "lightTranslationEventBoxGroups", "vfxEventBoxGroups"]):
        warn("Complex light events from v3 cannot be converted to v2 format and will be lost")
    
    return v2_map


def _convert_v4_to_v3(v4_map: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a v4 map format to v3 format"""
    warn("Converting from v4 to v3 format will result in significant data loss")
    
    v3_map = {
        "version": "3.3.0",
    }
    
    # Convert color notes
    if "colorNotes" in v4_map and "colorNotesData" in v4_map:
        color_notes = []
        for i, note in enumerate(v4_map["colorNotes"]):
            if i >= len(v4_map["colorNotesData"]):
                warn(f"Missing colorNotesData for note at index {i}")
                continue
                
            data = v4_map["colorNotesData"][note.get("i", i)]
            color_notes.append({
                "b": note["b"],
                "x": data["x"],
                "y": data["y"],
                "c": data["c"],
                "d": data["d"],
                "a": data.get("a", 0)
            })
        
        if color_notes:
            v3_map["colorNotes"] = color_notes
    
    # Convert bomb notes
    if "bombNotes" in v4_map and "bombNotesData" in v4_map:
        bomb_notes = []
        for i, bomb in enumerate(v4_map["bombNotes"]):
            if i >= len(v4_map["bombNotesData"]):
                warn(f"Missing bombNotesData for bomb at index {i}")
                continue
                
            data = v4_map["bombNotesData"][bomb.get("i", i)]
            bomb_notes.append({
                "b": bomb["b"],
                "x": data["x"],
                "y": data["y"]
            })
        
        if bomb_notes:
            v3_map["bombNotes"] = bomb_notes
    
    # Convert obstacles
    if "obstacles" in v4_map and "obstaclesData" in v4_map:
        obstacles = []
        for i, obs in enumerate(v4_map["obstacles"]):
            if i >= len(v4_map["obstaclesData"]):
                warn(f"Missing obstaclesData for obstacle at index {i}")
                continue
                
            data = v4_map["obstaclesData"][obs.get("i", i)]
            obstacles.append({
                "b": obs["b"],
                "d": data["d"],
                "x": data["x"],
                "y": data["y"],
                "w": data["w"],
                "h": data["h"]
            })
        
        if obstacles:
            v3_map["obstacles"] = obstacles
            
    # Convert arcs to sliders
    if "arcs" in v4_map and "arcsData" in v4_map:
        sliders = []
        for i, arc in enumerate(v4_map["arcs"]):
            if i >= len(v4_map["arcsData"]):
                warn(f"Missing arcsData for arc at index {i}")
                continue
                
            # Get head and tail data indices
            headIndex = arc.get("hi", i*2)
            tailIndex = arc.get("ti", i*2+1)
            
            # Check if we have colorNotesData for these indices
            if "colorNotesData" not in v4_map or headIndex >= len(v4_map["colorNotesData"]) or tailIndex >= len(v4_map["colorNotesData"]):
                warn(f"Missing colorNotesData for arc at index {i}")
                continue
                
            headData = v4_map["colorNotesData"][headIndex]
            tailData = v4_map["colorNotesData"][tailIndex]
            arcData = v4_map["arcsData"][arc.get("ai", i)]
            
            sliders.append({
                "c": headData.get("c", 0),
                "b": arc["hb"],
                "x": headData.get("x", 0),
                "y": headData.get("y", 0),
                "d": headData.get("d", 0),
                "mu": arcData.get("m", 1),
                "tb": arc["tb"],
                "tx": tailData.get("x", 0),
                "ty": tailData.get("y", 0),
                "tc": tailData.get("d", 0),
                "tmu": arcData.get("tm", 1),
                "m": 0  # Default mode
            })
        
        if sliders:
            warn("Arc conversion from v4 to v3 may be incomplete due to significant format differences")
            v3_map["sliders"] = sliders
            
    # Convert chains to burstSliders
    if "chains" in v4_map and "chainsData" in v4_map:
        burstSliders = []
        for i, chain in enumerate(v4_map["chains"]):
            if i >= len(v4_map["chainsData"]):
                warn(f"Missing chainsData for chain at index {i}")
                continue
                
            # Get head data
            headIndex = chain.get("i", i)
            if "colorNotesData" not in v4_map or headIndex >= len(v4_map["colorNotesData"]):
                warn(f"Missing colorNotesData for chain at index {i}")
                continue
                
            headData = v4_map["colorNotesData"][headIndex]
            chainData = v4_map["chainsData"][chain.get("ci", i)]
            
            burstSliders.append({
                "b": chain["hb"],
                "x": headData.get("x", 0),
                "y": headData.get("y", 0),
                "c": headData.get("c", 0),
                "d": headData.get("d", 0),
                "tb": chain["tb"],
                "tx": chainData.get("tx", 0),
                "ty": chainData.get("ty", 0),
                "sc": chainData.get("c", 3),
                "s": chainData.get("s", 0.5)
            })
        
        if burstSliders:
            warn("Chain conversion from v4 to v3 may be incomplete due to significant format differences")
            v3_map["burstSliders"] = burstSliders
    
    # Look for lightshow file elements if present in the map
    if "basicEvents" in v4_map and "basicEventsData" in v4_map:
        basic_events = []
        for i, event in enumerate(v4_map["basicEvents"]):
            if i >= len(v4_map["basicEventsData"]):
                warn(f"Missing basicEventsData for event at index {i}")
                continue
                
            data = v4_map["basicEventsData"][event.get("i", i)]
            basic_events.append({
                "b": event["b"],
                "et": data.get("t", 0),
                "i": data.get("i", 0),
                "f": data.get("f", 1)
            })
        
        if basic_events:
            v3_map["basicBeatmapEvents"] = basic_events
    
    # Convert color boost events
    if "colorBoostEvents" in v4_map and "colorBoostEventsData" in v4_map:
        color_boost_events = []
        for i, event in enumerate(v4_map["colorBoostEvents"]):
            if i >= len(v4_map["colorBoostEventsData"]):
                warn(f"Missing colorBoostEventsData for event at index {i}")
                continue
                
            data = v4_map["colorBoostEventsData"][event.get("i", i)]
            color_boost_events.append({
                "b": event["b"],
                "o": bool(data.get("b", True))
            })
        
        if color_boost_events:
            v3_map["colorBoostBeatmapEvents"] = color_boost_events
    
    # Convert waypoints
    if "waypoints" in v4_map and "waypointsData" in v4_map:
        waypoints = []
        for i, wp in enumerate(v4_map["waypoints"]):
            if i >= len(v4_map["waypointsData"]):
                warn(f"Missing waypointsData for waypoint at index {i}")
                continue
                
            data = v4_map["waypointsData"][wp.get("i", i)]
            waypoints.append({
                "b": wp["b"],
                "x": data["x"],
                "y": data["y"],
                "d": data["d"]
            })
        
        if waypoints:
            v3_map["waypoints"] = waypoints
    
    # Convert event keywords
    if "basicEventTypesWithKeywords" in v4_map:
        v3_map["basicEventTypesWithKeywords"] = v4_map["basicEventTypesWithKeywords"]
    
    # NJS events are not directly mappable to v3
    if "njsEvents" in v4_map:
        warn("NJS events from v4 format are not supported in v3 and will be lost")
    
    # Complex lighting events are not properly converted
    if any(key in v4_map for key in ["eventBoxGroups", "lightColorEventBoxes", "lightRotationEventBoxes", 
                                     "lightTranslationEventBoxes", "fxEventBoxes"]):
        warn("Complex lighting events from v4 format will be lost in v3 conversion")
    
    return v3_map


def _convert_v4_to_v2(v4_map: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a v4 map format to v2 format"""
    # First convert to v3, then to v2
    v3_map = _convert_v4_to_v3(v4_map)
    return _convert_v3_to_v2(v3_map)


def _convert_v3_to_v4(v3_map: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Convert a v3 map format to v4 format (beatmap and lightshow)"""
    warn("Converting from v3 to v4 format will result in some data restructuring")
    
    beatmap = {
        "version": "4.0.0",
    }
    
    lightshow = {
        "version": "4.0.0",
        "useNormalEventsAsCompatibleEvents": True
    }
    
    # Convert color notes
    if "colorNotes" in v3_map:
        color_notes = []
        color_notes_data = []
        
        for i, note in enumerate(v3_map["colorNotes"]):
            color_notes.append({
                "b": note["b"],
                "r": 0,  # Default rotation value
                "i": i
            })
            color_notes_data.append({
                "x": note["x"],
                "y": note["y"],
                "c": note["c"],
                "d": note["d"],
                "a": note.get("a", 0)
            })
        
        if color_notes:
            beatmap["colorNotes"] = color_notes
            beatmap["colorNotesData"] = color_notes_data
    
    # Convert bomb notes
    if "bombNotes" in v3_map:
        bomb_notes = []
        bomb_notes_data = []
        
        for i, bomb in enumerate(v3_map["bombNotes"]):
            bomb_notes.append({
                "b": bomb["b"],
                "r": 0,  # Default rotation value
                "i": i
            })
            bomb_notes_data.append({
                "x": bomb["x"],
                "y": bomb["y"]
            })
        
        if bomb_notes:
            beatmap["bombNotes"] = bomb_notes
            beatmap["bombNotesData"] = bomb_notes_data
    
    # Convert obstacles
    if "obstacles" in v3_map:
        obstacles = []
        obstacles_data = []
        
        for i, obs in enumerate(v3_map["obstacles"]):
            obstacles.append({
                "b": obs["b"],
                "r": 0,  # Default rotation value
                "i": i
            })
            obstacles_data.append({
                "d": obs["d"],
                "x": obs["x"],
                "y": obs["y"],
                "w": obs["w"],
                "h": obs["h"]
            })
        
        if obstacles:
            beatmap["obstacles"] = obstacles
            beatmap["obstaclesData"] = obstacles_data
    
    # Convert sliders to arcs
    if "sliders" in v3_map:
        arcs = []
        arcs_data = []
        colorNotes = beatmap.get("colorNotes", [])
        colorNotesData = beatmap.get("colorNotesData", [])
        
        slider_note_start_idx = len(colorNotesData)
        
        for i, slider in enumerate(v3_map["sliders"]):
            # Head note
            head_idx = slider_note_start_idx + (i * 2)
            tail_idx = slider_note_start_idx + (i * 2) + 1
            
            colorNotes.append({
                "b": slider["b"],
                "r": 0,
                "i": head_idx
            })
            colorNotesData.append({
                "x": slider["x"],
                "y": slider["y"],
                "c": slider["c"],
                "d": slider["d"],
                "a": 0
            })
            
            # Tail note
            colorNotes.append({
                "b": slider["tb"],
                "r": 0,
                "i": tail_idx
            })
            colorNotesData.append({
                "x": slider["tx"],
                "y": slider["ty"],
                "c": slider["c"],
                "d": slider["tc"],
                "a": 0
            })
            
            # Add arc
            arcs.append({
                "hb": slider["b"],
                "tb": slider["tb"],
                "hr": 0,
                "tr": 0,
                "hi": head_idx,
                "ti": tail_idx,
                "ai": i
            })
            arcs_data.append({
                "m": slider.get("m", 0),
                "tm": slider.get("tmu", 1),
                "a": 0
            })
        
        if arcs:
            beatmap["colorNotes"] = colorNotes
            beatmap["colorNotesData"] = colorNotesData
            beatmap["arcs"] = arcs
            beatmap["arcsData"] = arcs_data
    
    # Convert burst sliders to chains
    if "burstSliders" in v3_map and v3_map["burstSliders"]:
        chains = []
        chains_data = []
        colorNotes = beatmap.get("colorNotes", [])
        colorNotesData = beatmap.get("colorNotesData", [])
        
        chain_note_start_idx = len(colorNotesData)
        
        for i, chain in enumerate(v3_map["burstSliders"]):
            # Head note
            note_idx = chain_note_start_idx + i
            
            colorNotes.append({
                "b": chain["b"],
                "r": 0,
                "i": note_idx
            })
            colorNotesData.append({
                "x": chain["x"],
                "y": chain["y"],
                "c": chain["c"],
                "d": chain["d"],
                "a": 0
            })
            
            # Add chain
            chains.append({
                "hb": chain["b"],
                "tb": chain["tb"],
                "hr": 0,
                "tr": 0,
                "i": note_idx,
                "ci": i
            })
            chains_data.append({
                "tx": chain["tx"],
                "ty": chain["ty"],
                "c": chain.get("sc", 3),
                "s": chain.get("s", 0.5)
            })
        
        if chains:
            beatmap["colorNotes"] = colorNotes
            beatmap["colorNotesData"] = colorNotesData
            beatmap["chains"] = chains
            beatmap["chainsData"] = chains_data
    
    # Convert events to lightshow
    if "basicBeatmapEvents" in v3_map:
        basic_events = []
        basic_events_data = []
        
        for i, event in enumerate(v3_map["basicBeatmapEvents"]):
            basic_events.append({
                "b": event["b"],
                "i": i
            })
            basic_events_data.append({
                "t": event.get("et", 0),
                "i": event.get("i", 0),
                "f": event.get("f", 1)
            })
        
        if basic_events:
            lightshow["basicEvents"] = basic_events
            lightshow["basicEventsData"] = basic_events_data
    
    # Convert color boost events
    if "colorBoostBeatmapEvents" in v3_map:
        boost_events = []
        boost_events_data = []
        
        for i, event in enumerate(v3_map["colorBoostBeatmapEvents"]):
            boost_events.append({
                "b": event["b"],
                "i": i
            })
            boost_events_data.append({
                "b": 1 if event.get("o", False) else 0
            })
        
        if boost_events:
            lightshow["colorBoostEvents"] = boost_events
            lightshow["colorBoostEventsData"] = boost_events_data
    
    # Convert waypoints
    if "waypoints" in v3_map:
        waypoints = []
        waypoints_data = []
        
        for i, wp in enumerate(v3_map["waypoints"]):
            waypoints.append({
                "b": wp["b"],
                "i": i
            })
            waypoints_data.append({
                "x": wp["x"],
                "y": wp["y"],
                "d": wp["d"]
            })
        
        if waypoints:
            lightshow["waypoints"] = waypoints
            lightshow["waypointsData"] = waypoints_data
    
    # Convert event keywords
    if "basicEventTypesWithKeywords" in v3_map:
        lightshow["basicEventTypesWithKeywords"] = v3_map["basicEventTypesWithKeywords"]
    
    # Advanced lighting features can't be properly converted
    if any(key in v3_map for key in ["lightColorEventBoxGroups", "lightRotationEventBoxGroups", 
                                     "lightTranslationEventBoxGroups", "vfxEventBoxGroups"]):
        warn("Advanced lighting features from v3 format will need to be reconstructed in v4")
    
    return (beatmap, lightshow)


def _convert_v2_to_v4(v2_map: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Convert a v2 map format to v4 format (beatmap and lightshow)"""
    # First convert to v3, then to v4
    v3_map = _convert_v2_to_v3(v2_map)
    return _convert_v3_to_v4(v3_map)


def main():
    """Main function to handle CLI interface"""
    if len(sys.argv) < 3:
        print("Usage: python mapconvert.py <input_file> <output_file> [--v2|--v3|--v4]")
        print("For v4 format, <output_file> will be used as a base name for beatmap and lightshow files")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Default conversion direction
    target_version = None
    if len(sys.argv) >= 4:
        if sys.argv[3] in ["--v2", "--v3", "--v4"]:
            target_version = sys.argv[3][2:]  # Remove the '--' prefix
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            map_data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    # Auto-detect target version if not specified
    if target_version is None:
        if "_version" in map_data:
            target_version = "v3"  # Convert from v2 to v3
            print("Auto-detected v2 format, converting to v3")
        elif map_data.get("version", "").startswith("4"):
            target_version = "v3"  # Convert from v4 to v3
            print("Auto-detected v4 format, converting to v3")
        elif "version" in map_data:
            target_version = "v2"  # Convert from v3 to v2
            print("Auto-detected v3 format, converting to v2")
        else:
            print("Could not auto-detect map version. Please specify --v2, --v3 or --v4")
            sys.exit(1)
    
    try:
        output_data = convert(map_data, target_version)
        
        # Handle v4 output (tuple of beatmap and lightshow)
        if isinstance(output_data, tuple):
            beatmap, lightshow = output_data
            
            # Create output filenames
            output_base = os.path.splitext(output_file)[0]
            beatmap_file = f"{output_base}_Beatmap.dat"
            lightshow_file = f"{output_base}_Lightshow.dat"
            
            # Save beatmap
            with open(beatmap_file, 'w', encoding='utf-8') as f:
                json.dump(beatmap, f, indent=2)
                
            # Save lightshow
            with open(lightshow_file, 'w', encoding='utf-8') as f:
                json.dump(lightshow, f, indent=2)
                
            print("Conversion completed:")
            print(f"- Beatmap: {beatmap_file}")
            print(f"- Lightshow: {lightshow_file}")
        else:
            # Standard single file output
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
            print(f"Conversion completed: {input_file} → {output_file}")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()