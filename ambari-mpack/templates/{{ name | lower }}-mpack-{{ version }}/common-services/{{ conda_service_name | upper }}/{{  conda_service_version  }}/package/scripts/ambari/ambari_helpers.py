import os
import signal

from resource_management import *


def package_dir():
    return os.path.realpath(__file__).split('/package')[0] + '/package/'


def stop(pid_file):
    with open(pid_file, 'r') as fp:
        try:
            os.kill(int(fp.read().strip()), signal.SIGTERM)
        except OSError:
            pass
