import json
import os
import pathlib
import platform
import sys

from __init__ import File

with open(pathlib.Path(__file__).parent.parent / 'metadata.json') as f:
    _METADATA = json.load(f)
    __version__ = _METADATA['version']
    __author__ = _METADATA['authors']
    __description__ = _METADATA['description']


def version():
    print('SecuredFiles version {version} on {os} {os_release} ({os_version})'.format(
        version=__version__,
        os=platform.system(),
        os_release=platform.release(),
        os_version=platform.version(),
    ))


def help_message():
    version()
    print("\nUsage:")
    print('py' if os.name == 'nt' else 'python3', end='')
    print(" -m SecuredFiles [options] <read | lock | unlock> <filepath>\n")
    print("Description:")
    print("\t{}\n".format(__description__))
    print("Options:")
    print("\t-h, --help     Display this help message and exit.")
    print("\t-v, --version  Display the version and exit.")


if __name__ == '__main__':
    """
    This script allows you to retrieve decrypted file data from a terminal.
    """
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['-h', '--help']:
        help_message()
    elif len(sys.argv) > 1 and sys.argv[1].lower() in ['-v', '--version']:
        version()
    elif len(sys.argv) > 2:
        files = [File(path) for path in sys.argv[2:]]
        if sys.argv[1].lower() == 'read':
            for file in files:
                print(file.path.name, ':', file.data)
        elif sys.argv[1].lower() == 'lock':
            for file in files:
                try:
                    file = file.lock()
                    print(file.path.name, ': LOCKED')
                except PermissionError as ae:
                    print(file.path.name, ': {} - {}'.format(type(ae).__name__, ae))
        elif sys.argv[1].lower() == 'unlock':
            for file in files:
                try:
                    file = file.unlock()
                    print(file.path.name, ': UNLOCKED')
                except PermissionError as ae:
                    print(file.path.name, ': {} - {}'.format(type(ae).__name__, ae))
        else:
            help_message()
    else:
        help_message()
