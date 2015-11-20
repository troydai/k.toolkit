#! /usr/bin/env python3

# clean up all the packages

import os
import os.path
import shutil

def deleteResolution(function, path, excinfo):
    print('issue hit during deleting file {0}'.format(path))

# removing packages
if os.name == 'nt':
    packages_root = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], '.dnx', 'packages')
elif os.name == 'posix':
    packages_root = os.path.join(os.environ['HOME'], '.dnx', 'packages')

packages_folder = os.listdir(packages_root)

for p in packages_folder:
    print('removing', p)
    shutil.rmtree(os.path.join(packages_root, p), False, deleteResolution)

# clean kpm/dnu caches
if os.name == 'nt':
    local_app_data = os.environ['LocalAppData']
elif os.name == 'posix':
    local_app_data = '~/.local/share/'

dnu_cache = os.path.join(local_app_data, 'dnu', 'cache')
if os.path.exists(dnu_cache):
    print('removing', dnu_cache)
    shutil.rmtree(dnu_cache, False, deleteResolution)

nuget_cache = os.path.join(local_app_data, 'NuGet', 'Cache')
if os.path.exists(nuget_cache):
    print('removing', nuget_cache)
    shutil.rmtree(nuget_cache)
