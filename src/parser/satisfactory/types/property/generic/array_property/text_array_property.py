from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.property.generic.text_property import TextProperty, TextPropertyValue

class TextArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[TextPropertyValue], ue_type: str = 'TextArrayProperty', index: int = 0):
        super().__init__('TextArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [TextProperty.read_value(reader) for _ in range(element_count)]
        return TextArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer, property):
        for value in property.values:
            TextProperty.serialize_value(writer, value)
