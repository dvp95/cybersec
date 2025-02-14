import sys
import socket
import threading
from datetime import datetime


def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))  # error indicator: 0 if port is open
        if result == 0:
            print(f'Port {port} is open')
        s.close()
    except socket.error as e:
        print(f'Soket error on port {port}: {e}')
    except Exception as e:
        print(f'Unexpected error on port {port}: {e}')


def main():
    if len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        print('Invalid number of arguments. Usage: python scanner.py <target>')
        sys.exit(1)

    # resolving target hostname to an IP address
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f'Error: Unable to resolve hostname {target}')
        sys.exit(1)

    # adding a banner
    print('-' * 50)
    print(f'Scanning target {target_ip}')
    print(f'Time started: {datetime.now()}')
    print('-' * 50)

    try:
        # multithreading to scan ports concurrently
        threads = []
        for port in range(1, 65536):
            thread = threading.Thread(target=scan_port, args=(target_ip, port))
            threads.append(thread)
            thread.start()

        # wait for all threads to complete
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print('\nExiting program.')
        sys.exit(0)

    except socket.error as e:
        print(f'Socket error: {e}')
        sys.exit(1)

    print('\nScan completed!')


if __name__ == "__main__":
    main()
