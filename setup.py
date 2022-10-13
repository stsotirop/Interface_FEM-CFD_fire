import datetime

from setuptools import setup, find_packages
from pip._internal.req import parse_requirements


# Function to load requirements from file
def load_requirements(fname):
    return [
        req.requirement
        for req
        in parse_requirements(fname, session=False)
    ]


# Load requirements from .txt
requirements = load_requirements("requirements.txt")

# Run setuptools setup
setup(
    name='CFD-FEM',
    version='1.0.0',
    description='File transportations',
    author='stef',
    author_email='stef.com',
    url='stef',
    license=f'Copyright {datetime.date.today().year} stef, All rights reserved.',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'CFD-FEM = main_gui:run', # Function to start the app
        ],
    },
    packages=find_packages(exclude=['tests']),
    package_data={
        # 'py_oma.sources': ['*.*'], # Declare folder
        'computation_core': ['*.ui', '*/*'] # Declare extra type of files, everything of py_oma
    }
)
