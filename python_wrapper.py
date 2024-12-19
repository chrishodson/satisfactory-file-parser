import pyodide
import js

# Load the TypeScript code using pyodide
pyodide.runPythonAsync("""
import js
js.fetch('https://cdn.jsdelivr.net/npm/@etothepii/satisfactory-file-parser@2.1.3/build/index.js')
""")

# Import the TypeScript code
satisfactory_parser = js.import_module('@etothepii/satisfactory-file-parser')

def parse_save(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()
    save = satisfactory_parser.Parser.ParseSave(file_path, file_content)
    return save

def write_save(save, file_path):
    satisfactory_parser.Parser.WriteSave(save, file_path)

def parse_blueprint(main_file_path, config_file_path):
    with open(main_file_path, 'rb') as main_file, open(config_file_path, 'rb') as config_file:
        main_file_content = main_file.read()
        config_file_content = config_file.read()
    blueprint = satisfactory_parser.Parser.ParseBlueprintFiles(main_file_path, main_file_content, config_file_content)
    return blueprint

def write_blueprint(blueprint, main_file_path, config_file_path):
    satisfactory_parser.Parser.WriteBlueprintFiles(blueprint, main_file_path, config_file_path)
