
import argparse
from argparse import ArgumentDefaultsHelpFormatter

from zshell import ZShell

class TestHarness:

    def __init__(self, device_under_test:ZShell):
        self.dut = device_under_test
        self.results = {}
        self.failure_log = []

    def test_connect(self):
        result = self.dut.connect()
        self.results.update({"Connect": result})


def main(interface="uart", hwid=None, port=None, serial_no=None):


    dut = ZShell(interface=interface,
                 port=port,
                 hwid=hwid,
                 serial_no=serial_no)

    test_harness = TestHarness(device_under_test=dut)

    test_harness.test_connect()

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
    parser.add_argument("--port",
                        action='store_true',
                        default=None,
                        help="port of UART device")
    parser.add_argument("--hwid",
                        action="store_true",
                        default=None,
                        help="VID:PID (4 digits each) of UART device")
    parser.add_argument("--serial_no",
                        action="store_true",
                        default=None,
                        help="Serial number of UART device")
    args=parser.parse_args()

    main("uart", port="COM4")
