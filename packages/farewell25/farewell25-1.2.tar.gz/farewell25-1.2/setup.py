from setuptools import setup, find_packages
import os

setup(
    name='farewell25',
    version='1.2',
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files from the package
    package_data={
        'farewell25': ['farewell.mp3', 'farewell.png', 'trigger_farewell.py'],
    },
    entry_points={
        'console_scripts': [
            'farewell25 = farewell25.trigger_farewell:show_farewell',  # This will trigger show_farewell() when executed
        ],
    },
)
