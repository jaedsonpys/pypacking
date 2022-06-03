import os
import shutil
from configparser import ConfigParser
from platform import system
from hashlib import md5
import zipfile

from .exceptions import ConfigFileNotFoundError
from .exceptions import PackageNotFoundError

CONFIG_FILENAME = 'pypacking.ini'
USERNAME = os.environ.get('USER')
USER_OS = system()

_virtual_env = os.environ.get('VIRTUAL_ENV')

if USER_OS == 'Linux':
    if _virtual_env:
        LOCAL_PATH = _virtual_env
    else:
        LOCAL_PATH = os.path.join('/home', USERNAME, '.local')


class PyPacking:
    def __init__(self) -> None:
        if os.path.isfile(CONFIG_FILENAME) is False:
            raise ConfigFileNotFoundError('Configuration file "pypacking.ini" not found')

        project_config = ConfigParser()
        project_config.read(CONFIG_FILENAME)

        project_info = project_config['INFO']
        package_info = project_config['PACKAGE']

        self.project_name = project_info['projectName']
        self.project_version = project_info['version']
        self.project_description = project_info['description']

        self.package_path = package_info['packagePath']
        script_entry = package_info.get('scriptEntry')
        
        if script_entry:
            self.package_type = 'entry_script'
            self.script_entry = script_entry
        else:
            self.package_type = 'library'

        if os.path.isdir(self.package_path) is False:
            raise PackageNotFoundError(f'Package "{self.package_path}" not found in root directory')

        try:
            self.file_hashes = dict(project_config['FILES'])
        except KeyError:
            self.file_hashes = {}

        if not self.file_hashes:
            self._hash_files()
            project_config['FILES'] = self.file_hashes
            with open(CONFIG_FILENAME, 'w') as file_w:
                project_config.write(file_w)

    def _gen_hash(self, filepath: str) -> str:
        with open(filepath, 'rb') as file_read:
            content = file_read.read()
            hashfile = md5(content).hexdigest()

        return hashfile

    def _hash_files(self) -> dict:
        for dirpath, dirnames, filenames in os.walk(self.package_path):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                self.file_hashes[filepath] = self._gen_hash(filepath)

    @staticmethod
    def make_config(
        project_name: str,
        description: str,
        version: str,
        package_path: str,
        scriptEntry: str = None
    ) -> None:
        config = ConfigParser()

        config['INFO'] = {
            'projectName': project_name,
            'description': description,
            'version': version
        }

        config['PACKAGE'] = {
            'packagePath': package_path,
        }

        if scriptEntry:
            config['PACKAGE']['scriptEntry'] = scriptEntry

        config['FILES'] = {}

        with open(CONFIG_FILENAME, 'w') as file_write:
            config.write(file_write)

    def make_package(self) -> None:
        package_name = f'{self.project_name}-{self.project_version}'
        package_dist_path = os.path.join('dist', package_name)
        build_filepath = os.path.join('build', self.package_path)

        modified_files = []
        first_build = True

        if os.path.isdir('dist') is False:
            print('Creating dist/ directory...', end='')
            os.mkdir('dist')
            print('done')
        
        if os.path.isdir('build'):
            first_build = False

        if not first_build:
            for filepath, previous_hash in self.file_hashes.items():
                new_hash = self._gen_hash(filepath)

                if new_hash != previous_hash:
                    self.file_hashes[filepath] = new_hash
                    modified_files.append(filepath)

            print(f'{len(modified_files)} files were changed. Copying...')

            for file in modified_files:
                filepath = os.path.join('build', file)
                print(f'Removing {file} from build/ directory...')
                os.remove(filepath)
                print(f'Copying {file} to build/{self.package_path} directory...', end='')
                shutil.copyfile(file, filepath)
                print('done')
        else:
            print('First build detected')
            print('Copying package to build/ directory...', end='')
            shutil.copytree(self.package_path, build_filepath)
            print('done')

        print('Copying "pypacking.ini" file to build/ directory...', end='')
        shutil.copyfile(CONFIG_FILENAME, os.path.join('build', CONFIG_FILENAME))
        print('done')

        print('Compressing build/ directory into ZIP file...', end='')
        shutil.make_archive(package_dist_path, 'zip', 'build')
        print('done')

    def install(self, package_path: str) -> None:
        if os.path.isfile(package_path) is False:
            raise FileNotFoundError(f'Package "{package_path}" was not found.')

        package_data = zipfile.ZipFile(package_path, 'r')
        package_config = package_data.read(CONFIG_FILENAME)

        config = ConfigParser()
        config.read_string(package_config.decode())

        package_info = config['PACKAGE']
        name = config['INFO']['projectName']
        version = config['INFO']['version']
        package_name = package_info['packagePath']

        libdir_path = os.path.join(LOCAL_PATH, 'lib/python3/site-packages')
        package_dst = os.path.join(LOCAL_PATH, 'lib/python3/site-packages', package_name)

        script_entry = package_info.get('scriptEntry')
        
        if script_entry:
            pass
        else:
            # if package is a library
            print(LOCAL_PATH)
            shutil.unpack_archive(package_path, package_dst, format='zip')
            config_filename = os.path.join(package_dst, libdir_path, CONFIG_FILENAME)
            os.remove(config_filename)
