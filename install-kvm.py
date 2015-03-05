#!/usr/bin/env python3

import os
import os.path
import sys
import requests

def download(template, branch, filename, bin_folder):
    r = requests.get(template.format(branch, filename))
    with open(os.path.join(bin_folder, filename), 'w') as file_:
        file_.write(r.text)

print("Install kvm")

if os.name != 'nt':
    print("not implemented for non-Windows os.")
    sys.exit(1) 

dotk_dir = os.path.join(os.environ['USERPROFILE'], '.k')
dotk_bin = os.path.join(dotk_dir, 'bin')

if not os.path.exists(dotk_bin):
    os.mkdir(dotk_bin)

# {0} - branch, {1} - kvm.ps1|kvm.cmd
url_template = 'https://raw.githubusercontent.com/aspnet/dotnetsdk/{0}/src/{1}'

download(url_template, 'dev', 'kvm.cmd', dotk_bin)
download(url_template, 'dev', 'kvm.ps1', dotk_bin)

found = False
current_paths = os.environ['PATH'].split(';')
for path in current_paths:
    if path == dotk_bin:
        found = True
        break

if not found:
    current_paths.append(dotk_bin)
    paths_string = ';'.join(current_paths)
    os.system('setx PATH "{0}"'.format(paths_string))
