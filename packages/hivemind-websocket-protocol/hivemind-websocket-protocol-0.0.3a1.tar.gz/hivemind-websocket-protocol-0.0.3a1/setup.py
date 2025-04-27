import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of the package"""
    version_file = os.path.join(BASEDIR, 'hivemind_websocket_protocol', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if int(alpha) > 0:
        version += f"a{alpha}"
    return version


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


PLUGIN_ENTRY_POINT = 'hivemind-websocket-plugin=hivemind_websocket_protocol:HiveMindWebsocketProtocol'

setup(
    name='hivemind-websocket-protocol',
    version=get_version(),
    packages=['hivemind_websocket_protocol'],
    url='https://github.com/JarbasHiveMind/hivemind-websocket-protocol',
    license='Apache-2.0',
    author='jarbasAi',
    install_requires=required("requirements.txt"),
    entry_points={'hivemind.network.protocol': PLUGIN_ENTRY_POINT},
    author_email='jarbasai@mailfence.com',
    description='websocket network protocol for hivemind-core'
)
