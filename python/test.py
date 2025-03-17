
import argparse
from argparse import ArgumentDefaultsHelpFormatter
import time

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
            failures.append(f"Unexpected output from read function: {output}")

        if not failures:
            result = True

        self.failure_log += failures
        self.results.update({"Write/Read": result})

    def test_send_command(self):
        test_result = False
        failures = []
        cmd = "help"
        expected_output = 'Please press the <Tab> button to see all available commands.\r\n'

        output = self.dut.send_command(cmd)

        if expected_output not in output:
            failures.append(f"Unexpected output from read function: {output}")

        if not failures:
            test_result = True

        self.failure_log += failures
        self.results.update({"Send Command": test_result})

    def test_gpio_conf(self, num_pins: int, dev: str):
        test_result = False
        failures = []

        # test incorrect parameter - purpose FALSE
        try:
            result, output = self.dut.gpio_conf(device=dev, pin=0, purpose='foo')
            if result:
                failures.append('Failed to raise exception for invalid purpose')
        except Exception: # this is a hokey way of doing this
            pass

        # test incorrect parameter - pull FALSE
        try:
            result, output = self.dut.gpio_conf(device=dev, pin=0, pull='foo')
            if result:
                failures.append('Failed to raise exception for invalid pull direction')
        except Exception: # this is a hokey way of doing this
            pass

        # test incorrect parameter - active FALSE
        try:
            result, output = self.dut.gpio_conf(device=dev, pin=0, active='foo')
            if result:
                failures.append('Failed to raise exception for invalid active parameter')
        except Exception: # this is a hokey way of doing this
            pass

        # test incorrect parameter - init FALSE
        try:
            result, output = self.dut.gpio_conf(device=dev, pin=0, init='foo')
            if result:
                failures.append('Failed to raise exception for invalid active parameter')
        except Exception: # this is a hokey way of doing this
            pass


        for pin in range(num_pins):
            # TODO debug
            #print(f'Testing gpio_conf on pin {pin}')
            # TODO freezes on pin 11 input when commands run manually
            # TODO also 12, 13, 14... maybe everything higher than 10?
            # TODO that means this test is flawed - fail if timeout maybe?

            # test no parameters TRUE
            result, output = self.dut.gpio_conf(device=dev, pin=pin)
            if not result:
                msg = f'gpio_conf() failed with no parameters pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            # test configure inputs
            ## test configure pull ups TRUE
            result, output = self.dut.gpio_conf(device=dev, pin=pin, pull='up')
            if not result:
                msg = f'gpio_conf() input failed with pull="up" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test configure pull down TRUE
            result, output = self.dut.gpio_conf(device=dev, purpose='input', pin=pin, pull='down')
            if not result:
                msg = f'gpio_conf() input failed with pull="down" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test configure active high TRUE
            result, output = self.dut.gpio_conf(device=dev, pin=pin, active='high')
            if not result:
                msg = f'gpio_conf() input failed with active="high" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test configure active low TRUE
            result, output = self.dut.gpio_conf(device=dev, pin=pin, active='low')
            if not result:
                msg = f'gpio_conf() input failed with active="low" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test multiple input parameters
            result, output = self.dut.gpio_conf(device=dev, purpose='input', pin=pin, active='high', pull='down')
            if not result:
                msg = f'gpio_conf() input failed with active="high" and pull="down" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            # test configure outputs
            ## test configure pull up TRUE?
            result, output = self.dut.gpio_conf(device=dev, purpose='output', pin=pin, pull='up')
            if not result:
                msg = f'gpio_conf() output failed with pull="up" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test configure pull down TRUE?
            result, output = self.dut.gpio_conf(device=dev, purpose='output', pin=pin, pull='down')
            if not result:
                msg = f'gpio_conf() output failed with pull="down" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test configure init 0 TRUE
            result, output = self.dut.gpio_conf(device=dev, purpose='output', pin=pin, init='0')
            if not result:
                msg = f'gpio_conf() output failed with init="0" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test configure init 1 TRUE
            result, output = self.dut.gpio_conf(device=dev, purpose='output', pin=pin, init='1')
            if not result:
                msg = f'gpio_conf() output failed with init="1" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

            ## test multiple output parameters
            result, output = self.dut.gpio_conf(device=dev, purpose='output', pin=pin, init='1', pull='up')
            if not result:
                msg = f'gpio_conf() output failed with init="1" and pull="up" pin {pin}: {output}'
                print(msg)
                failures.append(msg)

        if not failures:
            test_result = True

        self.failure_log += failures
        self.results.update({"GPIO Configure": test_result})


    def test_gpio_get(self, num_pins: int, dev: str):

        failures = []
        test_result = False
        output = None

        # test third and last pin low (pulled down)
        self.dut.gpio_conf(device=dev, pin=2, purpose='input', pull='down')
        try:
            output = self.dut.gpio_get(device=dev, pin=2)
            if output != '0':
                msg = f'Failed to get 0 from pin 2 (low)'
                print(msg)
                failures.append(msg)
        except Exception as e:
            print(f'exception occurred getting reading from pin 2 (low): {e}')
            if output is not None:
                print(f'{output=}')

        self.dut.gpio_conf(device=dev, pin=num_pins-1, purpose='input', pull='down')
        if self.dut.gpio_get(device=dev, pin=num_pins-1) != '0':
            msg = f'Failed to get 0 from pin {num_pins-1} (low)'
            print(msg)
            failures.append(msg)

        # test third and last pin high (pulled up)
        self.dut.gpio_conf(device=dev, pin=2, purpose='input', pull='up')
        if self.dut.gpio_get(device=dev, pin=2) != '1':
            msg = f'Failed to get 1 from pin 2 (high)'
            print(msg)
            failures.append(msg)

        self.dut.gpio_conf(device=dev, pin=num_pins-1, purpose='input', pull='up')
        if self.dut.gpio_get(device=dev, pin=num_pins-1) != '1':
            msg = f'Failed to get 1 from pin {num_pins-1} (high)'
            print(msg)
            failures.append(msg)

        if not failures:
            test_result = True

        self.failure_log += failures
        self.results.update({'GPIO Get': test_result})

    def test_gpio_set(self, dev: str, in_pin=4, out_pin=5):

        test_result = False
        failures = []

        # configure input and output pins that are wired together
        self.dut.gpio_conf(device=dev, pin=in_pin, purpose='input', pull='down')
        self.dut.gpio_conf(device=dev, pin=out_pin, purpose='output')

        # turn on output and test that input goes high
        output = self.dut.gpio_set(device=dev, pin=out_pin, level=1)
        if output:
            msg = f'Error occured while setting pin {out_pin} to 1: {output}'
            print(msg)
            failures.append(msg)
        if self.dut.gpio_get(device=dev, pin=in_pin) != '1':
            msg = f'Failed to get high reading on pin {in_pin} when pin {out_pin} set high'
            print(msg)
            failures.append(msg)

        # turn off output and test that input goes low
        output = self.dut.gpio_set(device=dev, pin=out_pin, level=0)
        if output:
            msg = f'Error occured while setting pin {out_pin} to 0: {output}'
            print(msg)
            failures.append(msg)
        if self.dut.gpio_get(device=dev, pin=in_pin) != '0':
            msg = f'Failed to get low reading on pin {in_pin} when pin {out_pin} set low'
            print(msg)
            failures.append(msg)

        # test invalid level
        try:
            self.dut.gpio_set(device=dev, pin=out_pin, level=2)
            msg = f'Failed to throw exception for invalid level'
            print(msg)
            failures.append(msg)
        except:
            pass

        if not failures:
            test_result = True

        self.failure_log += failures
        self.results.update({'GPIO Set': test_result})

    def test_gpio_toggle(self, dev: str, in_pin=4, out_pin=5):

        test_result = False
        failures = []

        # configure input and output pins that are wired together
        self.dut.gpio_conf(device=dev, pin=in_pin, purpose='input', pull='down')
        self.dut.gpio_conf(device=dev, pin=out_pin, purpose='output', init='0')

        # toggle pin high
        output = self.dut.gpio_toggle(device=dev, pin=out_pin)
        if output:
            msg = f'Error occurred while toggling pin {out_pin}'
            print(msg)
            failures.append(msg)
        if not self.dut.gpio_get(device=dev, pin=in_pin):
            msg = f'Failed to toggle pin {out_pin} high'
            print(msg)
            failures.append(msg)

        # toggle pin low
        output = self.dut.gpio_toggle(device=dev, pin=out_pin)
        if output:
            msg = f'Error occurred while toggling pin {out_pin}'
            print(msg)
            failures.append(msg)
        if self.dut.gpio_get(device=dev, pin=in_pin):
            msg = f'Failed to toggle pin {out_pin} low'
            print(msg)
            failures.append(msg)

        if not failures:
            test_result = True

        self.failure_log += failures
        self.results.update({'GPIO Toggle': test_result})

    def test_gpio_devices(self, expected_dev: str):
        failures = []
        matches = []
        test_result = False
        gpio_dev_list = []
        expected_dev = expected_dev.split(':')

        for dev in expected_dev:
            gpio_dev_list.append(dev.split(','))

        output = self.dut.gpio_devices()

        failures.append("GPIO devices test not yet implemented")

        if not failures:
            test_result = True

        self.failure_log += failures
        self.results.update({'GPIO Devices': test_result})

