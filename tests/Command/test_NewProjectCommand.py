import io
import importlib
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch

from equipment.Command.NewProjectCommand import NewProjectCommand


ROOT = Path(__file__).resolve().parents[2]
PROJECT_TEMPLATE = ROOT / 'project'
new_project_module = importlib.import_module('equipment.Command.NewProjectCommand')
TEMPLATE_CACHE = Path(new_project_module.__file__).resolve().parent / '_project'


def build_project_template_zip() -> bytes:
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for file_path in PROJECT_TEMPLATE.rglob('*'):
            if not file_path.is_file():
                continue

            relative_path = file_path.relative_to(PROJECT_TEMPLATE)
            if '__pycache__' in relative_path.parts:
                continue

            archive_path = Path('equipment-main') / 'project' / relative_path
            zip_file.write(file_path, archive_path.as_posix())

    return buffer.getvalue()


class NewProjectCommandTest(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(tempfile.mkdtemp())
        self.template_zip = build_project_template_zip()
        self.addCleanup(shutil.rmtree, self.workspace)
        self.addCleanup(self.clean_template_cache)

    def clean_template_cache(self):
        if TEMPLATE_CACHE.is_dir():
            shutil.rmtree(TEMPLATE_CACHE)

    def test_run_scaffolds_project_from_downloaded_template(self):
        response = Mock(content=self.template_zip)

        with patch.object(new_project_module, '_download_project_template', return_value=response):
            NewProjectCommand().run('demo-app', str(self.workspace))

        project_path = self.workspace / 'demo-app'

        self.assertTrue((project_path / 'main.py').is_file())
        self.assertTrue((project_path / 'queues.py').is_file())
        self.assertTrue((project_path / 'scheduler.py').is_file())
        self.assertTrue((project_path / 'web.py').is_file())
        self.assertTrue((project_path / 'app' / 'Inspire.py').is_file())
        self.assertTrue((project_path / 'config' / 'app.yaml').is_file())
        self.assertTrue((project_path / 'tests' / 'TestCase.py').is_file())
        self.assertTrue((project_path / 'README.md').is_file())
        self.assertTrue((project_path / '.env').is_file())
        self.assertEqual(
            (project_path / '.env.example').read_text(encoding='utf-8'),
            (project_path / '.env').read_text(encoding='utf-8'),
        )
        self.assertIn('name = "demo-app"', (project_path / 'pyproject.toml').read_text(encoding='utf-8'))
        self.assertNotIn('PROJECT_NAME', (project_path / 'pyproject.toml').read_text(encoding='utf-8'))
        main_content = (project_path / 'main.py').read_text(encoding='utf-8')
        self.assertIn('$ python scheduler.py', main_content)
        self.assertNotIn('$ py ', main_content)
        self.assertFalse((project_path / 'storage' / 'logs' / 'app.log').exists())

    def test_run_does_not_overwrite_existing_project_when_user_declines(self):
        project_path = self.workspace / 'demo-app'
        project_path.mkdir()
        marker_path = project_path / 'pyproject.toml'
        marker_path.write_text('existing', encoding='utf-8')
        response = Mock(content=self.template_zip)

        with patch.object(new_project_module, '_download_project_template', return_value=response):
            with patch.object(new_project_module, 'confirm', return_value=False) as confirm:
                NewProjectCommand().run('demo-app', str(self.workspace))

        confirm.assert_called_once()
        self.assertEqual('existing', marker_path.read_text(encoding='utf-8'))

    def test_run_stops_when_template_download_fails(self):
        with patch.object(new_project_module, '_download_project_template', side_effect=Exception('network down')):
            NewProjectCommand().run('broken-app', str(self.workspace))

        self.assertFalse((self.workspace / 'broken-app').exists())


if __name__ == '__main__':
    unittest.main()
