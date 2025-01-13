
import argparse
from argparse import ArgumentDefaultsHelpFormatter
from time import sleep

from zshell import ZShell

class TestHarness:

    def __init__(self, device_under_test:ZShell):
        self.dut = device_under_test
        self.results = {}
        self.failure_log = []

    def test_connect(self):
        result = self.dut.connect()
        self.results.update({"Connect": result})

    def test_write_read(self):
        result = False
        failures = []
        payload = 'help'
        bytes_written = len(payload) + 1  # extra character is for newline \n
        expected_output = 'Please press the <Tab> button to see all available commands.\r\n'

        write_bytes = self.dut.write(payload='help')
        if write_bytes != bytes_written:
            failures.append("Bytes written did not match expected value")

        output = self.dut.read()
        if expected_output not in output:
            failures.append("Unexpected output from read function")

        if not failures:
            result = True

        self.failure_log += failures
        self.results.update({"Write/Read": result})


def main(interface="uart", hwid=None, port=None, serial_no=None):


    dut = ZShell(interface=interface,
                 port=port,
                 hwid=hwid,
                 serial_no=serial_no)

    test_harness = TestHarness(device_under_test=dut)

    test_harness.test_connect()
    test_harness.test_write_read()

    for test in test_harness.results:
        print(f'{test}: {test_harness.results[test]}')

    if all(test_harness.results.values()):
        print("PASS")
    else:
        print("FAIL")
        for failure in test_harness.failure_log:
            print(failure)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="ZShell test harness",
                                     formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p',"--port",
                        default=None,
                        help="port of UART device")
    parser.add_argument('-i',"--hwid",
                        default=None,
                        help="VID:PID (4 digits each) of UART device")
    parser.add_argument('-s',"--serial_no",
                        default=None,
                        help="Serial number of UART device")
    args = parser.parse_args()

    main("uart",
         port=args.port,
         hwid=args.hwid,
         serial_no=args.serial_no)
