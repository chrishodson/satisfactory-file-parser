from parser.satisfactory.types.structs.guid_info import GUIDInfo
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

def is_text_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'TextProperty'

class TextProperty(AbstractBaseProperty):

    def __init__(self, value: 'TextPropertyValue', ue_type: str = 'TextProperty', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('TextProperty', ue_type, guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader: 'BinaryReadable', ue_type: str, index: int = 0) -> 'TextProperty':
        guid_info = GUIDInfo.read(reader)
        value = TextProperty.read_value(reader)
        return TextProperty(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: 'BinaryReadable') -> 'TextPropertyValue':
        prop = {
            'flags': reader.read_int32(),
            'history_type': reader.read_byte()
        }

        if prop['history_type'] == 0:
            prop['namespace'] = reader.read_string()
            prop['key'] = reader.read_string()
            prop['value'] = reader.read_string()
        elif prop['history_type'] in [1, 3]:
            prop['source_fmt'] = TextProperty.read_value(reader)
            arguments_count = reader.read_int32()
            prop['arguments'] = []

            for _ in range(arguments_count):
                current_arguments_data = {
                    'name': reader.read_string(),
                    'value_type': reader.read_byte()
                }

                if current_arguments_data['value_type'] == 4:
                    current_arguments_data['argument_value'] = TextProperty.read_value(reader)
                else:
                    raise ValueError(f"Unimplemented FormatArgumentType `{current_arguments_data['value_type']}`")

                prop['arguments'].append(current_arguments_data)
        elif prop['history_type'] == 10:
            prop['source_text'] = TextProperty.read_value(reader)
            prop['transform_type'] = reader.read_byte()
        elif prop['history_type'] == 255:
            prop['has_culture_invariant_string'] = reader.read_int32() == 1
            if prop['has_culture_invariant_string']:
                prop['value'] = reader.read_string()
        else:
            raise ValueError(f"Unimplemented historyType `{prop['history_type']}`")

        return prop

    @staticmethod
    def calc_overhead(property: 'TextProperty') -> int:
        return 1

    @staticmethod
    def serialize(writer: 'ByteWriter', property: 'TextProperty') -> None:
        GUIDInfo.write(writer, property.guid_info)
        TextProperty.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: 'ByteWriter', value: 'TextPropertyValue') -> None:
        writer.write_int32(value['flags'])
        writer.write_byte(value['history_type'])

        if value['history_type'] == 0:
            writer.write_string(value['namespace'])
            writer.write_string(value['key'])
            writer.write_string(value['value'])
        elif value['history_type'] in [1, 3]:
            TextProperty.serialize_value(writer, value['source_fmt'])
            writer.write_int32(len(value['arguments']))

            for arg in value['arguments']:
                writer.write_string(arg['name'])
                writer.write_byte(arg['value_type'])

                if arg['value_type'] == 4:
                    TextProperty.serialize_value(writer, arg['argument_value'])
                else:
                    raise ValueError(f"Unimplemented FormatArgumentType `{arg['value_type']}`")
        elif value['history_type'] == 10:
            TextProperty.serialize_value(writer, value['source_text'])
            writer.write_byte(value['transform_type'])
        elif value['history_type'] == 255:
            writer.write_int32(1 if value['has_culture_invariant_string'] else 0)
            if value['has_culture_invariant_string']:
                writer.write_string(value['value'])
        else:
            raise ValueError(f"Unimplemented historyType `{value['history_type']}`")

class TextPropertyValue:
    def __init__(self, flags: int, history_type: int, namespace: str = None, key: str = None, value: str = None,
                 source_fmt: 'TextPropertyValue' = None, arguments: list = None, source_text: 'TextPropertyValue' = None,
                 transform_type: int = None, has_culture_invariant_string: bool = None):
        self.flags = flags
        self.history_type = history_type
        self.namespace = namespace
        self.key = key
        self.value = value
        self.source_fmt = source_fmt
        self.arguments = arguments
        self.source_text = source_text
        self.transform_type = transform_type
        self.has_culture_invariant_string = has_culture_invariant_string
