from setuptools import setup, find_packages


setup(
    name='dianpy',
    description='DianPy a special parser for working with the dian scoreboard',
    version='0.0.2',
    install_requires=[
        'xmlbind>=0.0.5'
    ],
    packages=find_packages()
)
