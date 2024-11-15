# Satisfactory File Parser
This is an NPM TypeScript Module to parse Satisfactory Files. Satisfactory is a game released by Coffee Stain Studios.
The reporitory is written entirely in TypeScript and comes with Type Definitions.

This parser can read, modify and write:
- Save Files `.sav`
- Blueprint Files `.sbp`, `.sbpcfg`

# Supported Versions
The version support of the packages is indicated below. Some bugs might still be present, see Bug Reporting further down.

Game Version Files of U5 and below are NOT supported.

| Game Version   |      Package                 |
|:--------------:|:-----------------------------|
| <= U5          |  ❌                          |
| U6 + U7        |  ✅ 0.0.1 - 0.0.34           |
| U8             |  ✅ 0.1.20 - 0.3.7           |
| U1.0           |  ✅ >= 0.4.20                |

# Installation
#### pip
`pip install satisfactory-file-parser`

# Mod Support ✅
By Default, most Mods just reuse Properties and Structs of the base game.
If however a Mod should not be working or have just objects with a lot of trailing unparseable data, Raise an issue or contact me.

Some explicitly tested mods include:
Ficsit-Cam, Structural Solutions, Linear Motion, Container Screens, Conveyor Wall Hole, X3-Signs, X3-Roads

# Reading a Save
Reading a Save in Memory.

```python
import os
from parser.parser import Parser

with open('./MySave.sav', 'rb') as f:
    file = f.read()
save = Parser.parse_save('MySave', file)
```


You can also read a Save via stream, to save RAM.
The binary data of the whole save will still be in memory, but the converted JSON can be streamed. (You can of course keep reading the stream in memory).
The returned `stream` is a readable WHATWG stream of type string and represents a `SatisfactorySave` object. this object can be serialized again.
WHATWG is used by default by browsers. Node js can use them using `Writable.toWeb()` and `Writable.fromWeb()` for example.
```python
import os
from parser.stream.reworked.readable_stream_parser import ReadableStreamParser

with open('./MySave.sav', 'rb') as f:
    file = f.read()
json_file_stream = open('./MySave.json', 'w', buffering=1024 * 1024 * 200)  # your outgoing JSON stream. In this case directly to file.

stream, start_streaming = ReadableStreamParser.create_readable_stream_from_save_to_json('MySave', file)

stream.pipe(json_file_stream)
json_file_stream.close()
start_streaming()
```


Consequently, writing a parsed save file back is just as easy.
The SaveParser has callbacks to assist during syncing on different occasions during the process.
For example, when writing the header or when writing a chunk of the save body.
The splitting in individual chunks enables you to more easily stream the binary data to somewhere else.
```python
import os
from parser.parser import Parser

file_header = None
body_chunks = []
Parser.write_save(save, lambda header: print('on save header.') or file_header = header, lambda chunk: print('on save body chunk.') or body_chunks.append(chunk))

# write complete sav file back to disk
with open('./MyModifiedSave.sav', 'wb') as f:
    f.write(file_header + b''.join(body_chunks))
```


## Inspecting Save Objects
You can for example loop through players and print their cached names and positions.

```python
from parser.satisfactory.types.objects.save_entity import is_save_entity, SaveEntity
from parser.satisfactory.types.property.generic.str_property import StrProperty

objects = [obj for level in save.levels for obj in level.objects]
players = [obj for obj in objects if is_save_entity(obj) and obj.type_path == '/Game/FactoryGame/Character/Player/Char_Player.Char_Player_C']
for player in players:
    name = player.properties['mCachedPlayerName'].value
    print(name, player.transform['translation'])
```


# Usage of Blueprint Parsing
Note, that blueprints consist of 2 files. The `.sbp` main file and the config file `.sbpcfg`.

```python
import os
from parser.parser import Parser

with open('./MyBlueprint.sbp', 'rb') as f:
    main_file = f.read()
with open('./MyBlueprint.sbpcfg', 'rb') as f:
    config_file = f.read()
blueprint = Parser.parse_blueprint_files('Myblueprint', main_file, config_file)
```

Consequently, writing a blueprint into binary data works the same way with getting callbacks in the same style as the save parsing.
```python
import os
from parser.parser import Parser

main_file_header = None
main_file_body_chunks = []
summary = Parser.write_blueprint_files(blueprint, lambda header: print('on main file header.') or main_file_header = header, lambda chunk: print('on main file body chunk.') or main_file_body_chunks.append(chunk))

# write complete .sbp file back to disk
with open('./MyBlueprint.sbp', 'wb') as f:
    f.write(main_file_header + b''.join(main_file_body_chunks))

# write .sbpcfg file back to disk, we get that data from the result of WriteBlueprintFiles
with open('./MyBlueprint.sbpcfg', 'wb') as f:
    f.write(summary['config_file_binary'])
```

# Additional Infos
For every parser call, you can pass optional callbacks to receive additional info.
Like a callback on the decompressed save body. Parsing saves provides a callback for reporting progress [0,1] and an occasional message.
```python
save = Parser.parse_save('MySave', file, {
    'on_decompressed_save_body': lambda body: print('on decompressed body', len(body)),
    'on_progress_callback': lambda progress, msg: print(progress, msg)
})
```
```python
stream, start_streaming = ReadableStreamParser.create_readable_stream_from_save_to_json(savename, file, {
    'on_progress': lambda progress, msg: print('progress', progress, msg)
})
```
```python
blueprint = Parser.parse_blueprint_files('Myblueprint', file, config_file, {
    'on_decompressed_blueprint_body': lambda body: print('on decompressed body', len(body))
})
```

# Bug Reports or Feedback
You can always raise an issue on the linked [github project](https://github.com/etothepii4/satisfactory-file-parser) or hit me up on the satisfactory discord `etothepii`.

# [Changelog](https://github.com/etothepii4/satisfactory-file-parser/blob/main/CHANGELOG.md).

# License 
MIT License

Copyright (c) 2021-2024 etothepii

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
