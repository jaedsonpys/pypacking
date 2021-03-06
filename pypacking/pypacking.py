import os
import sys
import shutil
from configparser import ConfigParser
import platform
from hashlib import md5
import zipfile

from .exceptions import ConfigFileNotFoundError
from .exceptions import PackageNotFoundError
from .exceptions import InvalidConfigFileError

CONFIG_FILENAME = 'pypacking.ini'
USERNAME = os.environ.get('USER')
USER_OS = platform.system()

_virtual_env = os.environ.get('VIRTUAL_ENV')

if USER_OS == 'Linux':
    if _virtual_env:
        SITE_PACKAGES_PATH = sys.path[-1]
        LOCAL_PATH = _virtual_env
    else:
        LOCAL_PATH = os.path.join('/home/{USERNAME}/.local')
        for path in sys.path:
            if os.path.basename(path) == 'site-packages':
                SITE_PACKAGES_PATH = path
                break


class PyPacking:
    def __init__(self) -> None:
        self.package_path = None
        self.project_description = None
        self.project_name = None
        self.project_version = None
        self.file_hashes = None

    def read_config(self) -> None:
        if os.path.isfile(CONFIG_FILENAME) is False:
            raise ConfigFileNotFoundError('Configuration file "pypacking.ini" not found')

        project_config = ConfigParser()
        project_config.read(CONFIG_FILENAME)

        try:
            project_info = project_config['INFO']
            package_info = project_config['PACKAGE']
        except KeyError:
            raise InvalidConfigFileError('Default settings not found')

        self.author_name = project_info.get('authorName')
        self.author_email = project_info.get('authorEmail') 
        self.project_name = project_info.get('projectName')
        self.project_version = project_info.get('version')
        self.project_description = project_info.get('description')

        self.package_path = package_info.get('packagePath')

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
        author_name: str,
        author_email: str,
        project_name: str,
        description: str,
        version: str,
        package_path: str,
        script_entry: str = None
    ) -> None:
        config = ConfigParser()

        config['INFO'] = {
            'authorName': author_name,
            'authorEmail': author_email,
            'projectName': project_name,
            'description': description,
            'version': version
        }

        config['PACKAGE'] = {
            'packagePath': package_path,
        }

        if script_entry:
            config['PACKAGE']['scriptEntry'] = script_entry

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

            if modified_files:
                print(f'{len(modified_files)} files were changed. Copying...')

                for file in modified_files:
                    filepath = os.path.join('build', file)
                    print(f'Removing {file} from build/ directory...')
                    os.remove(filepath)
                    print(f'Copying {file} to build/{self.package_path} directory...', end='')
                    shutil.copyfile(file, filepath)
                    print('done')
            else:
                print('No files changed.')
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

    def _install_library(self, project_name: str, package_path: str) -> None:
        print(f'\tThe package will be saved in "{SITE_PACKAGES_PATH}"')
        
        print('\tUnpack package...', end='')
        shutil.unpack_archive(package_path, SITE_PACKAGES_PATH, format='zip')
        print('done')
        print('\tRename configuration file...', end='')

        config_filename = os.path.join(SITE_PACKAGES_PATH, CONFIG_FILENAME)
        config_package_filename = os.path.join(SITE_PACKAGES_PATH, f'{project_name}.ini')
        os.rename(config_filename, config_package_filename)
        print('done')

    def _install_script(self, package_name: str, script_entry: str) -> None:
        # script entry format: <command name>:<file>:<function (without parentheses)>
        # example: pysgi:main:run

        script_dst = os.path.join(LOCAL_PATH, 'bin')
        command, file, function = script_entry.split(':')

        print(f'\tCreating a script for the command "{command}"...')
        
        if _virtual_env:
            script = f'#!{LOCAL_PATH}/bin/python3\n'
        else:
            script = '#!/usr/bin/python3\n'

        script += f'from {package_name}.{file} import {function}\n\n'
        script += f'_call_fc = {function}()\n'
        script += 'exit(_call_fc)\n'

        entry_filename = os.path.join(script_dst, command)

        with open(entry_filename, 'w') as entry_script:
            entry_script.write(script)

        print('\tGiving execute permission to the script...')
        os.system(f'chmod +x {entry_filename}')
        print('\tScript created.')

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
        script_entry = package_info.get('scriptEntry')

        print(f'Installing {name} in {version} version...')
        self._install_library(name, package_path)

        if script_entry:
            self._install_script(package_info['packagePath'], script_entry)

        print(f'Package \033[1m{name}\033[m successfully installed!')

    @staticmethod
    def list_packages() -> dict:
        packages_path = os.listdir(SITE_PACKAGES_PATH)
        all_packages = {}

        for p in packages_path:
            if p.endswith('.ini'):
                full_filepath = os.path.join(SITE_PACKAGES_PATH, p)
                config = ConfigParser()
                config.read(full_filepath)

                package_config = {}
                package_config.update(dict(config['PACKAGE']))
                package_config.update(dict(config['INFO']))

                all_packages[config['INFO']['projectName']] = package_config

        return all_packages

    def uninstall(self, project_name: str) -> None:
        all_packages = self.list_packages()
        selected_package = all_packages.get(project_name)

        if selected_package:
            package_name = selected_package['packagepath']
            package_version = selected_package['version']

            print(f'Uninstalling package {package_name} in version {package_version}...')
            print(f'Removing from lib/ directory...', end='')

            package_path = os.path.join(SITE_PACKAGES_PATH, package_name)
            shutil.rmtree(package_path)
            print('done')

            script_entry = selected_package.get('scriptentry')

            if script_entry:
                print('Removing from bin/ directory...', end='')
                command_name = script_entry.split(':')[0]
                script_path = os.path.join(LOCAL_PATH, 'bin', command_name)
                os.remove(script_path)
                print('done')

            print('Removing package configuration file...', end='')
            config_filepath = os.path.join(SITE_PACKAGES_PATH, f'{project_name}.ini')
            os.remove(config_filepath)
            print('done')
        else:
            print(f'\033[31mPackage "{project_name}" not found.\033[m')
