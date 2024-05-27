from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in demowarehouse/__init__.py
from demowarehouse import __version__ as version

setup(
	name="demowarehouse",
	version=version,
	description="Test",
	author="Viral Patel",
	author_email="viral@gmail.ocm",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
