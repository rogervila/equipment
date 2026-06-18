from pathlib import Path
from shutil import copyfile, copytree, ignore_patterns, rmtree
from zipfile import ZipFile
from io import BytesIO
from click import confirm, echo, style
from requests import get
from equipment.Command.AbstractCommand import AbstractCommand


class NewProjectCommand(AbstractCommand):
    def run(self, *args, **kwargs) -> None:
        name = kwargs.get('name', args[0] if len(args) > 0 else None)
        path = kwargs.get('path', args[1] if len(args) > 1 else None)

        if name is None or path is None:
            raise TypeError('NewProjectCommand.run requires name and path')

        project_template_root = Path(__file__).resolve().parent / '_project'

        if project_template_root.is_dir():
            rmtree(project_template_root)

        try:
            response = get('https://github.com/rogervila/equipment/archive/refs/heads/main.zip', timeout=60)
            with ZipFile(BytesIO(response.content)) as zip_file:
                zip_file.extractall(project_template_root)
        except Exception as e:
            echo(style(f'Could not download project template: {e}', fg='red'))
            return

        project_template_path = project_template_root / 'equipment-main' / 'project'

        if not project_template_path.is_dir():
            echo(style(f'Project template not found in "{project_template_path}". If the error persists, please open an issue', fg='red'))
            return

        try:
            echo(style(f'Creating "{name}" project on {path}...', fg='green'))

            project_path = Path(path) / name
            already_exists = project_path.is_dir()
            confirmation = confirm(
                f'Directory "{project_path}" already exists. Do you want to override it?' # autopep8: off
            ) if already_exists else True

            if not confirmation:
                echo(style('Skip', fg='yellow'))
                return None

            copytree(
                project_template_path,
                project_path,
                symlinks=True,
                dirs_exist_ok=True,
                ignore=ignore_patterns(
                    '*.py[co]',
                    '__pycache__',
                    '.git',
                    'htmlcov',
                    'equipment',
                    'venv',
                    '.env',
                    '.coverage',
                    '*.log',
                    '*.lock',
                    '*.sqlite*',
                    '.DS_Store',
                )
            )

            copyfile(
                project_template_path / '.env.example',
                project_path / '.env'
            )

            pyproject_path = project_path / 'pyproject.toml'

            pyproject_content = pyproject_path.read_text(encoding='utf-8')

            pyproject_content = pyproject_content.replace('PROJECT_NAME', name)

            pyproject_path.write_text(pyproject_content, encoding='utf-8')

            echo(style(f'Project "{name}" successfully created on {project_path}!', fg='green'))
        except Exception as e:
            echo(style(f'Fatal error: {e}', fg='red'))
            return
