#!/usr/bin/env python

from collections import defaultdict
from datetime import datetime, timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os.path
import os
import requests


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
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.t'):
                # test_files.append(os.path.relpath(os.path.join(root, f),
                #                                   path))
                test_files.append(os.path.join(root, f))
    return test_files


def get_snapshot_tests(tests):
    snapshot = []
    for test in tests:
        with open(test) as f:
            if 'snapshot.rc' in f.read():
                snapshot.append(test)
    return snapshot


def get_regression_logs(job='centos6-regression', days=7):
    '''
    Get a list of links to last X days' logs from a Jenkins job
    '''
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    cut_off_date = datetime.today() - timedelta(days=days)
    for page in xrange(0, JENKINS_MAX, 100):
        build_info = requests.get(
                JENKINS_URL +
                '/job/' +
                job +
                '/'
                'api/json?depth=1&tree=allBuilds'
                '[url,result,timestamp,builtOn,actions[value]]'
                '{{{0},{1}}}'.format(page, page+100),
                verify=False).json()
        for build in build_info.get('allBuilds'):
            if datetime.fromtimestamp(build['timestamp']/1000) < cut_off_date:
                # stop when timestamp older than cut off date
                return
            if build['result'] == 'SUCCESS':
                yield build['url'] + 'consoleText'


def fetch_and_parse_timing(url):
    '''
    Fetch a Jenkins build URL, parse the timing, and return a list of list of
    timing
    '''
    text = requests.get(url, verify=False).text
    text = text.split('Tests ordered by time taken, slowest to fastest:')
    timing = []
    for line in text[1].split('\n'):
        if line.startswith('./tests'):
            timing.append(parse_timing_line(line))
    return timing


def parse_timing_line(line):
    '''
    Take a line of test timing info and split out a dict, one text and one
    integer of timing
    '''
    return (
            line.split(' - ')[0].strip(),
            int(line.split(' - ')[1].strip().split('second')[0])
    )

def split_into_x_chunks(tests, snapshot, chunks):
    chunked = defaultdict(list)
    # Put the snapshot tests in chunk 0
    chunked[0] = snapshot
    chunk = 1
    for i in range(0, len(tests)):
        chunked[chunk].append(tests[i])
        chunk += 1
        # Make sure that that chunk 0 is not filled until every other chunk has
        # the same number of tests as it does.
        if chunk == chunks:
            if len(chunked[chunk-1]) < len(chunked[0]):
                chunk = 1
            else:
                chunk = 0
    return dict(chunked)


def main():
    tests = get_all_tests('../glusterfs/')
    # Put snapshot tests into one chunk since it's going to run outside docker
    snapshot_tests = get_snapshot_tests(tests)
    tests = list(set(tests) - set(snapshot_tests))
    chunked_tests = split_into_x_chunks(tests, snapshot_tests, 10)
    for k, v in chunked_tests.items():
        print len(v)


if __name__ == '__main__':
    main()
