#! /usr/bin/env python3

# clean up all the packages

import os
import os.path
import shutil

packages_root = os.path.join(os.environ['HOME'], '.k', 'packages')
packages_folder = os.listdir(packages_root)

for p in packages_folder:
    print('removing', p)
    shutil.rmtree(os.path.join(packages_root, p))

