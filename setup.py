from setuptools import setup, find_packages
import os

def get_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
             paths.append(os.path.join('..', path, filename))
    return paths

def readme():
    with open('README.rst') as f:
        return f.read()

static_files = get_files('recipebox/static')
template_files = get_files('recipebox/templates')

setup(
    name="recipebox",
    version='0.1.0',
    platforms="all",
    long_description=readme(),
    packages=find_packages(),
    package_data={
        "": static_files + template_files
    },
    author="Jeff Caffrey-Hill",
    author_email="jeff@reverentengineer.com",
    install_requires=(
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Login'
    ),
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest'
    ],
)
