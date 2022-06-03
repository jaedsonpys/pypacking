from argeasy import ArgEasy

from .exceptions import ConfigFileNotFoundError, PackageNotFoundError
from .pypacking import PyPacking


def main():
    parser = ArgEasy(
        project_name='PyPacking',
        description='Build project packages',
        version='1.0.0'
    )

    parser.add_argument('generate_config', 'Generate a default config file', action='store_true')
    parser.add_argument('dist', 'Create a distribution of your package', action='store_true')

    args = parser.get_args()

    if args.generate_config:
        project_name = input('Name: ').strip()
        project_description = input('Description (default description): ').strip()
        project_version = input('Version (1.0.0): ').strip()
        package_path = input('Python package: ').strip()

        if not project_version:
            project_version = '1.0.0'
        if not project_description:
            project_description = f'The {project_name} project'

        PyPacking.make_config(project_name, project_description, project_version, package_path)
        print('-' * 50)
        print('Project config \033[1mcreated\033[m! Check "pypacking.ini" file.')
    elif args.dist:
        print('Creating package...')

        try:
            pypacking = PyPacking()
        except ConfigFileNotFoundError as error:
            print('-' * 30)
            print(f'\033[31m{error.msg}\033[m')
            return None
        except PackageNotFoundError as error:
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
