from hashlib import md5
import os
import shutil
from configparser import ConfigParser
from typing import Tuple

CONFIG_FILENAME = 'pypacking.ini'


class PyPacking:
    def __init__(self):
        if os.path.isfile(CONFIG_FILENAME) is False:
            raise FileNotFoundError('Configuration file "pypacking.ini" not found')

        project_config = ConfigParser()
        project_config.read(CONFIG_FILENAME)

        project_info = project_config['INFO']
        package_info = project_config['PACKAGE']

        self.project_name = project_info['projectName']
        self.project_version = project_info['version']
        self.project_description = project_info['description']

        self.package_path = package_info['packagePath']

        self.file_hashes = {}
        self._hash_files()

    def _gen_hash(self, filepath: str) -> str:
        with open(filepath, 'rb') as file_read:
            content = file_read.read()
            hashfile = md5(content).hexdigest()

        return hashfile

    @staticmethod
    def make_config(
        project_name: str,
        description: str,
        version: str,
        package_path: str
    ) -> None:
        config = ConfigParser()

        config['INFO'] = {
            'projectName': project_name,
            'description': description,
            'version': version
        }

        config['PACKAGE'] = {
            'packagePath': package_path
        }

        with open(CONFIG_FILENAME, 'w') as file_write:
            config.write(file_write)

    def make_package(self):
        package_name = f'{self.project_name}-{self.project_version}'
        package_dist_path = os.path.join('dist', package_name)

        if os.path.isdir('dist') is False:
            os.mkdir('dist')
        
        if os.path.isdir('build'):
            shutil.rmtree('build')

        shutil.copytree(self.package_path, 'build')
        shutil.copyfile(CONFIG_FILENAME, os.path.join('build', CONFIG_FILENAME))
        shutil.make_archive(package_dist_path, 'zip', 'build')
