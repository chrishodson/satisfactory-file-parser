from src.parser.file_types import ChunkCompressionInfo
from src.parser.satisfactory.types.objects.save_component import SaveComponent
from src.parser.satisfactory.types.objects.save_entity import SaveEntity
from src.parser.satisfactory.types.structs.col4 import col4
from src.parser.satisfactory.types.structs.object_reference import ObjectReference
from src.parser.satisfactory.types.structs.vec3 import vec3

class BlueprintConfig:
    def __init__(self, description: str, color: col4, iconID: int, referencedIconLibrary: str = None, iconLibraryType: str = None):
        self.description = description
        self.color = color
        self.iconID = iconID
        self.referencedIconLibrary = referencedIconLibrary
        self.iconLibraryType = iconLibraryType

class BlueprintHeader:
    def __init__(self, designerDimension: vec3 = None, itemCosts: list = None, recipeReferences: list = None):
        self.designerDimension = designerDimension
        self.itemCosts = itemCosts if itemCosts is not None else []
        self.recipeReferences = recipeReferences if recipeReferences is not None else []

class Blueprint:
    def __init__(self, name: str, compressionInfo: ChunkCompressionInfo, header: BlueprintHeader, config: BlueprintConfig, objects: list):
        self.name = name
        self.compressionInfo = compressionInfo
        self.header = header
        self.config = config
        self.objects = objects
