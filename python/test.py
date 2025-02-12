
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

    def test_send_command(self):
        test_result = False
        failures = []
        cmd = "help"
        expected_output = "\r\nPlease press the <Tab> button to see all available commands.\r\nYou can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.\r\nYou can try to call commands with <-h> or <--help> parameter for more information.\r\n\r\nShell supports following meta-keys:\r\n  Ctrl + (a key from: abcdefklnpuw)\r\n  Alt  + (a key from: bf)\r\nPlease refer to shell documentation for more details.\r\n\r\nAvailable commands:\r\n  clear  : Clear screen.\r\n  device  : Device commands\r\n  devmem  : Read/write physical memory\r\nUsage:\r\nRead memory at address with optional width:\r\ndevmem <address> [<width>]\r\nWrite memory at address with mandatory width and value:\r\ndevmem <address> <width> <value>\r\n  gpio  : GPIO commands\r\n  help  : Prints the help message.\r\n  history  : Command history.\r\n  i2c  : I2C commands\r\n  kernel  : Kernel commands\r\n  pwm  : PWM shell commands\r\n  rem  : Ignore lines beginning with 'rem '\r\n  resize  : Console gets terminal screen size or assumes default in case the\r\nreadout fails. It must be executed after each terminal width change\r\nto ensure correct text display.\r\n  retval  : Print return value of most recent command\r\n  shell  : Useful, not Unix-like shell commands.\r\n  spi  : SPI commands\r\n ".strip()

        output = self.dut.send_command(cmd)

        test_result = (output == expected_output)

        self.failure_log += failures
        self.results.update({"Send Command": test_result})

    def test_gpio_conf(self, num_pins: int, dev: str):
        test_result = False
        failures = []

        result, output = self.dut.gpio_conf(device=dev, pin=0, init='1')

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
            print(f'Testing gpio_conf on pin {pin}')

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

        # test third and last pin low (pulled down)
        self.dut.gpio_conf(device=dev, pin=2, purpose='input', pull='down')
        if self.dut.gpio_get(device=dev, pin=2) != 0:
            msg = f'Failed to get 0 from pin 2 (low)'
            print(msg)
            failures.append(msg)

        self.dut.gpio_conf(device=dev, pin=num_pins-1, purpose='input', pull='down')
        if self.dut.gpio_get(device=dev, pin=num_pins-1) != 0:
            msg = f'Failed to get 0 from pin {num_pins-1} (low)'
            print(msg)
            failures.append(msg)

        # test third and last pin high (pulled up)
        self.dut.gpio_conf(device=dev, pin=2, purpose='input', pull='up')
        if self.dut.gpio_get(device=dev, pin=2) != 1:
            msg = f'Failed to get 1 from pin 2 (high)'
            print(msg)
            failures.append(msg)

        self.dut.gpio_conf(device=dev, pin=num_pins-1, purpose='input', pull='up')
        if self.dut.gpio_get(device=dev, pin=num_pins-1) != 1:
            msg = f'Failed to get 1 from pin {num_pins-1} (high)'
            print(msg)
            failures.append(msg)

        if not failures:
            test_result = True

        self.failure_log += failures
        self.results.update({'GPIO Get': test_result})


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
