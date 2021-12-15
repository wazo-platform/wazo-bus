from setuptools import setup

setup(
    name='bus-test',
    version='0.1',
    packages=['bus_test'],
    include_package_data=True,
    install_requires=[
        'flask', 'kombu'
    ],
)
