import re
import serial
from serial.tools import list_ports
from time import sleep


class UARTInterface:
    def __init__(self,
                 port=None,
                 hwid=None,
                 serial_no=None,
                 baudrate=115200,
                 read_timeout=3,
                 write_timeout=3):

        self.port = port
        self.hwid = hwid
        self.baudrate = baudrate
        self.serial_no = serial_no

        if self.port is None:
            self.port = self.find_port()

        self.ser = serial.Serial(port=self.port)
        self.ser.baudrate = self.baudrate
        self.ser.timeout = read_timeout
        self.ser.write_timeout = write_timeout

    def connect(self):
        """
        Resets and opens port. Flushes input and output buffers.

        Returns True if successful, False otherwise.
        """

        self.ser.close()
        self.ser.open()

        if not self.ser.is_open:
            return False

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        return True

    def read(self):
        """
        reads bytes off the serial port while there are bytes waiting
        converts to string and returns entire string once there are no bytes
        """
        output = ""
        # TODO this is not working - re module passing unterminated character exception
        suffix = b'\x1b[m'
        strip_char =  r'\x1b\[m' #  note the backslash before [m

        while self.ser.in_waiting:
            bytes_read = self.ser.read_until(expected=suffix)
            output += re.sub(pattern=strip_char,
                             repl='',
                             string=bytes_read.decode())
        return output

    def write(self, payload:str):
        bytes_read = self.ser.write(f'{payload}\n'.encode())
        sleep(0.5)  # account for lag between read and write
        return bytes_read

    def send_command(self, cmd: str):
        """
        writes given command
        returns output via read()
        strips escape/control characters, command echo, and terminal name
        """

        extra_char_pattern = re.compile(pattern=r'\x1b\[(1;32m|13C|1;31m)')
        terminal_pattern = re.compile(r'((uart)|(rtt)):~\$')
        cmd_pattern = re.compile(pattern=f'^{cmd}')
        output = ''

        self.write(cmd)
        raw_output = self.read()

        # strip echo and escape characters from output
        output = extra_char_pattern.sub(repl='', string=raw_output)
        output = cmd_pattern.sub(repl='', string=output)
        output = terminal_pattern.sub(repl='', string=output)

        return output.strip()


    def find_port(self):
        """
        iterates through ports and finds hwid and serial number
        if both hwid and serial_no are given, prioritizes serial_no

        returns port as string if found, None if not
        """
        pattern = re.compile(r'VID:PID=(\d{4}:\d{4}) SER=([a-zA-Z\d]*)')

        for port in list_ports.comports():
            hwid_match = pattern.search(port.hwid)
            if self.serial_no is not None:
                if hwid_match.group(2) == self.serial_no:
                    return port.device
            if self.hwid is not None:
                if hwid_match.group(1) == self.hwid:
                    return port.device

            return None


class RTTInterface:
    def __init__(self):
        print('RTT interface not yet implemented')

    def connect(self):
        print('not yet implemented')

    def read(self):
        print('not yet implemented')

    def write(self, payload):
        print('not yet implemented')

    def send_command(self, cmd: str, expected_output=None, match_all=False):
        print('not yet implemented')


class ZShell:
    def __init__(self, interface='uart',
                 port=None,
                 hwid=None,
                 serial_no=None):
        if interface.lower() == 'uart':
            self.interface = UARTInterface(port=port,
                                           hwid=hwid,
                                           serial_no=serial_no)
        if interface.lower() == 'rtt':
            self.interface = RTTInterface()

    def connect(self):
        return self.interface.connect()

    def read(self) -> str:
        return self.interface.read()

    def write(self, payload:str):
        return self.interface.write(payload)

    def send_command(self, cmd: str):
        return self.interface.send_command(cmd=cmd)

    def gpio_conf(self,
                  device: str,
                  pin: int,
                  purpose='input',
                  pull='',
                  active='',
                  init='',
                  config_flags=''):

        result = False
        output = ''

        if purpose.lower() == 'input':
            io = 'i'
        elif purpose.lower() == 'output':
            io = 'o'
        else:
            raise Exception('GPIO Configure - Purpose must be input or output')

        if not pull:
            ud = ''
        elif pull.lower() == 'up':
            ud = 'u'
        elif pull.lower() == 'down':
            ud = 'd'
        else:
            raise Exception('GPIO Configure - pull must be up, down, or unspecified (defaults to open)')

        if not active:
            hl = ''
        elif active.lower() == 'high':
            hl = 'h'
        elif active.lower() == 'low':
            hl = 'l'
        else:
            raise Exception('GPIO Configure - active must be high, low, or unspecified (defaults to high)')

        if not init:
            init_10 = ''
        elif str(init.lower()) == '0':
            init_10 = '0'
        elif str(init.lower()) == '1':
            init_10 = '1'
        else:
            raise Exception('GPIO Configure - init must be 0, 1, or unspecified (defaults to 0)')


        cmd = f'gpio conf {device} {str(pin)} {io}{ud}{hl}{init_10} {config_flags}'

        output = self.send_command(cmd=cmd)

        if not output:  # successful command has no return
            result = True

        return result, output

    def gpio_get(self, device, pin):
        """
        get value of given pin on given device
        returns 0 for low, 1 for high
        """
        print('not yet implemented')

        #cmd = f'gpio get {device} {str(pin)}'



    def gpio_set(self, device, pin, level='0'):
        print('not yet implemented')

    def gpio_toggle(self, device, pin):
        print('not yet implemented')

    def gpio_devices(self):
        print('not yet implemented')

    def gpio_blink(self, device, pin):
        print('not yet implemented')

    def gpio_info(self, device):
        print('not yet implemented')

# TODO GPIO

  #conf     : Configure GPIO pin
  #          Usage: gpio conf <device> <pin> <configuration <i|o>[u|d][h|l][0|1]>
  #          [vendor specific]
  #          <i|o> - input|output
  #          [u|d] - pull up|pull down, otherwise open
  #          [h|l] - active high|active low, otherwise defaults to active high
  #          [0|1] - initialise to logic 0|logic 1, otherwise defaults to logic 0
  #          [vendor specific] - configuration flags within the mask 0xFF00
  #          see include/zephyr/dt-bindings/gpio/
  #get      : Get GPIO pin value
  #          Usage: gpio get <device> <pin>
  #set      : Set GPIO pin value
  #          Usage: gpio set <device> <pin> <level 0|1>
  #toggle   : Toggle GPIO pin
  #          Usage: gpio toggle <device> <pin>
  #devices  : List all GPIO devices
  #          Usage: gpio devices
  #blink    : Blink GPIO pin
  #          Usage: gpio blink <device> <pin>
  #info     : GPIO Information
  #          Usage: gpio info [device]



