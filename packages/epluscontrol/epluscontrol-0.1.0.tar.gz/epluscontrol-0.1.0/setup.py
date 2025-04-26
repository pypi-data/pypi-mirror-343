from setuptools import setup, find_packages

setup(
    packages=find_packages(include=['epluscontrol', 'epluscontrol.*']),
    include_package_data=True,
)