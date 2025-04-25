from setuptools import setup, find_packages

setup(
    name='naturaldsl',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'dask[complete]',
        'lark-parser',
        'pandas',
        'numpy',
        'matplotlib',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'naturaldsl=naturaldsl.interpreter:main',  # Assuming the main function is in interpreter.py
        ],
    },
)
