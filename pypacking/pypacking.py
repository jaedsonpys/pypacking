from configparser import ConfigParser

CONFIG_FILENAME = 'pypacking.ini'


class PyPacking:
    def __init__(self):
        project_config = ConfigParser()
        project_config.read(CONFIG_FILENAME)

        project_info = project_config['INFO']
        package_info = project_config['PACKAGE']

        self.project_name = project_info['projectName']
        self.project_version = project_info['version']
        self.project_description = project_info['description']

        self.package_path = package_info['packagePath']

    def make_config(
        self,
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
