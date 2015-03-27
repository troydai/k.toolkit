#! /usr/bin/env python3

# clean up all the packages

import os
import os.path
import shutil

if os.name == 'nt':
    packages_root = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], '.dnx', 'packages')
elif os.name == 'posix':
    packages_root = os.path.join(os.environ['HOME'], '.dnx', 'packages')

packages_folder = os.listdir(packages_root)

for p in packages_folder:
    print('removing', p)
    shutil.rmtree(os.path.join(packages_root, p))

kpm_cache = os.path.join(os.environ['LocalAppData'], 'kpm', 'cache')
if os.path.exists(kpm_cache):
    print('removing', kpm_cache)
    shutil.rmtree(kpm_cache)

nuget_cache = os.path.join(os.environ['LocalAppData'], 'NuGet', 'Cache')
if os.path.exists(nuget_cache):
    print('removing', nuget_cache)
    shutil.rmtree(nuget_cache)
