import json
import subprocess
import sys
import unittest


HEAVY_OPTIONAL_MODULES = {
    'boto3',
    'botocore',
    'python_sqlite_log_handler',
    'pythonjsonlogger',
    'redis',
    'rq',
    'sqlalchemy',
}

TEMPLATE_DOWNLOAD_MODULES = {
    'charset_normalizer',
    'requests',
    'urllib3',
}

# Modules listed in __lazy_modules__ (PEP 810), only deferred on Python 3.15+.
LAZY_IMPORT_MODULES = {
    'dotenv',
    'logging.handlers',
    'py_compile',
    'schedule',
    'zipfile',
}


class ImportPerformanceTest(unittest.TestCase):
    def test_import_equipment_defers_optional_provider_dependencies(self):
        code = (
            'import json\n'
            'import sys\n'
            'import equipment\n'
            f'roots = {sorted(HEAVY_OPTIONAL_MODULES)!r}\n'
            "modules = sorted(name for name in sys.modules if name.split('.', 1)[0] in roots)\n"
            'print(json.dumps(modules))\n'
        )

        completed = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertEqual([], json.loads(completed.stdout))

    def test_import_cli_defers_template_download_dependencies(self):
        code = (
            'import json\n'
            'import sys\n'
            'import equipment.Command\n'
            f'roots = {sorted(TEMPLATE_DOWNLOAD_MODULES)!r}\n'
            "modules = sorted(name for name in sys.modules if name.split('.', 1)[0] in roots)\n"
            'print(json.dumps(modules))\n'
        )

        completed = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertEqual([], json.loads(completed.stdout))

    @unittest.skipIf(sys.version_info < (3, 15), 'PEP 810 lazy imports require Python 3.15+')
    def test_import_defers_lazy_modules(self):
        code = (
            'import json\n'
            'import sys\n'
            'import equipment\n'
            'import equipment.Command\n'
            'import equipment.Scheduler.Scheduler\n'
            f'names = {sorted(LAZY_IMPORT_MODULES)!r}\n'
            'modules = [name for name in names if name in sys.modules]\n'
            'print(json.dumps(modules))\n'
        )

        completed = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertEqual([], json.loads(completed.stdout))


if __name__ == '__main__':
    unittest.main()
