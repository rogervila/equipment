from py_compile import compile  # pylint: disable=W0622
from os import makedirs, walk, sep
from os.path import join, dirname, exists, isfile, isdir
from shutil import copyfile, copytree
from click import echo, style

from equipment.Command.AbstractCommand import AbstractCommand


class CompileCommand(AbstractCommand):
    def run(self, dist: str) -> None:
        try:
            echo(style(f'Compiling project into {dist}...', fg='green'))

            ignore_dirs = ['__pycache__', 'dist', 'tests', 'equipment']

            for root, dirs, files in walk('.'):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                for file in files:
                    if file.endswith('.py'):
                        source_path = join(root, file)
                        dest_path = join('.', dist, root.replace('/', sep).replace('\\', sep), f'{file}c')
                        makedirs(dirname(dest_path), exist_ok=True)
                        compile(source_path, dest_path)

            include_sources = ['config', 'database', 'storage', '.coveragerc', '.editorconfig',
                            '.env', '.env.example', '.gitignore', 'pyproject.toml', 'README.md']

            for source in include_sources:
                source_env_path = join('.', source)
                dest_env_path = join('.', dist, source.replace( '/', sep).replace('\\', sep))
                if exists(source_env_path):
                    if isfile(source_env_path):
                        copyfile(source_env_path, dest_env_path)
                    if isdir(source_env_path):
                        copytree(source_env_path, dest_env_path, dirs_exist_ok=True)


            echo(style(f'Project successfully compiled on {dist}!', fg='green'))
        except Exception as e:
            echo(style(f'Fatal error: {e}', fg='red'))
            return
