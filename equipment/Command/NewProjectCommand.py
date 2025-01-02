from os import sep
from os.path import abspath, dirname, isdir, join
from shutil import copyfile, copytree, ignore_patterns
from click import confirm, echo, style
from equipment.Command.AbstractCommand import AbstractCommand
from requests import get
from zipfile import ZipFile
from io import BytesIO

class NewProjectCommand(AbstractCommand):
    def run(self, name: str, path: str) -> None:
        project_template_path = f'{abspath(dirname(__file__))}{sep}_project'

        if not isdir(project_template_path):
            try:
                response = get('https://github.com/rogervila/equipment/archive/refs/heads/main.zip')
                with ZipFile(BytesIO(response.content)) as zip_file:
                    zip_file.extractall(project_template_path)
            except Exception as e:
                echo(style(f'Could not download project template: {e}', fg='red'))
                return

        project_template_path = f'{project_template_path}{sep}equipment-main{sep}project'

        if not isdir(project_template_path):
            echo(style(f'Project template not found in "{project_template_path}". If the error persists, please open an issue', fg='red'))
            return

        try:
            echo(style(f'Creating "{name}" project on {path}...', fg='green'))

            project_path = f'{path}{sep}{name}'
            already_exists = isdir(project_path)
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
                join(project_template_path, '.env.example'),
                join(project_path, '.env')
            )

            echo(style(f'Project successfully created on {project_path}!', fg='green'))
        except Exception as e:
            echo(style(f'Fatal error: {e}', fg='red'))
            return
