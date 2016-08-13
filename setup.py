'''Setup script for dotbagit-python'''


from setuptools import setup, find_packages

setup (
    name='dotbagit',
    version='0.1',
    url='https://github.com/rjeschmi/dotbagit-python',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dotbagit = dotbagit.cli:main',
        ]
    },
)
