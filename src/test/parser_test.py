import os
import json
import pytest
from parser.parser import Parser
from parser.satisfactory.save.satisfactory_save import SatisfactorySave
from parser.stream.reworked.readable_stream_parser import ReadableStreamParser

def setup_module(module):
    global file_log
    file_log = open(os.path.join(os.path.dirname(__file__), 'test-log.txt'), 'w')
    original_stdout = sys.stdout
    sys.stdout = file_log

def teardown_module(module):
    if file_log:
        file_log.close()

def parse_save_sync(savename, file, on_decompressed_save_body):
    save = Parser.parse_save(savename, file, {
        'on_decompressed_save_body': on_decompressed_save_body,
        'on_progress_callback': lambda progress, msg: print(f'progress {progress} {msg}')
    })
    return save

def write_save_sync(save, on_binary_before_compressing):
    main_file_header = None
    main_file_body_chunks = []
    Parser.write_save(save,
        lambda header: main_file_header = header,
        lambda chunk: main_file_body_chunks.append(chunk),
        {'on_binary_before_compressing': on_binary_before_compressing}
    )
    with open(os.path.join(os.path.dirname(__file__), save.name + '_on-writing.sav'), 'wb') as f:
        f.write(main_file_header + b''.join(main_file_body_chunks))

save_list = [
    'Release 001',
    'Release 032',
    '264_ohne_Mods',
    'ficsitcam-1',
    'structuralsolutions-1',
    'x3-roads-signs'
]

@pytest.mark.parametrize('savename', save_list)
def test_parse_save_to_json_with_stream_and_sync(savename):
    filepath = os.path.join(os.path.dirname(__file__), savename + '.sav')
    binary_filepath_stream = os.path.join(os.path.dirname(__file__), savename + '.stream.bin')
    binary_filepath_sync = os.path.join(os.path.dirname(__file__), savename + '.sync.bin')
    with open(filepath, 'rb') as f:
        file = f.read()
    out_json_path_stream = os.path.join(os.path.dirname(__file__), savename + '.stream.json')
    out_json_path_sync = os.path.join(os.path.dirname(__file__), savename + '.sync.json')

    out_json_stream = open(out_json_path_stream, 'w')

    stream, start_streaming = ReadableStreamParser.create_readable_stream_from_save_to_json(savename, file, {
        'on_decompressed_save_body': lambda decompressed_body: open(binary_filepath_stream, 'wb').write(decompressed_body),
        'on_progress': lambda progress, msg: print(f'progress {progress} {msg}')
    })

    start = time.perf_counter()
    start_streaming()
    stream.pipe_to(out_json_stream)

    end = 0
    out_json_stream.close()
    end = time.perf_counter()

    print(f'Streaming took {(end - start) / 1000} seconds.')

    start2 = time.perf_counter()
    save = parse_save_sync(savename, file, lambda decompressed_body: open(binary_filepath_sync, 'wb').write(decompressed_body))
    with open(out_json_path_sync, 'w') as f:
        json.dump(save, f)
    end2 = time.perf_counter()

    print(f'Sync Parsing took {(end2 - start2) / 1000} seconds.')

    with open(out_json_path_stream, 'r') as f:
        json1 = json.load(f)
    with open(out_json_path_sync, 'r') as f:
        json2 = json.load(f)
    assert json.dumps(json1) == json.dumps(json2)

@pytest.mark.parametrize('savename', save_list)
def test_write_sync_save(savename):
    filepath = os.path.join(os.path.dirname(__file__), savename + '.sync.json')
    with open(filepath, 'r') as f:
        save = json.load(f)
    write_save_sync(save, lambda binary: open(os.path.join(os.path.dirname(__file__), save['name'] + '_on-writing.bin'), 'wb').write(binary))

@pytest.mark.parametrize('blueprintname', [
    'release-single-wall',
    'release-storage-mk1',
    'release-storage-mk2-blueprintmk2',
    'release-two-foundations',
])
def test_read_write_sync_blueprint(blueprintname):
    filepath_blueprint = os.path.join(os.path.dirname(__file__), blueprintname + '.sbp')
    filepath_blueprint_config = os.path.join(os.path.dirname(__file__), blueprintname + '.sbpcfg')
    binary_filepath = os.path.join(os.path.dirname(__file__), blueprintname + '.bins')
    with open(filepath_blueprint, 'rb') as f:
        file = f.read()
    with open(filepath_blueprint_config, 'rb') as f:
        config_file_buffer = f.read()

    blueprint = Parser.parse_blueprint_files(blueprintname, file, config_file_buffer, {
        'on_decompressed_blueprint_body': lambda decompressed_body: open(binary_filepath, 'wb').write(decompressed_body)
    })

    with open(os.path.join(os.path.dirname(__file__), blueprintname + '.json'), 'w') as f:
        json.dump(blueprint, f, indent=4)

    main_file_header = None
    main_file_body_chunks = []
    response = Parser.write_blueprint_files(blueprint,
        lambda header: main_file_header = header,
        lambda chunk: main_file_body_chunks.append(chunk),
        {
            'on_main_file_binary_before_compressing': lambda binary: open(os.path.join(os.path.dirname(__file__), blueprintname + '.bins_modified'), 'wb').write(binary)
        }
    )

    with open(os.path.join(os.path.dirname(__file__), blueprintname + '.sbp_modified'), 'wb') as f:
        f.write(main_file_header + b''.join(main_file_body_chunks))

    with open(os.path.join(os.path.dirname(__file__), blueprintname + '.sbpcfg_modified'), 'wb') as f:
        f.write(response['config_file_binary'])
