from setuptools import setup, find_packages

setup(
    name='pakku',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'requests',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'pakku = pakku.main:main',
        ],
    },
    author='AlphaDarkmoon',
    description='A lightweight Feature Rich Python package manager with GUI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AlphaDarkmoon/pakku',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

