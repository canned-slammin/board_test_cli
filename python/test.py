
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

    def test_write_read(self):
        result = False
        failures = []
        payload = 'help'
        bytes_written = len(payload) + 1  # extra character is for newline \n
        expected_output = 'Please press the <Tab> button to see all available commands.\r\n'

        write_bytes = self.dut.write(payload=payload)
        if write_bytes != bytes_written:
            failures.append("Bytes written did not match expected value")

        output = self.dut.read()
        if expected_output not in output:
            failures.append("Unexpected output from read function")

        if not failures:
            result = True

        self.failure_log += failures
        self.results.update({"Write/Read": result})

    def test_gpio_conf(self, num_pins: int, dev: str):
        test_result = False
        failures = []

        print(f'GPIO device: {dev}')  # TODO debug
        result, output = self.dut.gpio_conf(device=dev, pin=0, init='1')

        #TODO test incorrect parameter - purpose FALSE
        #TODO test incorrect parameter - pull FALSE
        #TODO test incorrect parameter - active FALSE
        #TODO test incorrect parameter - init FALSE
        for pin in range(num_pins): # TODO why is this so slow? i suspect read() is timing out every time
        #TODO test no parameters TRUE
            result, output = self.dut.gpio_conf(device=dev, pin=pin)
            print(f'{result=}\n{output=}')
            # test configure input
            ##TODO test configure pull up TRUE
            ##TODO test configure pull down TRUE
            ##TODO test configure active high TRUE?
            ##TODO test configure active low TRUE?
            ##TODO test configure init 0 FALSE
            ##TODO test configure init 1 FALSE
            ## test configure output
            ## TODO test configure pull up TRUE?
            ## TODO test configure pull down TRUE?
            ## TODO test configure active high FALSE?
            ## TODO test configure active low FALSE?
            ## TODO test configure init 0 TRUE
            ## TODO test configure init 1 TRUE


        failures.append('GPIO configure not yet implemented')

        self.failure_log += failures
        self.results.update({"GPIO Configure": test_result})



def main(num_pins: int,
         gpio_device: str,
         interface="uart",
         hwid=None,
         port=None,
         serial_no=None):


    dut = ZShell(interface=interface,
                 port=port,
                 hwid=hwid,
                 serial_no=serial_no)

    test_harness = TestHarness(device_under_test=dut)

    test_harness.test_connect()
    test_harness.test_write_read()
    test_harness.test_gpio_conf(num_pins=int(num_pins), dev=gpio_device)

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
    parser.add_argument('-g', '--gpio-pins',
                        default=None,
                        help="Number of GPIO pins to test")
    parser.add_argument('-gd', '--gpio-device',
                        default=None,
                        help='GPIO device tree name (ex. gpio@50000000')
    args = parser.parse_args()

    main(num_pins=args.gpio_pins,
         gpio_device=args.gpio_device,
         interface="uart",
         port=args.port,
         hwid=args.hwid,
         serial_no=args.serial_no)
