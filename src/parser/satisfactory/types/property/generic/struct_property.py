from parser.satisfactory.types.structs.col4 import col4
from parser.satisfactory.types.structs.vec3 import vec3
from parser.satisfactory.types.structs.vec4 import vec4
from parser.satisfactory.types.structs.guid_info import GUIDInfo
from parser.satisfactory.types.structs.mods.FicsItCam.FICFrameRange import FICFrameRange
from parser.satisfactory.types.structs.dynamic_struct_property_value import DynamicStructPropertyValue
from parser.satisfactory.types.error.parser_error import CorruptSaveError
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.byte.binary_readable_interface import BinaryReadable
from parser.satisfactory.types.byte.byte_writer import ByteWriter


class BasicMultipleStructPropertyValue:
    def __init__(self, values: dict):
        self.values = values


class BasicStructPropertyValue:
    def __init__(self, value: any):
        self.value = value


class BoxStructPropertyValue:
    def __init__(self, min: vec3, max: vec3, is_valid: bool):
        self.min = min
        self.max = max
        self.is_valid = is_valid


class RailroadTrackPositionStructPropertyValue:
    def __init__(self, root: str, instance_name: str, offset: float, forward: float):
        self.root = root
        self.instance_name = instance_name
        self.offset = offset
        self.forward = forward


class InventoryItemStructPropertyValue:
    def __init__(self, unk1: int, item_name: str, has_item_state: int, item_state: dict = None):
        self.unk1 = unk1
        self.item_name = item_name
        self.has_item_state = has_item_state
        self.item_state = item_state


class FICFrameRangeStructPropertyValue:
    def __init__(self, begin: str, end: str):
        self.begin = begin
        self.end = end


class ClientIdentityInfo:
    def __init__(self, offline_id: str, account_ids: dict):
        self.offline_id = offline_id
        self.account_ids = account_ids


GENERIC_STRUCT_PROPERTY_VALUE = (BasicMultipleStructPropertyValue, BasicStructPropertyValue, BoxStructPropertyValue, 
                                 RailroadTrackPositionStructPropertyValue, InventoryItemStructPropertyValue, 
                                 FICFrameRangeStructPropertyValue, ClientIdentityInfo, DynamicStructPropertyValue, 
                                 col4, vec3, vec4, str)


class StructProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, ue_type: str = 'StructProperty', index: int = 0, guid_info: GUIDInfo = None):
        super().__init__('StructProperty', ue_type, '', guid_info, index)
        self.subtype = subtype
        self.value = BasicMultipleStructPropertyValue({})
        self.unk1 = None
        self.unk2 = None
        self.unk3 = None
        self.unk4 = None

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int, size: int):
        struct = StructProperty(
            reader.read_string(),
            ue_type,
            index,
            GUIDInfo.read(reader)
        )

        unk1 = reader.read_int32()
        if unk1 != 0:
            struct.unk1 = unk1

        unk2 = reader.read_int32()
        if unk2 != 0:
            struct.unk2 = unk2

        unk3 = reader.read_int32()
        if unk3 != 0:
            struct.unk3 = unk3

        unk4 = reader.read_int32()
        if unk4 != 0:
            struct.unk4 = unk4

        before = reader.get_buffer_position()
        struct.value = StructProperty.parse_value(reader, struct.subtype, size)
        read_bytes = reader.get_buffer_position() - before
        if read_bytes != size:
            if size - read_bytes == 4:
                reader.skip_bytes(size - read_bytes)
            else:
                raise CorruptSaveError(f"possibly corrupt. Read {read_bytes} for StructProperty Content of {struct.subtype}, but {size} were indicated.")

        return struct

    @staticmethod
    def parse_value(reader: BinaryReadable, subtype: str, size: int):
        if subtype == 'Color':
            return col4.parse_bgra(reader)
        elif subtype == 'IntPoint':
            return str(reader.read_int64())
        elif subtype == 'LinearColor':
            return col4.parse_rgba(reader)
        elif subtype in ['Vector', 'Rotator', 'Vector2D']:
            return vec3.parse_f(reader) if size == 12 else vec3.parse(reader)
        elif subtype in ['Quat', 'Vector4', 'Vector4D']:
            return vec4.parse_f(reader) if size == 16 else vec4.parse(reader)
        elif subtype == 'Box':
            return BoxStructPropertyValue(
                min=vec3.parse_f(reader) if size == 25 else vec3.parse(reader),
                max=vec3.parse_f(reader) if size == 25 else vec3.parse(reader),
                is_valid=reader.read_byte() >= 1
            )
        elif subtype == 'RailroadTrackPosition':
            return RailroadTrackPositionStructPropertyValue(
                root=reader.read_string(),
                instance_name=reader.read_string(),
                offset=reader.read_float32(),
                forward=reader.read_float32()
            )
        elif subtype == 'TimerHandle':
            return reader.read_string()
        elif subtype == 'Guid':
            return reader.read_string()
        elif subtype == 'ClientIdentityInfo':
            offline_id = reader.read_string()
            num_account_ids = reader.read_int32()
            account_ids = {}
            for _ in range(num_account_ids):
                platform_flag_maybe = reader.read_byte()
                id_size = reader.read_int32()
                account_id = list(reader.read_bytes(id_size))
                account_ids[platform_flag_maybe] = account_id
            return ClientIdentityInfo(offline_id, account_ids)
        elif subtype == 'InventoryItem':
            before = reader.get_buffer_position()
            value = InventoryItemStructPropertyValue(
                unk1=reader.read_int32(),
                item_name=reader.read_string(),
                has_item_state=reader.read_int32()
            )
            if value.has_item_state >= 1:
                value.item_state = {
                    'unk': reader.read_int32(),
                    'path_name': reader.read_string(),
                    'binary_size': reader.read_int32(),
                    'item_state_raw': list(reader.read_bytes(value.item_state['binary_size']))
                }
            bytes_left = size - (reader.get_buffer_position() - before)
            if bytes_left != 0 and (bytes_left != 4 or reader.read_int32() != 0):
                raise CorruptSaveError("save may be corrupt. InventoryItem has weird format that was not seen so far and therefore not implemented. Could be that the save is ported from way before U8.")
            return value
        elif subtype == 'FluidBox':
            return BasicStructPropertyValue(reader.read_float32())
        elif subtype == 'SlateBrush':
            return reader.read_string()
        elif subtype == 'DateTime':
            return str(reader.read_int64())
        elif subtype == 'FICFrameRange':
            return FICFrameRange.parse(reader)
        else:
            return DynamicStructPropertyValue.read(reader, 0, subtype)

    @staticmethod
    def calc_overhead(property):
        return len(property.subtype) + 5 + 4 + 4 + 4 + 4 + 1

    @staticmethod
    def serialize(writer: ByteWriter, property):
        writer.write_string(property.subtype)
        GUIDInfo.write(writer, property.guid_info)
        writer.write_int32(property.unk1 or 0)
        writer.write_int32(property.unk2 or 0)
        writer.write_int32(property.unk3 or 0)
        writer.write_int32(property.unk4 or 0)
        StructProperty.serialize_value(writer, property.subtype, property.value)

    @staticmethod
    def serialize_value(writer: ByteWriter, subtype: str, value):
        if subtype == 'Color':
            col4.serialize_bgra(writer, value)
        elif subtype == 'IntPoint':
            writer.write_int64(int(value))
        elif subtype == 'LinearColor':
            col4.serialize_rgba(writer, value)
        elif subtype in ['Vector', 'Rotator', 'Vector2D']:
            vec3.serialize(writer, value)
        elif subtype in ['Quat', 'Vector4', 'Vector4D']:
            vec4.serialize(writer, value)
        elif subtype == 'Box':
            vec3.serialize(writer, value.min)
            vec3.serialize(writer, value.max)
            writer.write_byte(1 if value.is_valid else 0)
        elif subtype == 'RailroadTrackPosition':
            writer.write_string(value.root)
            writer.write_string(value.instance_name)
            writer.write_float32(value.offset)
            writer.write_float32(value.forward)
        elif subtype == 'TimerHandle':
            writer.write_string(value)
        elif subtype == 'Guid':
            writer.write_string(value)
        elif subtype == 'ClientIdentityInfo':
            writer.write_string(value.offline_id)
            writer.write_int32(len(value.account_ids))
            for platform_flag_maybe, account_id in value.account_ids.items():
                writer.write_byte(platform_flag_maybe)
                writer.write_int32(len(account_id))
                writer.write_bytes_array(account_id)
        elif subtype == 'InventoryItem':
            writer.write_int32(value.unk1)
            writer.write_string(value.item_name)
            writer.write_int32(value.has_item_state)
            if value.has_item_state >= 1:
                writer.write_int32(value.item_state['unk'])
                writer.write_string(value.item_state['path_name'])
                writer.write_int32(value.item_state['binary_size'])
                writer.write_bytes_array(value.item_state['item_state_raw'])
        elif subtype == 'FluidBox':
            writer.write_float32(value.value)
        elif subtype == 'SlateBrush':
            writer.write_string(value)
        elif subtype == 'DateTime':
            writer.write_int64(int(value))
        elif subtype == 'FICFrameRange':
            FICFrameRange.serialize(writer, value)
        else:
            DynamicStructPropertyValue.write(writer, 0, value)
