import unittest
from python_wrapper import parse_save, write_save, parse_blueprint, write_blueprint

class TestPythonWrapper(unittest.TestCase):

    def test_parse_save(self):
        save = parse_save('test_save.sav')
        self.assertIsNotNone(save)
        self.assertIn('header', save)
        self.assertIn('levels', save)

    def test_write_save(self):
        save = parse_save('test_save.sav')
        write_save(save, 'test_save_output.sav')
        save_output = parse_save('test_save_output.sav')
        self.assertEqual(save, save_output)

    def test_parse_blueprint(self):
        blueprint = parse_blueprint('test_blueprint.sbp', 'test_blueprint.sbpcfg')
        self.assertIsNotNone(blueprint)
        self.assertIn('header', blueprint)
        self.assertIn('objects', blueprint)

    def test_write_blueprint(self):
        blueprint = parse_blueprint('test_blueprint.sbp', 'test_blueprint.sbpcfg')
        write_blueprint(blueprint, 'test_blueprint_output.sbp', 'test_blueprint_output.sbpcfg')
        blueprint_output = parse_blueprint('test_blueprint_output.sbp', 'test_blueprint_output.sbpcfg')
        self.assertEqual(blueprint, blueprint_output)

if __name__ == '__main__':
    unittest.main()
