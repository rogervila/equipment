from py_compile import compile  # pylint: disable=W0622
from os import walk
from pathlib import Path
from shutil import copyfile, copytree
from click import echo, style

from equipment.Command.AbstractCommand import AbstractCommand


class CompileCommand(AbstractCommand):
    def run(self, *args, **kwargs) -> None:
        dist = kwargs.get('dist', args[0] if len(args) > 0 else None)

        if dist is None:
            raise TypeError('CompileCommand.run requires dist')

        try:
            echo(style(f'Compiling project into {dist}...', fg='green'))

            output_path = Path(dist)
            output_resolved = output_path.resolve()
            ignore_dirs = {'__pycache__', 'dist', 'tests', 'equipment'}

            for root, dirs, files in walk('.'):
                root_path = Path(root)
                dirs[:] = [
                    directory for directory in dirs
                    if directory not in ignore_dirs
                    and (root_path / directory).resolve() != output_resolved
                ]

                for file in files:
                    if file.endswith('.py'):
                        source_path = root_path / file
                        dest_path = output_path / source_path.parent / f'{source_path.name}c'
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        compile(str(source_path), str(dest_path))

            include_sources = [
                Path('config'),
                Path('database'),
                Path('storage'),
                Path('.coveragerc'),
                Path('.editorconfig'),
                Path('.env'),
                Path('.env.example'),
                Path('.gitignore'),
                Path('pyproject.toml'),
                Path('README.md'),
            ]

            for source_path in include_sources:
                dest_path = output_path / source_path
                if source_path.exists():
                    if source_path.is_file():
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        copyfile(source_path, dest_path)
                    if source_path.is_dir():
                        copytree(source_path, dest_path, dirs_exist_ok=True)


            echo(style(f'Project successfully compiled on {dist}!', fg='green'))
        except Exception as e:
            echo(style(f'Fatal error: {e}', fg='red'))
            return
