from argeasy import ArgEasy
import os

from .exceptions import ConfigFileNotFoundError
from .exceptions import PackageNotFoundError
from .exceptions import InvalidConfigFileError
from .pypacking import PyPacking


def main():
    parser = ArgEasy(
        project_name='PyPacking',
        description=('PyPacking is a package manager and'
                    'installer for Python designed to be'
                    'interactive and user-friendly.\nWith'
                    'easy operation, you can install packages and tools.'),
        version='2.0.0'
    )

    parser.add_argument('generate_config', 'Generate a default config file', action='store_true')
    parser.add_argument('dist', 'Create a distribution of your package', action='store_true')
    parser.add_argument('list', 'Lists packages installed by PyPacking', action='store_true')
    parser.add_argument('install', 'Install a package')
    parser.add_argument('uninstall', 'Uninstall a package')

    args = parser.get_args()

    if args.generate_config:
        author_name = input('Author name: ').strip()
        author_email = input('Author email: ').strip()
        project_name = input('Project name: ').strip()
        project_description = input('Description (default description): ').strip()
        project_version = input('Version (1.0.0): ').strip()
        package_path = input('Python package: ').strip()
        entry_script = input('Entry script (nothing to disable): ').strip()

        entry_script = entry_script if entry_script else None

        if not project_version:
            project_version = '1.0.0'
        if not project_description:
            project_description = f'The {project_name} project'

        PyPacking.make_config(
            author_name,
            author_email,
            project_name,
            project_description,
            project_version,
            package_path,
            script_entry=entry_script
        )

        print('-' * 50)
        print('Project config \033[1mcreated\033[m! Check "pypacking.ini" file.')
    elif args.dist:
        print('Creating package...')
        pypacking = PyPacking()

        try:
            pypacking.read_config()
        except ConfigFileNotFoundError as error:
            print('-' * 30)
            print(f'\033[31m{error.msg}\033[m')
            return None
        except PackageNotFoundError as error:
            print('-' * 30)
            print(f'\033[31m{error.msg}\033[m')
            return None
        except InvalidConfigFileError as error:
            print('-' * 30)
            print(f'\033[31m{error.msg}\033[m')
            return None
    
        pypacking.make_package()
        print('=' * 20, end=' ')
        print('SUCESS', end=' ')
        print('=' * 20)
        
        name = pypacking.project_name
        version = pypacking.project_version
        print(f'\033[32mPackage {name} in version {version} has been generated.\033[m')
    elif args.install:
        package_name: str = args.install

        if package_name.endswith('.zip'):
            if os.path.isfile(package_name) is False:
                print('Error:')
                print(f'\t\033[31mPackage file "{package_name}" not found\033[m')
            else:
                pypack = PyPacking()
                pypack.install(package_name)
    elif args.list:
        packages = PyPacking.list_packages()

        for name, info in packages.items():
            print(f'{name}::{info["version"]}')
    elif args.uninstall:
        project_name = args.uninstall

        pypacking = PyPacking()
        pypacking.uninstall(project_name)
