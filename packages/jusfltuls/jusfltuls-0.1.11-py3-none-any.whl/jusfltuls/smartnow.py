#!/usr/bin/env python3
import subprocess as sp
import shlex
from fire import Fire
import os

def main(command="smartnow.sh"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("D... ...", script_dir)
    full_command = os.path.join(script_dir, command)
    print("D... ...", full_command)
    CMD = shlex.split(full_command)
    result = sp.run( CMD, capture_output=True, text=True )
    if result.returncode != 0:
        print("X... error calling", command)
    print(result.stdout ) ####   REPOERT THE OUTPUT
    return
if __name__ == "__main__":
    Fire(main)
