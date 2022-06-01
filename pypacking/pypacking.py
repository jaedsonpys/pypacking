from configparser import ConfigParser
import os

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

    @staticmethod
    def make_config(
        projectName: str,
        description: str,
        version: str,
        packagePath: str
    ) -> None:
        config = ConfigParser()

        config['INFO'] = {
            'projectName': projectName,
            'description': description,
            'version': version
        }

        config['PACKAGE'] = {
            'packagePath': packagePath
        }

        with open(CONFIG_FILENAME, 'w') as file_write:
            config.write(file_write)
