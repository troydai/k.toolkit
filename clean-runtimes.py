#! /usr/bin/env python3

# clean up all the runtime folders

import os
import os.path
import shutil

runtime_root = os.path.join(os.environ['HOME'], '.k', 'runtimes')
runtime_folders = os.listdir(runtime_root)

for r in runtime_folders:
    print('removing', r)
    shutil.rmtree(os.path.join(runtime_root, r))

