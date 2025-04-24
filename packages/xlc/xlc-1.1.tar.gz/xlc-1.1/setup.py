# coding=utf-8

import os
import tarfile
from urllib.parse import urljoin

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

from xlc.attribute import __author__
from xlc.attribute import __author_email__
from xlc.attribute import __description__
from xlc.attribute import __project__
from xlc.attribute import __urlhome__
from xlc.attribute import __version__

__urlcode__ = __urlhome__
__urldocs__ = __urlhome__
__urlbugs__ = urljoin(__urlhome__, "issues")


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    return requirements


class CustomInstallCommand(install):
    """Customized setuptools install command"""

    def run(self):
        install.run(self)  # Run the standard installation
        self.unpack_tar_files()  # Unpack all .tar files after installation

    def unpack_tar_files(self):
        install_lib = self.install_lib
        assert isinstance(install_lib, str)
        package_dir = os.path.join(install_lib, "xlc", "database")
        for filename in os.listdir(package_dir):
            if filename.endswith(".tar.xz"):
                tar_path = os.path.join(package_dir, filename)
                with tarfile.open(tar_path, "r:xz") as tar:
                    tar.extractall(path=tar_path[:-7])
                os.remove(tar_path)


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    url=__urlhome__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __urlcode__,
                  "Bug Tracker": __urlbugs__,
                  "Documentation": __urldocs__},
    packages=find_packages(include=["xlc*"], exclude=["xlc.unittest"]),
    package_data={"xlc.database": ["langmark.toml", "langtags.toml", "*.tar.xz"]},  # noqa:E501
    install_requires=all_requirements(),
    cmdclass={
        "install": CustomInstallCommand,
    }
)
