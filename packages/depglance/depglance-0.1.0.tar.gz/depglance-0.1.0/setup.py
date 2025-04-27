from setuptools import setup, find_packages

setup(
    name='depglance',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['pyvis', 'requests'],
    entry_points={'console_scripts': ['depglance=depglance.cli:main']},
)
