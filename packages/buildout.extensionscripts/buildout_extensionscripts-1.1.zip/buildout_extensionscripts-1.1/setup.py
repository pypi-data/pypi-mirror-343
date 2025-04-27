from setuptools import setup

setup(
    name='buildout.extensionscripts',
    description='Use simple python scripts as zc.buildout extensions',
    long_description=open('README.rst').read(),
    version='1.1',
    packages=['buildout', 'buildout.extensionscripts'],
    namespace_packages=['buildout'],
    install_requires=['setuptools'],
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Buildout"],
    license='BSD',
    entry_points={
        'zc.buildout.extension':
            ['default = buildout.extensionscripts:extension']})
