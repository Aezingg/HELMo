#!/usr/bin/python3
#python3 check_ssh.py user

import sys
from datetime import datetime
import os
try:
    with open(f"/actives/{sys.argv[1]}", "r+") as file_users:
        sys.exit(f"{sys.argv[1]} est déjà connecté")

except FileNotFoundError:
    sys.exit()