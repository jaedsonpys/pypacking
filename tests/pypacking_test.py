from pyseqtest import SeqTest
import os
import sys

sys.path.insert(0, './')

from pypacking import PyPacking


class PyPackingTest(SeqTest):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    PyPackingTest().run()
