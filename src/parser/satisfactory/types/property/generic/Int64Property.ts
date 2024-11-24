import { BinaryReadable } from '../../../../byte/binary-readable.interface';
import { ByteWriter } from '../../../../byte/byte-writer.class';
import { GUIDInfo } from '../../structs/GUIDInfo';
import { AbstractBaseProperty } from './AbstractBaseProperty';

export const isInt64Property = (property: any): property is Int64Property => !Array.isArray(property) && property.type === 'Int64Property';

export type Int64Property = AbstractBaseProperty & {
    type: 'Int64Property';
    value: string;
};

export namespace Int64Property {

    export const Parse = (reader: BinaryReadable, ueType: string, index: number = 0): Int64Property => {
        const guidInfo = GUIDInfo.read(reader);
        const value = ReadValue(reader);

        return {
            ...AbstractBaseProperty.Create({ index, ueType, guidInfo, type: '' }),
            type: 'Int64Property',
            value,
        } satisfies Int64Property;
    }

    export const ReadValue = (reader: BinaryReadable): string => {
        return reader.readInt64().toString();
    }

    export const CalcOverhead = (property: Int64Property): number => {
        return 1;
    }

    export const Serialize = (writer: ByteWriter, property: Int64Property): void => {
        GUIDInfo.write(writer, property.guidInfo);
        SerializeValue(writer, property.value);
    }

    export const SerializeValue = (writer: ByteWriter, value: string): void => {
        writer.writeInt64(BigInt(value));
    }
}