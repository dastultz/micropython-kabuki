#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import argparse
import os
import sys
import subprocess

cmd_parser = argparse.ArgumentParser(description="Install Kabuki to pyboard.")
cmd_parser.add_argument("-p", "--path", default="/Volumes/PYBOARD", help="the mount point of the pyboard")
args = cmd_parser.parse_args()

mount_point = args.path

if not os.path.isdir(mount_point):
    print("Pyboard is not mounted")
    sys.exit()

rsync = "rsync -ravzLq --delete --exclude=*.pyc --exclude=*py.class"
# lib directory
subprocess.check_call("{} --exclude=pyb.py --include=*.py lib {}".format(rsync, mount_point), shell=True)
# kabuki to lib
subprocess.check_call("{} kabuki {}/lib".format(rsync, mount_point), shell=True)
# main.py
main_py_path = mount_point + "/main.py"
target = open(main_py_path, 'w')
target.truncate()
target.write("from kabuki.pyboard import runner\n\n")
target.write("runner.run()\n")
target.close()


