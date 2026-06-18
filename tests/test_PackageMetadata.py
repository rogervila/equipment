import pathlib
import tomllib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SUPPORTED_CLASSIFIERS = {
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
}


def load_pyproject(path: pathlib.Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


class PackageMetadataTest(unittest.TestCase):
    def test_package_metadata_declares_supported_python_versions(self):
        project = load_pyproject(ROOT / "pyproject.toml")["project"]

        self.assertEqual(">=3.12", project["requires-python"])
        self.assertTrue(SUPPORTED_CLASSIFIERS.issubset(project["classifiers"]))
        self.assertTrue((ROOT / project["readme"]).is_file())

    def test_template_metadata_declares_supported_python_versions(self):
        project = load_pyproject(ROOT / "project" / "pyproject.toml")["project"]

        self.assertEqual(">=3.12", project["requires-python"])
        self.assertTrue(SUPPORTED_CLASSIFIERS.issubset(project["classifiers"]))
        self.assertTrue((ROOT / "project" / project["readme"]).is_file())


if __name__ == "__main__":
    unittest.main()
