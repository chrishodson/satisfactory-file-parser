from src.parser.satisfactory.types.structs.GUIDInfo import GUIDInfo


class AbstractBaseProperty:
    def __init__(self, type: str, ue_type: str, name: str = '', guid_info: GUIDInfo = None, index: int = 0):
        self.type = type
        self.ue_type = ue_type
        self.name = name
        self.guid_info = guid_info
        self.index = index


class PropertiesMap(dict):
    def __setitem__(self, key: str, value: AbstractBaseProperty):
        if not isinstance(value, AbstractBaseProperty):
            raise TypeError("Value must be an instance of AbstractBaseProperty")
        super().__setitem__(key, value)
