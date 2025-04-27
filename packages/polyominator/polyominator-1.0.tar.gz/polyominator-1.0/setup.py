from setuptools import setup, find_packages

import json
import os

def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию"""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]

def read_README():
    """Читаем README.md"""
    filepath = os.path.join(os.path.dirname(__file__), "README.md")
    with open(filepath) as f:
        readme = f.read()
    return readme

if __name__ == '__main__':
    setup(
        name='polyominator',
        version=os.getenv('PACKAGE_VERSION', '1.0'),
        package_dir={'': 'src'},
        packages=find_packages('src'),
        description='Polyomino task solver.',
        install_requires=[
              *read_pipenv_dependencies('Pipfile.lock'),
        ],
        url="https://github.com/KirilinAM/Polyomino-solver",
        long_description=read_README(),  
        long_description_content_type="text/markdown", 
        author="Artem",
        author_email="kirilinartem@yandex.ru"
    )