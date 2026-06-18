import os
import shutil
import tempfile
import unittest
from pathlib import Path

from equipment.Command.CompileCommand import CompileCommand


class CompileCommandTest(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(tempfile.mkdtemp())
        self.previous_cwd = Path.cwd()
        os.chdir(self.workspace)
        self.addCleanup(os.chdir, self.previous_cwd)
        self.addCleanup(shutil.rmtree, self.workspace)

    def write_file(self, path: str, content: str = '') -> Path:
        file_path = self.workspace / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        return file_path

    def test_compile_creates_bytecode_and_copies_runtime_assets(self):
        self.write_file('main.py', 'print("hello")\n')
        self.write_file('app/service.py', 'VALUE = 1\n')
        self.write_file('tests/test_skip.py', 'VALUE = 2\n')
        self.write_file('equipment/__init__.py', 'VALUE = 3\n')
        self.write_file('config/app.yaml', 'app:\n  name: demo\n')
        self.write_file('database/schema.sql', 'select 1;\n')
        self.write_file('storage/app/data.txt', 'data')
        self.write_file('.env', 'APP_ENV=local\n')
        self.write_file('.env.example', 'APP_ENV=local\n')
        self.write_file('.coveragerc', '[run]\n')
        self.write_file('.editorconfig', 'root = true\n')
        self.write_file('.gitignore', '.env\n')
        self.write_file('pyproject.toml', '[project]\nname = "demo"\n')
        self.write_file('README.md', '# Demo\n')

        CompileCommand().run('dist')

        self.assertTrue((self.workspace / 'dist' / 'main.pyc').is_file())
        self.assertTrue((self.workspace / 'dist' / 'app' / 'service.pyc').is_file())
        self.assertFalse((self.workspace / 'dist' / 'tests' / 'test_skip.pyc').exists())
        self.assertFalse((self.workspace / 'dist' / 'equipment' / '__init__.pyc').exists())
        self.assertEqual('app:\n  name: demo\n', (self.workspace / 'dist' / 'config' / 'app.yaml').read_text(encoding='utf-8'))
        self.assertEqual('APP_ENV=local\n', (self.workspace / 'dist' / '.env').read_text(encoding='utf-8'))
        self.assertEqual('# Demo\n', (self.workspace / 'dist' / 'README.md').read_text(encoding='utf-8'))

    def test_compile_skips_existing_output_directory(self):
        self.write_file('main.py', 'print("hello")\n')
        self.write_file('build/output/old.py', 'print("old")\n')

        CompileCommand().run(str(Path('build') / 'output'))

        self.assertTrue((self.workspace / 'build' / 'output' / 'main.pyc').is_file())
        self.assertFalse((self.workspace / 'build' / 'output' / 'build' / 'output' / 'old.pyc').exists())


if __name__ == '__main__':
    unittest.main()
