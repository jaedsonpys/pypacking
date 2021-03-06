from pypacking import PyPacking
from pypacking import __version__

import shutil

# generating config
print('Creating "pypacking.ini" file...')

PyPacking.make_config(
    author_name='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    project_name='PyPacking',
    description='PyPacking python package manager',
    version=__version__,
    package_path='pypacking',
    script_entry='pypacking:main:main'
)

pypacking = PyPacking()
pypacking.read_config()

# making package
print('Make package...')
pypacking.make_package()

# install package
print(f'Install PyPacking {__version__}...')
pypacking.install(f'dist/PyPacking-{__version__}.zip')

# clear build and dist directory
print('Clear build/ and dist/ directory...')
shutil.rmtree('dist', ignore_errors=True)
shutil.rmtree('build', ignore_errors=True)

print('Installation completed. All very well.')
