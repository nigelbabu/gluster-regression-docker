#!/usr/bin/env python

from collections import defaultdict
import os.path
import os


def get_all_tests(path):
    '''
    Returns a list of paths to .t files. Needs path to glusterfs checkout
    '''
    path = os.path.normpath(path)
    test_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.t'):
                 #test_files.append(os.path.relpath(os.path.join(root, f), path))
                 test_files.append(os.path.join(root, f))
    return test_files


def get_snapshot_tests(tests):
    snapshot = []
    for test in tests:
        with open(test) as f:
            if 'snapshot.rc' in f.read():
                snapshot.append(test)
    return snapshot


# Variables
path_to_gluster = '../glusterfs')
total_chunks = 5

tests = get_all_tests('../glusterfs/')
chunks = defaultdict(list)
chunks[0] = get_snapshot_tests(tests)
tests = list(set(tests) - set(chunks[0]))


# Get all the tests
# One chunck with all snapshot tests
# Document all slow tests (for now slower than 120 seconds)
# Put everything else into multiple chunks
#
