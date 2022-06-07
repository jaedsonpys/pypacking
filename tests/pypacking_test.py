from pyseqtest import SeqTest
import os
import sys

sys.path.insert(0, './')

from pypacking import PyPacking


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


if __name__ == '__main__':
    PyPackingTest().run()