def main(num_pins: int,
         gpio_device: str,
         interface="uart",
         hwid=None,
         port=None,
         serial_no=None,
         gpio_dev_list=None):


    dut = ZShell(interface=interface,
                 port=port,
                 hwid=hwid,
                 serial_no=serial_no)

    test_harness = TestHarness(device_under_test=dut)

    print("Testing connect()...")
    test_harness.test_connect()
    print("Finished testing connect()")
    print("Testing write() and read()...")
    test_harness.test_write_read()
    print("Finished testing write() and read()")
    print("Testing send_command()...")
    test_harness.test_send_command()
    print("Finished testing send_command()")
    print("Testing gpio_conf()...")
    test_harness.test_gpio_conf(num_pins=int(num_pins), dev=gpio_device)
    print("Finished testing gpio_conf()")
    print("Testing gpio_get()...")
    test_harness.test_gpio_get(num_pins=int(num_pins), dev=gpio_device)
    print("Finished testing gpio_get()")
    print("Testing gpio_set()...")
    test_harness.test_gpio_set(dev=gpio_device)
    print("Finished testing gpio_set()")
    print("Testing gpio_toggle()")
    test_harness.test_gpio_toggle(dev=gpio_device)
    print("Finished testing gpio_toggle()")
    #print("Testing gpio_devices")
    #test_harness.test_gpio_devices(expected_dev=gpio_dev_list)
    #print("Finished testing gpio_devices()")

    for test in test_harness.results:
        print(f'{test}: {test_harness.results[test]}')

    if all(test_harness.results.values()):
        print("PASS")
    else:
        print("FAIL")
        print("Failure log:")
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
                        help='GPIO device tree name (ex. gpio@50000000)')
    parser.add_argument('-gl', '--gpio-dev-list',
                        default="gpio@50000000,gpio0:gpio@50000300,gpio1",
                        help='List of all GPIO devices and other names expected on tree, as a string, in a,b:c,d format')
    args = parser.parse_args()

    main(num_pins=args.gpio_pins,
         gpio_device=args.gpio_device,
         interface="uart",
         port=args.port,
         hwid=args.hwid,
         serial_no=args.serial_no,
         gpio_dev_list=args.gpio_dev_list)
