#!/usr/bin/env python
''''
This tiny program looks at all the test files in gluster/tests and puts them in
separate chunks for parallel execution.
'''


from collections import defaultdict
import os.path
import os
import subprocess


JENKINS_URL = 'https://build.gluster.org'
JENKINS_MAX = 100
PATH_TO_GLUSTER = '../glusterfs'
NUMBER_OF_CHUNKS = 10


def get_all_tests(path):
    '''
    Returns a list of paths to .t files. Needs path to glusterfs checkout
    '''
    path = os.path.normpath(path)
    test_files = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.t'):
                test_files.append(os.path.relpath(os.path.join(root, f),
                                                  path))
    return test_files


def get_disabled_tests(path):
    '''
    Returns a list of tests that are disabled.
    '''
    path = os.path.normpath(path)
    disabled_tests = []
    excluded_tests = subprocess.check_output(
        ['grep', '-rl', 'G_TESTDEF_TEST_STATUS_CENTOS6=BAD_TEST', 'tests'],
        cwd=path
    )
    for line in excluded_tests.split('\n'):
        disabled_tests.append(line)
    return disabled_tests


def split_into_x_chunks(tests, chunks):
    '''
    Take the entire list of tests and split them into as many chunks as
    requested.
    '''
    chunked = defaultdict(list)
    for i in range(0, len(tests)):
        chunked[i % chunks].append(tests[i])
    return dict(chunked)


def main():
    '''
    Put everything together
    '''
    disabled_tests = get_disabled_tests(PATH_TO_GLUSTER)
    tests = get_all_tests(PATH_TO_GLUSTER)
    tests = list(set(tests) - set(disabled_tests))
    # Put snapshot tests into one chunk since it's going to run outside docker
    chunked_tests = split_into_x_chunks(tests, 10)
    for chunk, content in chunked_tests.items():
        with open('qa/chunks/' + str(chunk) + '.txt', 'w') as f:
            f.write(' '.join(content))


if __name__ == '__main__':
    main()
