import unittest
import os

from HTMLTestRunner import HTMLTestRunner

from unit_tests.configuration import configurationSuite
from unit_tests.work_classes import workClassesSuite


output_dir = os.environ.get('REPORT_OUT_DIR', '/reports')
tester_name = os.environ.get('REPORT_TESTER_NAME', 'robot')
version = os.environ.get('HPE_VERS', 'v0.0.1')

testsSuite = unittest.TestSuite()
testsSuite.addTest(configurationSuite)
testsSuite.addTest(workClassesSuite)

test_runner = HTMLTestRunner(log=True,
                             verbosity=2,
                             output=output_dir,
                             title=f'Test report for helpers_entity:{version}',
                             report_name=version,
                             open_in_browser=False,
                             add_traceback=True,
                             tested_by=tester_name,
                             description=f"Report on unit tests of the helpers_entity:{version}")

test_runner.log_file = f'{output_dir}/unit-tests.log'
test_runner.html_report_file_name = f'{output_dir}/unit-tests.html'


def main():
    test_runner.run(testsSuite)
    