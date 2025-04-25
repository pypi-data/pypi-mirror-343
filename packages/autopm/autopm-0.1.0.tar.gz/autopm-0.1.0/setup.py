from setuptools import setup, find_packages

setup(
    name='autopm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        "importlib-metadata; python_version<'3.8'",
    ],
    entry_points={
        'console_scripts': [
            'autopm=autopm.cli:main'
        ]
    },
    author='Saptarshi',
    description='Auto-tracking Python package manager',
    python_requires='>=3.6'
)