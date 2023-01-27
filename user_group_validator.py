#Tool to validate if any membership group is missing for a server

#!/usr/bin/python3.9

import os,sys
from datetime import datetime
import subprocess

#shell command lines passed as arguments to be passed into subprocess

clush_bin="/usr/bin/clush"
clush_sw="-w"
clush_opt="nodename[001-050]"
clush_cmd="id"
clush_cmd_arg1="target_groupname"

clush = subprocess.Popen([clush_bin,clush_sw,clush_opt,clush_cmd,clush_cmd_arg1], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

id_lst = []


# opens communication with target hosts to query group membership data for each host and store data in memory

try:
    outs, errs = clush.communicate(timeout=10)
    id_lst = outs
except TimeoutExpired:
    clush.kill()

#creates dictionary list with host as key and item as membership group list for a host

hosts = {}

for line in id_lst.splitlines():
    print(line)
    host =  (line.split())
    hosts[host[0][:-1]] = host[3]

# write log file for host with missing 1 or more groups

def writelog(output):
    with open("log.txt", "a") as file_object:
        file_object.write(output)


all_groups = ['1126(gu)', '4085(group1)','2218(group2)','3967(group3)'] #expected membership group for all servers

#Validating if all expected groups exist for a host

def validation():
    flag=True
    for key, groups  in hosts.items():
        for group in all_groups:
            if group not in groups:
		# Display server's actual group membership
                trouble_host=("Host "+ str(key) +" missing one or more groups! " + groups)
                writelog(str(datetime.now()) + "  ")
                writelog(trouble_host + "\n")
                flag=False
                continue
    return flag

value = validation()
if(value is True):
    print(0)
else:
    print(2)

#lets shell know if it failed
if not value:
    sys.exit(2)
