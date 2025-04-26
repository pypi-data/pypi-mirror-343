from setuptools import setup, find_packages

setup(
    packages=find_packages(include=[
        'epluscontrol', 
        'epluscontrol.*', 
        'epluscontrol.energyplus.*',
	'epluscontrol.energyplus.utils.*']),
    include_package_data=True,
)