from src.parser.satisfactory.types.structs.md5_hash import MD5Hash

class ModData:
    def __init__(self, Reference: str, Name: str, Version: str):
        self.Reference = Reference
        self.Name = Name
        self.Version = Version

class SatisfactoryModMetadata:
    def __init__(self, Version: int, FullMapName: str, Mods: list[ModData]):
        self.Version = Version
        self.FullMapName = FullMapName
        self.Mods = Mods

class SatisfactorySaveHeader:
    def __init__(self, saveHeaderType: int, saveVersion: int, buildVersion: int, mapName: str, mapOptions: str, sessionName: str, playDurationSeconds: int, saveDateTime: str, sessionVisibility: int, rawModMetadataString: str = None, modMetadata: SatisfactoryModMetadata = None, isModdedSave: int = None, saveIdentifier: str = None, fEditorObjectVersion: int = None, partitionEnabledFlag: bool = None, consistencyHashBytes: MD5Hash = None, creativeModeEnabled: bool = None):
        self.saveHeaderType = saveHeaderType
        self.saveVersion = saveVersion
        self.buildVersion = buildVersion
        self.mapName = mapName
        self.mapOptions = mapOptions
        self.sessionName = sessionName
        self.playDurationSeconds = playDurationSeconds
        self.saveDateTime = saveDateTime
        self.sessionVisibility = sessionVisibility
        self.rawModMetadataString = rawModMetadataString
        self.modMetadata = modMetadata
        self.isModdedSave = isModdedSave
        self.saveIdentifier = saveIdentifier
        self.fEditorObjectVersion = fEditorObjectVersion
        self.partitionEnabledFlag = partitionEnabledFlag
        self.consistencyHashBytes = consistencyHashBytes
        self.creativeModeEnabled = creativeModeEnabled

RoughSaveVersion = ['<U6', 'U6/U7', 'U8', 'U1.0+']
