
import argparse
from argparse import ArgumentDefaultsHelpFormatter

from zshell import ZShell

def test_connect():
    print('not yet implemented')
    return False

def run_tests(interface="uart", hwid=None, port=None, serial_no=None):
    failures = []

    if interface.lower() != 'uart' and interface.lower() != 'rtt':
        failures.append(f'interface "{interface}" not recognized')
        return failures

    dut = ZShell(interface=interface,
                 port=port,
                 hwid=hwid,
                 serial_no=serial_no)

    if not test_connect():
        failures.append(f'connect function failed')
        return failures

def main(interface="uart", hwid=None, port=None, serial_no=None):
    failures = run_tests(interface=interface,
                         hwid=hwid,
                         port=port,
                         serial_no=serial_no)
    if not failures:
        print('Test Pass')
    else:
        print('Test Failed')
        for failure in failures:
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

    main("uart")
