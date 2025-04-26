import io
from typing import Dict, List, Union, Optional, Set, BinaryIO, Any
from bsor.Bsor import Bsor, make_bsor, VRObject, Info, Frame, Note, Wall, Height, Pause, ControllerOffsets, UserData
from bsor.Bsor import lookup_dict_scoring_type, lookup_dict_event_type, MAGIC_HEX
from bstokenizer import ReplayTokenType as TokenType

class BeatSaberReplayTokenizer:
    """Tokenizer for Beat Saber replays (BSOR format)"""
    
    def __init__(self):
        """Initialize the tokenizer"""
        pass
    
    def tokenize(self, replay_data: Union[Bsor, bytes, BinaryIO, str], exclude: Optional[Set[str]] = None) -> List[Dict]:
        """
        Tokenize a Beat Saber replay into a sequence of tokens
        
        Args:
            replay_data: BSOR object, binary data, file path, or file-like object with replay data
            exclude: Set of element types to exclude
        
        Returns:
            List of token dictionaries
        """
        # Handle different input types
        bsor_data = None
        if isinstance(replay_data, Bsor):
            bsor_data = replay_data
        elif isinstance(replay_data, bytes):
            bsor_data = make_bsor(io.BytesIO(replay_data))
        elif isinstance(replay_data, str):
            with open(replay_data, 'rb') as f:
                bsor_data = make_bsor(f)
        elif hasattr(replay_data, 'read'):  # File-like object
            bsor_data = make_bsor(replay_data)
        else:
            raise ValueError("Unsupported replay_data type")
        
        exclude = exclude or set()
        tokens = []
        
        # Process info
        if "info" not in exclude:
            info_token = self._process_info(bsor_data.info)
            tokens.append(info_token)
        
        # Process frames
        if "frames" not in exclude:
            for frame in bsor_data.frames:
                frame_token = self._process_frame(frame)
                tokens.append(frame_token)
        
        # Process notes
        if "notes" not in exclude:
            for note in bsor_data.notes:
                note_token = self._process_note(note)
                tokens.append(note_token)
        
        # Process walls
        if "walls" not in exclude:
            for wall in bsor_data.walls:
                wall_token = self._process_wall(wall)
                tokens.append(wall_token)
        
        # Process heights
        if "heights" not in exclude:
            for height in bsor_data.heights:
                height_token = self._process_height(height)
                tokens.append(height_token)
        
        # Process pauses
        if "pauses" not in exclude:
            for pause in bsor_data.pauses:
                pause_token = self._process_pause(pause)
                tokens.append(pause_token)
        
        # Process controller offsets
        if "controller_offsets" not in exclude and bsor_data.controller_offsets:
            if not isinstance(bsor_data.controller_offsets, list):  # Handle different types based on Bsor implementation
                controller_token = self._process_controller_offset(bsor_data.controller_offsets)
                tokens.append(controller_token)
        
        # Process user data
        if "user_data" not in exclude and bsor_data.user_data:
            for user_data in bsor_data.user_data:
                user_data_token = self._process_user_data(user_data)
                tokens.append(user_data_token)
        
        # Sort tokens by time for consistency
        # Not all tokens have time, so we need to be careful
        tokens_with_time = [t for t in tokens if "time" in t]
        tokens_without_time = [t for t in tokens if "time" not in t]
        
        tokens_with_time.sort(key=lambda x: x["time"])
        
        # Combine the sorted tokens with time and tokens without time
        sorted_tokens = tokens_without_time + tokens_with_time
        
        return sorted_tokens
    
    def _process_info(self, info: Info) -> Dict:
        """
        Process Info object into a token
        
        Args:
            info: Info object
        
        Returns:
            Token dictionary
        """
        return {
            "type": TokenType.INFO.value,
            "version": info.version,
            "gameVersion": info.gameVersion,
            "timestamp": info.timestamp,
            "playerId": info.playerId,
            "playerName": info.playerName,
            "platform": info.platform,
            "trackingSystem": info.trackingSystem,
            "hmd": info.hmd,
            "controller": info.controller,
            "songHash": info.songHash,
            "songName": info.songName,
            "mapper": info.mapper,
            "difficulty": info.difficulty,
            "score": info.score,
            "mode": info.mode,
            "environment": info.environment,
            "modifiers": info.modifiers,
            "jumpDistance": info.jumpDistance,
            "leftHanded": info.leftHanded,
            "height": info.height,
            "startTime": info.startTime,
            "failTime": info.failTime,
            "speed": info.speed,
            "raw": info  # Keep the original object
        }
    
    def _process_vr_object(self, vr_obj: VRObject) -> Dict:
        """
        Process VRObject into a dictionary
        
        Args:
            vr_obj: VRObject
        
        Returns:
            Dictionary with position and rotation
        """
        return {
            "position": {
                "x": vr_obj.x,
                "y": vr_obj.y,
                "z": vr_obj.z
            },
            "rotation": {
                "x": vr_obj.x_rot,
                "y": vr_obj.y_rot,
                "z": vr_obj.z_rot,
                "w": vr_obj.w_rot
            }
        }
    
    def _process_frame(self, frame: Frame) -> Dict:
        """
        Process Frame object into a token
        
        Args:
            frame: Frame object
        
        Returns:
            Token dictionary
        """
        return {
            "type": TokenType.FRAME.value,
            "time": frame.time,
            "fps": frame.fps,
            "head": self._process_vr_object(frame.head),
            "left_hand": self._process_vr_object(frame.left_hand),
            "right_hand": self._process_vr_object(frame.right_hand),
            "raw": frame  # Keep the original object
        }
    
    def _process_note(self, note: Note) -> Dict:
        """
        Process Note object into a token
        
        Args:
            note: Note object
        
        Returns:
            Token dictionary
        """
        token = {
            "type": TokenType.NOTE.value,
            "time": note.event_time,
            "spawn_time": note.spawn_time,
            "note_id": note.note_id,
            "scoringType": note.scoringType,
            "scoringTypeName": lookup_dict_scoring_type.get(note.scoringType, "Unknown"),
            "lineIndex": note.lineIndex,
            "noteLineLayer": note.noteLineLayer,
            "colorType": note.colorType,
            "cutDirection": note.cutDirection,
            "event_type": note.event_type,
            "event_type_name": lookup_dict_event_type.get(note.event_type, "Unknown"),
            "score": note.score,
            "raw": note  # Keep the original object
        }
        
        if note.cut:  # Only present for good and bad cuts
            token["cut"] = {
                "speedOK": note.cut.speedOK,
                "directionOk": note.cut.directionOk,
                "saberTypeOk": note.cut.saberTypeOk,
                "wasCutTooSoon": note.cut.wasCutTooSoon,
                "saberSpeed": note.cut.saberSpeed,
                "saberDirection": note.cut.saberDirection,
                "saberType": note.cut.saberType,
                "timeDeviation": note.cut.timeDeviation,
                "cutDeviation": note.cut.cutDeviation,
                "cutPoint": note.cut.cutPoint,
                "cutNormal": note.cut.cutNormal,
                "cutDistanceToCenter": note.cut.cutDistanceToCenter,
                "cutAngle": note.cut.cutAngle,
                "beforeCutRating": note.cut.beforeCutRating,
                "afterCutRating": note.cut.afterCutRating
            }
            token["pre_score"] = note.pre_score
            token["post_score"] = note.post_score
            token["acc_score"] = note.acc_score
        
        return token
    
    def _process_wall(self, wall: Wall) -> Dict:
        """
        Process Wall object into a token
        
        Args:
            wall: Wall object
        
        Returns:
            Token dictionary
        """
        return {
            "type": TokenType.WALL.value,
            "time": wall.time,
            "id": wall.id,
            "energy": wall.energy,
            "spawn_time": wall.spawnTime,
            "raw": wall  # Keep the original object
        }
    
    def _process_height(self, height: Height) -> Dict:
        """
        Process Height object into a token
        
        Args:
            height: Height object
        
        Returns:
            Token dictionary
        """
        return {
            "type": TokenType.HEIGHT.value,
            "time": height.time,
            "height": height.height,
            "raw": height  # Keep the original object
        }
    
    def _process_pause(self, pause: Pause) -> Dict:
        """
        Process Pause object into a token
        
        Args:
            pause: Pause object
        
        Returns:
            Token dictionary
        """
        return {
            "type": TokenType.PAUSE.value,
            "time": pause.time,
            "duration": pause.duration,
            "raw": pause  # Keep the original object
        }
    
    def _process_controller_offset(self, controller_offset: ControllerOffsets) -> Dict:
        """
        Process ControllerOffsets object into a token
        
        Args:
            controller_offset: ControllerOffsets object
        
        Returns:
            Token dictionary
        """
        return {
            "type": TokenType.CONTROLLER_OFFSET.value,
            "left": self._process_vr_object(controller_offset.left),
            "right": self._process_vr_object(controller_offset.right),
            "raw": controller_offset  # Keep the original object
        }
    
    def _process_user_data(self, user_data: UserData) -> Dict:
        """
        Process UserData object into a token
        
        Args:
            user_data: UserData object
        
        Returns:
            Token dictionary
        """
        return {
            "type": TokenType.USER_DATA.value,
            "key": user_data.key,
            "bytes": user_data.bytes,
            "raw": user_data  # Keep the original object
        }
    
    def detokenize(self, tokens: List[Dict]) -> Bsor:
        """
        Convert tokens back into a Beat Saber replay
        
        Args:
            tokens: List of token dictionaries
        
        Returns:
            BSOR object
        """
        # Group tokens by type
        token_groups = {}
        for token in tokens:
            token_type = token["type"]
            if token_type not in token_groups:
                token_groups[token_type] = []
            token_groups[token_type].append(token)
        
        # Create a new BSOR object
        bsor = Bsor()
        
        # Set magic number and file version
        bsor.magic_number = int(MAGIC_HEX, 16)
        bsor.file_version = 1
        
        # Process info tokens (should be only one)
        if TokenType.INFO.value in token_groups:
            info_token = token_groups[TokenType.INFO.value][0]
            
            # If the raw info object is available, use it
            if "raw" in info_token and isinstance(info_token["raw"], Info):
                bsor.info = info_token["raw"]
            else:
                # Otherwise create a new Info object
                info = Info()
                info.version = info_token.get("version", "")
                info.gameVersion = info_token.get("gameVersion", "")
                info.timestamp = info_token.get("timestamp", "")
                info.playerId = info_token.get("playerId", "")
                info.playerName = info_token.get("playerName", "")
                info.platform = info_token.get("platform", "")
                info.trackingSystem = info_token.get("trackingSystem", "")
                info.hmd = info_token.get("hmd", "")
                info.controller = info_token.get("controller", "")
                info.songHash = info_token.get("songHash", "")
                info.songName = info_token.get("songName", "")
                info.mapper = info_token.get("mapper", "")
                info.difficulty = info_token.get("difficulty", "")
                info.score = info_token.get("score", 0)
                info.mode = info_token.get("mode", "")
                info.environment = info_token.get("environment", "")
                info.modifiers = info_token.get("modifiers", "")
                info.jumpDistance = info_token.get("jumpDistance", 0.0)
                info.leftHanded = info_token.get("leftHanded", False)
                info.height = info_token.get("height", 0.0)
                info.startTime = info_token.get("startTime", 0.0)
                info.failTime = info_token.get("failTime", 0.0)
                info.speed = info_token.get("speed", 1.0)
                bsor.info = info
        
        # Process frame tokens
        bsor.frames = []
        if TokenType.FRAME.value in token_groups:
            for token in token_groups[TokenType.FRAME.value]:
                if "raw" in token and isinstance(token["raw"], Frame):
                    bsor.frames.append(token["raw"])
                else:
                    frame = Frame()
                    frame.time = token.get("time", 0.0)
                    frame.fps = token.get("fps", 0)
                    
                    head = self._create_vr_object(token.get("head", {}))
                    left_hand = self._create_vr_object(token.get("left_hand", {}))
                    right_hand = self._create_vr_object(token.get("right_hand", {}))
                    
                    frame.head = head
                    frame.left_hand = left_hand
                    frame.right_hand = right_hand
                    
                    bsor.frames.append(frame)
        
        # Process note tokens
        bsor.notes = []
        if TokenType.NOTE.value in token_groups:
            for token in token_groups[TokenType.NOTE.value]:
                if "raw" in token and isinstance(token["raw"], Note):
                    bsor.notes.append(token["raw"])
                else:
                    # This would need complete note reconstruction
                    # For now, we'll assume raw objects are preserved
                    pass
        
        # Process wall tokens
        bsor.walls = []
        if TokenType.WALL.value in token_groups:
            for token in token_groups[TokenType.WALL.value]:
                if "raw" in token and isinstance(token["raw"], Wall):
                    bsor.walls.append(token["raw"])
                else:
                    wall = Wall()
                    wall.id = token.get("id", 0)
                    wall.energy = token.get("energy", 0.0)
                    wall.time = token.get("time", 0.0)
                    wall.spawnTime = token.get("spawn_time", 0.0)
                    bsor.walls.append(wall)
        
        # Process height tokens
        bsor.heights = []
        if TokenType.HEIGHT.value in token_groups:
            for token in token_groups[TokenType.HEIGHT.value]:
                if "raw" in token and isinstance(token["raw"], Height):
                    bsor.heights.append(token["raw"])
                else:
                    height = Height()
                    height.height = token.get("height", 0.0)
                    height.time = token.get("time", 0.0)
                    bsor.heights.append(height)
        
        # Process pause tokens
        bsor.pauses = []
        if TokenType.PAUSE.value in token_groups:
            for token in token_groups[TokenType.PAUSE.value]:
                if "raw" in token and isinstance(token["raw"], Pause):
                    bsor.pauses.append(token["raw"])
                else:
                    pause = Pause()
                    pause.duration = token.get("duration", 0)
                    pause.time = token.get("time", 0.0)
                    bsor.pauses.append(pause)
        
        # Process controller offset tokens
        if TokenType.CONTROLLER_OFFSET.value in token_groups:
            token = token_groups[TokenType.CONTROLLER_OFFSET.value][0]  # Should only be one
            if "raw" in token and isinstance(token["raw"], ControllerOffsets):
                bsor.controller_offsets = token["raw"]
            else:
                controller_offsets = ControllerOffsets()
                controller_offsets.left = self._create_vr_object(token.get("left", {}))
                controller_offsets.right = self._create_vr_object(token.get("right", {}))
                bsor.controller_offsets = controller_offsets
        
        # Process user data tokens
        bsor.user_data = []
        if TokenType.USER_DATA.value in token_groups:
            for token in token_groups[TokenType.USER_DATA.value]:
                if "raw" in token and isinstance(token["raw"], UserData):
                    bsor.user_data.append(token["raw"])
                else:
                    user_data = UserData()
                    user_data.key = token.get("key", "")
                    user_data.bytes = token.get("bytes", [])
                    bsor.user_data.append(user_data)
        
        return bsor
    
    def _create_vr_object(self, data: Dict[str, Any]) -> VRObject:
        """
        Create a VRObject from dictionary data
        
        Args:
            data: Dictionary with position and rotation data
            
        Returns:
            VRObject
        """
        vr_obj = VRObject()
        
        position = data.get("position", {})
        rotation = data.get("rotation", {})
        
        vr_obj.x = position.get("x", 0.0)
        vr_obj.y = position.get("y", 0.0)
        vr_obj.z = position.get("z", 0.0)
        
        vr_obj.x_rot = rotation.get("x", 0.0)
        vr_obj.y_rot = rotation.get("y", 0.0)
        vr_obj.z_rot = rotation.get("z", 0.0)
        vr_obj.w_rot = rotation.get("w", 1.0)
        
        return vr_obj