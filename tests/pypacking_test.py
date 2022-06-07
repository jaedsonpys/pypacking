from pyseqtest import SeqTest
import os

from pypacking import PyPacking
from pypacking.exceptions import ConfigFileNotFoundError
from pypacking.exceptions import InvalidConfigFileError
from pypacking.exceptions import PackageNotFoundError


class PyPackingTest(SeqTest):
    def __init__(self):
        super().__init__()

    def test_make_config(self):
        pypacking = PyPacking.make_config(
            author_name='Jaedson Silva',
            author_email='imunknowuser@protonmail.com',
            project_name='PyPacking',
            description='Simple description',
            version='1.0.0',
            package_path='pypacking',
            script_entry='pypacking:main:main'
        )

        self.is_true(os.path.isfile('./pypacking.ini'), msg_error='Config file not created')

    def test_read_config(self):
        pypacking = PyPacking()
        pypacking.read_config()

        self.is_true(pypacking.author_name == 'Jaedson Silva', msg_error='Author name wrong')
        self.is_true(pypacking.author_email == 'imunknowuser@protonmail.com', msg_error='Author email wrong')
        self.is_true(pypacking.project_name == 'PyPacking', msg_error='Project name wrong')
        self.is_true(pypacking.project_description == 'Simple description', msg_error='Description wrong')
        self.is_true(pypacking.project_version == '1.0.0', msg_error='Version wrong')
        self.is_true(pypacking.package_path == 'pypacking', msg_error='Package path wrong')


    def test_make_package(self):
        pypacking = PyPacking()
        
        try:
            pypacking.read_config()
        except ConfigFileNotFoundError as error:
            self.is_true(False, msg_error=error.msg)
        except PackageNotFoundError as error:
            self.is_true(False, msg_error=error.msg)
        except InvalidConfigFileError as error:
            self.is_true(False, msg_error=error.msg)

        pypacking.make_package()

        self.is_true(os.path.isdir('build'), msg_error='build/ directory not created')

        # checking build directory
        self.is_true(os.path.isdir('build/pypacking'), msg_error='build/pypacking directory not created')
        self.is_true(os.path.isfile('build/pypacking.ini'), msg_error='build/pypacking.ini file not created')

        self.is_true(os.path.isdir('dist'), msg_error='dist/ directory not created')
        self.is_true(os.path.isfile('dist/PyPacking-1.0.0.zip'), msg_error='Package file not created')


if __name__ == '__main__':
    PyPackingTest().run()
