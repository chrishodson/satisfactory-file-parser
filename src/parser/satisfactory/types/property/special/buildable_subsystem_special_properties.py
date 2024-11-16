from src.parser.byte.binary_readable_interface import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.structs.col4 import col4
from src.parser.satisfactory.types.structs.object_reference import ObjectReference
from src.parser.satisfactory.types.structs.transform import Transform


def is_buildable_subsystem_special_properties(obj: any) -> bool:
    return obj.type == 'BuildableSubsystemSpecialProperties'


class BuildableSubsystemSpecialProperties:
    def __init__(self):
        self.type = 'BuildableSubsystemSpecialProperties'
        self.buildables = []

    @staticmethod
    def parse(reader: BinaryReadable) -> 'BuildableSubsystemSpecialProperties':
        property = BuildableSubsystemSpecialProperties()

        entries_count = reader.read_int32()
        if entries_count > 0:
            for _ in range(entries_count):
                reader.read_int32()  # 0
                type_path = reader.read_string()
                count = reader.read_int32()

                instances = []
                for _ in range(count):
                    transform = Transform.parse(reader)

                    used_swatch_slot = ObjectReference.read(reader)
                    used_material = ObjectReference.read(reader)
                    used_pattern = ObjectReference.read(reader)
                    used_skin = ObjectReference.read(reader)

                    primary_color = col4.parse_rgba(reader)
                    secondary_color = col4.parse_rgba(reader)

                    used_paint_finish = ObjectReference.read(reader)
                    pattern_rotation = reader.read_byte()
                    used_recipe = ObjectReference.read(reader)
                    blueprint_proxy = ObjectReference.read(reader)

                    instances.append(BuildableTypeInstance(
                        transform,
                        primary_color,
                        secondary_color,
                        used_swatch_slot,
                        used_material,
                        used_pattern,
                        used_skin,
                        used_recipe,
                        used_paint_finish,
                        pattern_rotation,
                        blueprint_proxy
                    ))

                property.buildables.append({
                    'typePath': type_path,
                    'instances': instances
                })

        return property

    @staticmethod
    def serialize(writer: ByteWriter, property: 'BuildableSubsystemSpecialProperties'):
        writer.write_int32(len(property.buildables))

        if len(property.buildables) > 0:
            for buildable in property.buildables:
                writer.write_int32(0)
                writer.write_string(buildable['typePath'])
                writer.write_int32(len(buildable['instances']))

                for instance in buildable['instances']:
                    Transform.serialize(writer, instance.transform)

                    ObjectReference.write(writer, instance.used_swatch_slot)
                    ObjectReference.write(writer, instance.used_material)
                    ObjectReference.write(writer, instance.used_pattern)
                    ObjectReference.write(writer, instance.used_skin)

                    col4.serialize_rgba(writer, instance.primary_color)
                    col4.serialize_rgba(writer, instance.secondary_color)

                    ObjectReference.write(writer, instance.used_paint_finish)
                    writer.write_byte(instance.pattern_rotation)
                    ObjectReference.write(writer, instance.used_recipe)
                    ObjectReference.write(writer, instance.blueprint_proxy)


class BuildableTypeInstance:
    def __init__(self, transform: Transform, primary_color: col4, secondary_color: col4, used_swatch_slot: ObjectReference,
                 used_pattern: ObjectReference, used_material: ObjectReference, used_skin: ObjectReference,
                 used_recipe: ObjectReference, used_paint_finish: ObjectReference, pattern_rotation: int,
                 blueprint_proxy: ObjectReference):
        self.transform = transform
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.used_swatch_slot = used_swatch_slot
        self.used_pattern = used_pattern
        self.used_material = used_material
        self.used_skin = used_skin
        self.used_recipe = used_recipe
        self.used_paint_finish = used_paint_finish
        self.pattern_rotation = pattern_rotation
        self.blueprint_proxy = blueprint_proxy
