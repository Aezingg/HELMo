#!/usr/bin/python3
#python3 cascade.py user hostname

import sys
try:
    with open(f"/actives/{sys.argv[1]}", "r+") as file_users:
        content = file_users.read()
        if sys.argv[2] in content:
            sys.exit()
        else:
            sys.exit(f"{sys.argv[1]} est déjà connecté sur la machine {sys.argv[2]}")

except FileNotFoundError:
    sys.exit()