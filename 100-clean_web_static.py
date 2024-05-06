#!/usr/bin/env python3
"""
Deletes out-of-date archives.

Execute file using:
    fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u
    ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

env.hosts = ['54.208.215.244', '54.144.146.48']

def do_clean(number=1):
    """
    Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep.
        If number is 0 or 1, keeps only the most recent archive.
        If number is 2, keeps the most and second-most recent archives, etc.
    """
    number = max(int(number), 1)

    # Delete local archives
    with lcd("versions"):
        local_archives = sorted(os.listdir())
        for archive in local_archives[:-number]:
            local(f"rm ./{archive}")

    # Delete remote archives
    with cd("/data/web_static/releases"):
        remote_archives = sorted(run("ls -tr").split())
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        for archive in remote_archives[:-number]:
            run(f"rm -rf ./{archive}")
