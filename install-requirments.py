import subprocess
import sys
import os


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


with open(os.path.join(sys.path[0], "requirements.txt"), "r", encoding="utf-8") as reqs:
    packages = reqs.readlines()
    for package in packages:
        install(package)

input("Press ENTER to exit")
