import json
from typing import Dict, List, Union, Optional, Set
from bstokenizer import mapconvert, MapTokenType as TokenType
from bstokenizer.heck import customDataHandler

# This tokenizer does not support all map features, just up to 3.3.0 (conversion from older and newer formats will be done automatically)
# Supports versions v2.0.0 - v4.1.0 (and possibly newer)
# Note: The Beat Saber map format is subject to change, and this tokenizer may not support all features of future versions.


class BeatSaberMapTokenizer:
    """Tokenizer for Beat Saber maps"""

    def __init__(self, default_bpm: float = 120.0):
        """
        Initialize the tokenizer with a default BPM

        Args:
            default_bpm: Default beats per minute if not specified in map
        """
        self.default_bpm = default_bpm
        self.version = None
        self.bpm_changes = []  # List of (beat, bpm) tuples for time conversion

    def _beats_to_seconds(self, beat: float) -> float:
        """
        Convert beat position to seconds based on BPM changes

        Args:
            beat: Beat position

        Returns:
            Time in seconds
        """
        if not self.bpm_changes:
            # No BPM changes, use default BPM
            return (beat * 60) / self.default_bpm

        # Sort BPM changes by beat
        sorted_changes = sorted(self.bpm_changes, key=lambda x: x[0])

        # If beat is before first BPM change, use default BPM
        if beat < sorted_changes[0][0]:
            return (beat * 60) / self.default_bpm

        # Find applicable BPM changes
        time = 0
        prev_beat = 0
        prev_bpm = self.default_bpm

        for change_beat, change_bpm in sorted_changes:
            if beat < change_beat:
                # Beat is between previous change and this change
                time += ((beat - prev_beat) * 60) / prev_bpm
                return time

            # Add time from previous change to this change
            time += ((change_beat - prev_beat) * 60) / prev_bpm
            prev_beat = change_beat
            prev_bpm = change_bpm

        # Beat is after all BPM changes
        time += ((beat - prev_beat) * 60) / prev_bpm
        return time

    def _seconds_to_beats(self, seconds: float) -> float:
        """
        Convert seconds to beats based on BPM changes

        Args:
            seconds: Time in seconds

        Returns:
            Beat position
        """
        if not self.bpm_changes:
            # No BPM changes, use default BPM
            return (seconds * self.default_bpm) / 60

        # Sort BPM changes by beat
        sorted_changes = sorted(self.bpm_changes, key=lambda x: x[0])

        # Initialize variables
        remaining_seconds = seconds
        current_beat = 0
        prev_bpm = self.default_bpm
        prev_time = 0

        # Add a sentinel value to make the loop simpler
        time_changes = [(0, 0, self.default_bpm)]  # (beat, seconds, bpm)

        # Convert beat positions to time
        for i, (change_beat, change_bpm) in enumerate(sorted_changes):
            # Calculate time of this change
            change_time = prev_time + (
                (change_beat - time_changes[-1][0]) * 60 / time_changes[-1][2]
            )
            time_changes.append((change_beat, change_time, change_bpm))
            prev_time = change_time

        # Find which BPM segment the time falls into
        for i in range(1, len(time_changes)):
            seg_start_beat, seg_start_time, seg_bpm = time_changes[i - 1]
            seg_end_beat, seg_end_time, _ = time_changes[i]

            if seconds < seg_end_time or i == len(time_changes) - 1:
                # We're in this segment
                elapsed_sec = seconds - seg_start_time
                elapsed_beats = (elapsed_sec * seg_bpm) / 60
                return seg_start_beat + elapsed_beats

        # If we get here, use the last BPM
        elapsed_sec = seconds - time_changes[-1][1]
        elapsed_beats = (elapsed_sec * time_changes[-1][2]) / 60
        return time_changes[-1][0] + elapsed_beats

    def tokenize(
        self, map_data: Union[str, Dict], exclude: Optional[Set[str]] = None
    ) -> List[Dict]:
        """
        Tokenize a Beat Saber map into a sequence of tokens

        Args:
            map_data: JSON string or dictionary containing the map data
            exclude: Set of element types to exclude (e.g. {"colorNotes", "basicBeatmapEvents"})

        Returns:
            List of token dictionaries
        """
        # Parse JSON if string
        if isinstance(map_data, str):
            map_data = json.loads(map_data)

        if isinstance(map_data, tuple):
            map_data = mapconvert.convert(map_data, "3")

        if isinstance(map_data, dict):
            # Likely a map already loaded in a dictionary format,
            # check if it needs to be converted
            # Check map format version and convert if needed
            if "_version" in map_data:  # v2 map format
                map_data = mapconvert.convert(map_data, "3")
            elif "version" in map_data:
                version = str(map_data["version"])
                if not version.startswith("3"):
                    map_data = mapconvert.convert(map_data, "3")
            else:
                raise ValueError("Map data missing version information")

        if isinstance(map_data, list):
            raise ValueError("Map data is likely not v3 or a valid Beat Saber map.")

        exclude = exclude or set()
        tokens = []

        # Store version
        self.version = map_data.get("version", None)

        if self.version is None:
            raise ValueError("Map data is likely not v3 or a valid Beat Saber map.")

        self.version = map_data.get(
            "_version", None
        )  # _version is used in v2 maps, we'll have to convert.

        map_data = mapconvert.convert(map_data, "3")

        # Process BPM events first to set up time conversion
        self._process_bpm_events(map_data)

        # Process each element type if not excluded
        if "bpmEvents" not in exclude and "bpmEvents" in map_data:
            for event in map_data["bpmEvents"]:
                tokens.append(
                    {
                        "type": TokenType.BPM.value,
                        "beat": event["b"],
                        "time": self._beats_to_seconds(event["b"]),
                        "bpm": event["m"],
                        "raw": event,
                    }
                )

        if "rotationEvents" not in exclude and "rotationEvents" in map_data:
            for event in map_data["rotationEvents"]:
                tokens.append(
                    {
                        "type": TokenType.ROTATION.value,
                        "beat": event["b"],
                        "time": self._beats_to_seconds(event["b"]),
                        "execution_type": event["e"],
                        "rotation": event["r"],
                        "raw": event,
                    }
                )

        if "colorNotes" not in exclude and "colorNotes" in map_data:
            for note in map_data["colorNotes"]:
                # Process custom data for color notes
                processed_note = customDataHandler.parse_custom_data(
                    TokenType.COLOR_NOTE, note
                )
                tokens.append(
                    {
                        "type": TokenType.COLOR_NOTE.value,
                        "beat": processed_note["b"],
                        "time": self._beats_to_seconds(processed_note["b"]),
                        "x": processed_note["x"],
                        "y": processed_note["y"],
                        "color": processed_note["c"],
                        "direction": processed_note["d"],
                        "angle_offset": processed_note.get("a", 0),
                        "custom_data": processed_note.get("customData", {}),
                        "raw": note,  # Keep the original data
                    }
                )

        if "bombNotes" not in exclude and "bombNotes" in map_data:
            for bomb in map_data["bombNotes"]:
                # Process custom data for bomb notes
                processed_bomb = customDataHandler.parse_custom_data(
                    TokenType.BOMB_NOTE, bomb
                )
                tokens.append(
                    {
                        "type": TokenType.BOMB_NOTE.value,
                        "beat": processed_bomb["b"],
                        "time": self._beats_to_seconds(processed_bomb["b"]),
                        "x": processed_bomb["x"],
                        "y": processed_bomb["y"],
                        "custom_data": processed_bomb.get("customData", {}),
                        "raw": bomb,  # Keep the original data
                    }
                )

        if "obstacles" not in exclude and "obstacles" in map_data:
            for obstacle in map_data["obstacles"]:
                # Process custom data for obstacles
                processed_obstacle = customDataHandler.parse_custom_data(
                    TokenType.OBSTACLE, obstacle
                )
                tokens.append(
                    {
                        "type": TokenType.OBSTACLE.value,
                        "beat": processed_obstacle["b"],
                        "time": self._beats_to_seconds(processed_obstacle["b"]),
                        "duration": processed_obstacle["d"],
                        "duration_seconds": (processed_obstacle["d"] * 60)
                        / self._get_bpm_at_beat(processed_obstacle["b"]),
                        "x": processed_obstacle["x"],
                        "y": processed_obstacle["y"],
                        "width": processed_obstacle["w"],
                        "height": processed_obstacle["h"],
                        "custom_data": processed_obstacle.get("customData", {}),
                        "raw": obstacle,  # Keep the original data
                    }
                )

        if "sliders" not in exclude and "sliders" in map_data:
            for slider in map_data["sliders"]:
                # Process custom data for sliders
                processed_slider = customDataHandler.parse_custom_data(
                    TokenType.SLIDER, slider
                )
                tokens.append(
                    {
                        "type": TokenType.SLIDER.value,
                        "beat": processed_slider["b"],
                        "time": self._beats_to_seconds(processed_slider["b"]),
                        "x": processed_slider["x"],
                        "y": processed_slider["y"],
                        "color": processed_slider["c"],
                        "direction": processed_slider["d"],
                        "tail_beat": processed_slider["tb"],
                        "tail_time": self._beats_to_seconds(processed_slider["tb"]),
                        "tail_x": processed_slider["tx"],
                        "tail_y": processed_slider["ty"],
                        "custom_data": processed_slider.get("customData", {}),
                        "raw": slider,  # Keep the original data
                    }
                )

        if "burstSliders" not in exclude and "burstSliders" in map_data:
            for burst in map_data["burstSliders"]:
                # Process custom data for burst sliders
                processed_burst = customDataHandler.parse_custom_data(
                    TokenType.BURST_SLIDER, burst
                )
                tokens.append(
                    {
                        "type": TokenType.BURST_SLIDER.value,
                        "beat": processed_burst["b"],
                        "time": self._beats_to_seconds(processed_burst["b"]),
                        "x": processed_burst["x"],
                        "y": processed_burst["y"],
                        "color": processed_burst["c"],
                        "direction": processed_burst["d"],
                        "tail_beat": processed_burst["tb"],
                        "tail_time": self._beats_to_seconds(processed_burst["tb"]),
                        "tail_x": processed_burst["tx"],
                        "tail_y": processed_burst["ty"],
                        "slice_count": processed_burst["sc"],
                        "squish": processed_burst["s"],
                        "custom_data": processed_burst.get("customData", {}),
                        "raw": burst,  # Keep the original data
                    }
                )

        if "basicBeatmapEvents" not in exclude and "basicBeatmapEvents" in map_data:
            for event in map_data["basicBeatmapEvents"]:
                # Process custom data for basic events
                processed_event = customDataHandler.parse_custom_data(
                    TokenType.BASIC_EVENT, event
                )
                tokens.append(
                    {
                        "type": TokenType.BASIC_EVENT.value,
                        "beat": processed_event.get("b", event.get("b", 0)),
                        "time": self._beats_to_seconds(
                            processed_event.get("b", event.get("b", 0))
                        ),
                        "event_type": processed_event.get("et", event.get("et", 0)),
                        "value": processed_event.get("v", event.get("v", 0)),
                        "float_value": processed_event.get("f", 1),
                        "custom_data": processed_event.get(
                            "customData", event.get("customData", {})
                        ),
                        "raw": event,  # Keep the original data
                    }
                )

        # Add other element types processing (waypoints, etc.)
        # Sort all tokens by beat/time for consistency
        tokens.sort(key=lambda x: x["beat"])
        return tokens

    def _process_bpm_events(self, map_data: Dict) -> None:
        """
        Process BPM events to build the BPM changes list

        Args:
            map_data: Map data dictionary
        """
        self.bpm_changes = []
        if "bpmEvents" in map_data:
            for event in map_data["bpmEvents"]:
                self.bpm_changes.append((event["b"], event["m"]))

        # Ensure there's at least one BPM entry
        if not self.bpm_changes:
            self.bpm_changes.append((0, self.default_bpm))

    def _get_bpm_at_beat(self, beat: float) -> float:
        """
        Get the BPM at a specific beat

        Args:
            beat: Beat position

        Returns:
            BPM at that beat
        """
        if not self.bpm_changes:
            return self.default_bpm

        # Sort BPM changes by beat
        sorted_changes = sorted(self.bpm_changes, key=lambda x: x[0])

        # Find the last BPM change before or at this beat
        current_bpm = self.default_bpm
        for change_beat, change_bpm in sorted_changes:
            if beat < change_beat:
                break
            current_bpm = change_bpm

        return current_bpm

    def detokenize(self, tokens: List[Dict], target_version="3") -> Dict:
        """
        Convert tokens back into a Beat Saber map

        Args:
            tokens: List of token dictionaries
            target_version: Target version to convert to

        Returns:
            Map data dictionary
        """
        map_data = {"version": self.version or "3.3.0"}

        # Group tokens by type
        token_groups = {}
        for token in tokens:
            token_type = token["type"]
            if token_type not in token_groups:
                token_groups[token_type] = []
            token_groups[token_type].append(token)

        # Convert tokens back to map elements
        if TokenType.BPM.value in token_groups:
            map_data["bpmEvents"] = [
                {"b": token["beat"], "m": token["bpm"]}
                for token in token_groups[TokenType.BPM.value]
            ]

        if TokenType.COLOR_NOTE.value in token_groups:
            map_data["colorNotes"] = []
            for token in token_groups[TokenType.COLOR_NOTE.value]:
                note = {
                    "b": token["beat"],
                    "x": token["x"],
                    "y": token["y"],
                    "c": token["color"],
                    "d": token["direction"],
                    "a": token["angle_offset"],
                }
                # Add custom data if it exists
                if token.get("custom_data") and len(token["custom_data"]) > 0:
                    note["customData"] = token["custom_data"]
                map_data["colorNotes"].append(note)

        if TokenType.BOMB_NOTE.value in token_groups:
            map_data["bombNotes"] = []
            for token in token_groups[TokenType.BOMB_NOTE.value]:
                bomb = {"b": token["beat"], "x": token["x"], "y": token["y"]}
                # Add custom data if it exists
                if token.get("custom_data") and len(token["custom_data"]) > 0:
                    bomb["customData"] = token["custom_data"]
                map_data["bombNotes"].append(bomb)

        if TokenType.OBSTACLE.value in token_groups:
            map_data["obstacles"] = []
            for token in token_groups[TokenType.OBSTACLE.value]:
                obstacle = {
                    "b": token["beat"],
                    "d": token["duration"],
                    "x": token["x"],
                    "y": token["y"],
                    "w": token["width"],
                    "h": token["height"],
                }
                # Add custom data if it exists
                if token.get("custom_data") and len(token["custom_data"]) > 0:
                    obstacle["customData"] = token["custom_data"]
                map_data["obstacles"].append(obstacle)

        if TokenType.SLIDER.value in token_groups:
            map_data["sliders"] = []
            for token in token_groups[TokenType.SLIDER.value]:
                slider = {
                    "b": token["beat"],
                    "x": token["x"],
                    "y": token["y"],
                    "c": token["color"],
                    "d": token["direction"],
                    "tb": token["tail_beat"],
                    "tx": token["tail_x"],
                    "ty": token["tail_y"],
                }
                # Add custom data if it exists
                if token.get("custom_data") and len(token["custom_data"]) > 0:
                    slider["customData"] = token["custom_data"]
                map_data["sliders"].append(slider)

        if TokenType.BURST_SLIDER.value in token_groups:
            map_data["burstSliders"] = []
            for token in token_groups[TokenType.BURST_SLIDER.value]:
                burst = {
                    "b": token["beat"],
                    "x": token["x"],
                    "y": token["y"],
                    "c": token["color"],
                    "d": token["direction"],
                    "tb": token["tail_beat"],
                    "tx": token["tail_x"],
                    "ty": token["tail_y"],
                    "sc": token["slice_count"],
                    "s": token["squish"],
                }
                # Add custom data if it exists
                if token.get("custom_data") and len(token["custom_data"]) > 0:
                    burst["customData"] = token["custom_data"]
                map_data["burstSliders"].append(burst)

        if TokenType.BASIC_EVENT.value in token_groups:
            map_data["basicBeatmapEvents"] = []
            for token in token_groups[TokenType.BASIC_EVENT.value]:
                event = {
                    "b": token["beat"],
                    "et": token["event_type"],
                    "v": token["value"],
                    "f": token["float_value"],
                }
                # Add custom data if it exists
                if token.get("custom_data") and len(token["custom_data"]) > 0:
                    event["customData"] = token["custom_data"]
                map_data["basicBeatmapEvents"].append(event)

        # Convert to target version if necessary
        if target_version != "3":
            map_data = mapconvert.convert(map_data, target_version)

        return map_data
