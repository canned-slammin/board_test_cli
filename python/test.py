
from zshell import ZShell

def test_connect():
    print('not yet implemented')
    return False

def run_tests(interface="uart", hwid=None):
    failures = []

    if interface.lower() != 'uart' and interface.lower() != 'rtt':
        failures.append(f'interface "{interface}" not recognized')
        return failures

    dut = ZShell(interface=interface, hwid=hwid)

    if not test_connect():
        failures.append(f'connect function failed')
        return failures

def main(interface="uart", hwid=None):
    failures = run_tests(interface=interface, hwid=hwid)
    if not failures:
        print('Test Pass')
    else:
        print('Test Failed')
        for failure in failures:
            print(failure)


if __name__ == "__main__":

    main("uart")
