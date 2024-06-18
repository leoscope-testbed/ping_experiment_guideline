from datetime import datetime
import yaml
import argparse
import time 
import importlib
from random import shuffle
from numpy import random

'''
Example execution: python -m leotest --test-config leotest-config.yaml
'''

def run_test(testname, config):
    runner = config['tests'][testname]['runner']
    test_module = importlib.import_module(
                                'leotest.runners.{}'
                                .format(runner))

    test_ep = getattr(test_module, config["tests"][testname]["entry_point"])

    test = test_ep(testname=testname, config=config, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None) 

    print('Starting test \'' + str(testname) + '\'..')
    output = test.start_test()
    print(output)
    print('Test \'' + str(testname) + '\' completed.')
    test.stop_test()
    test.teardown()

def run_tests_once(config):
    testnames = [testname for testname in config['tests']]
    shuffle(testnames)
    for testname in testnames:
        runner = config['tests'][testname]['runner']
        print('running %s with runner %s' % (testname, runner))
        run_test(testname, config)
        time.sleep(30)

def run_tests(config, once = False):

    if once:
        run_tests_once(config)
    else:
        interval_min = config['schedule']['interval']['min']
        interval_max = config['schedule']['interval']['max']
        while True: 
            run_tests_once(config)
            sleeptime = random.uniform(interval_min, interval_max)
            print('Sleeping for %d seconds' % (sleeptime))
            time.sleep(sleeptime)

def main():

    parser = argparse.ArgumentParser(description='Leotest')
    parser.add_argument('--test-config', type=str, default="", metavar='N',
                        help='Path to yaml configuration file')

    args = parser.parse_args()

    with open(args.test_config, 'r') as stream:
        config = yaml.safe_load(stream)

    print(config)
    run_tests(config, once = True)

if __name__ == "__main__":
    main()