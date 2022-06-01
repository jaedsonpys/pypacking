import os
import shutil
from configparser import ConfigParser
from hashlib import md5

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
        build_filepath = os.path.join('build', self.package_path)

        modified_files = []
        first_build = True

        if os.path.isdir('dist') is False:
            os.mkdir('dist')
        
        if os.path.isdir('build'):
            first_build = False

        if not first_build:
            for filepath, previous_hash in self.file_hashes.items():
                new_hash = self._gen_hash(filepath)

                if new_hash != previous_hash:
                    self.file_hashes[filepath] = new_hash
                    modified_files.append(filepath)

            for file in modified_files:
                filepath = os.path.join('build', file)
                os.remove(filepath)
                shutil.copyfile(file, filepath)
        else:
            shutil.copytree(self.package_path, build_filepath)

        shutil.copyfile(CONFIG_FILENAME, os.path.join(build_filepath, CONFIG_FILENAME))
        shutil.make_archive(package_dist_path, 'zip', 'build')
