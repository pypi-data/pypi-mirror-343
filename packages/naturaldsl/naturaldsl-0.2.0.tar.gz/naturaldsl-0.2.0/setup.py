from setuptools import setup, find_packages

setup(
    name="natural_dsl",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "dask[complete]",
        "seaborn",
        "matplotlib",
        "pandas",
        "numpy",
    ],
    entry_points={
        'console_scripts': [
            'natural-dsl-cli=cli:main',  # This will map the CLI to the 'main' function in 'cli.py'
        ],
    },
    author="Praduman Sharma",
    author_email="prdmn.shrm@gmail.com",
    description="NaturalDSL: A natural programming language for data science",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pradumana/Naturaldsl",  # Update with your actual repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
)
