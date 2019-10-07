#!./base/lib/py

from __future__ import with_statement

import os
import sys
import cPickle as pickle
import pprint

import kernel
from kernel.config import config

def main():
    # Before doing anything we need to initialize the package system.  Among
    # other things, this loads all the modules and registers all the custom
    # DataType objects from types.ini.
    kernel.packages.init_packages()

    cacheDir = config.get("DEFAULT", "CACHE_DIR")
    
    # Some basic checking of command line arguments.
    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]
        
        if not os.path.isabs(path):
            path = os.path.join(cacheDir, path)
            
        if not path.endswith(".pkl"):
            path += ".pkl"
        
        if not os.path.exists(path):
            path = None

    if not path:
        usage()
        return

    # This is the important bit: read the binary data from the pickle file,
    # unpickle it, and pretty-print it.
    with open(path, 'rb') as f:
        data = f.read()
        obj = pickle.loads(data)
        # Try to simplify the object if it supports it.  This is because 
        # kernel.structure.Structure objects don't pretty-print well, but
        # simplifying them turns them into normal Python dicts that contain
        # all the same information.
        if hasattr(obj, 'simplify'):
            obj = obj.simplify()
        pprint.pprint(obj)

def usage():
    print """dump_pkl.py
    Usage:
        dump_pkl <path/to/file.pkl>
    """

if __name__ == '__main__':
    main()
