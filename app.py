import sys
import ipaddress
import math

# Условный импорт для кроссплатформенной работы
if sys.platform == 'win32':
    import msvcrt
else:
    import tty
    import termios

def wait_for_key():
    print("\nPress Enter to continue or Esc to exit.")
    if sys.platform == 'win32':
        while True:
            key = msvcrt.getch()
            if key == b'\r':  # Enter key
                return 'enter'
            elif key == b'\x1b':  # Esc key
                return 'esc'
    else:
        # Unix-like systems
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            if key == '\x1b':  # Esc key
                return 'esc'
            elif key == '\r' or key == '\n':  # Enter key
                return 'enter'
            else:
                return 'other'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    while True:
        ip_range_str = input("Enter IP range (e.g., 192.168.0.0-192.168.0.255 or 192.168.1.0/27): ")
        hosts_input = input("Enter required number of hosts separated by commas (e.g., 50,20,30): ")

        # Determine start and end IP from the given range
        try:
            if '-' in ip_range_str:
                start_ip_str, end_ip_str = ip_range_str.split('-')
                start_ip = ipaddress.IPv4Address(start_ip_str.strip())
                end_ip = ipaddress.IPv4Address(end_ip_str.strip())
            elif '/' in ip_range_str:
                network = ipaddress.IPv4Network(ip_range_str.strip(), strict=False)
                start_ip = network.network_address
                end_ip = network.broadcast_address
            else:
                print("Invalid IP range format.")
                action = wait_for_key()
                if action == 'enter':
                    continue
                elif action == 'esc':
                    print("Exiting the program.")
                    break
                else:
                    continue
        except ValueError as e:
            print(f"Error parsing IP range: {e}")
            action = wait_for_key()
            if action == 'enter':
                continue
            elif action == 'esc':
                print("Exiting the program.")
                break
            else:
                continue

        start_ip_int = int(start_ip)
        end_ip_int = int(end_ip)

        # Check the validity of the range
        if start_ip_int > end_ip_int:
            print("Start IP is greater than End IP.")
            action = wait_for_key()
            if action == 'enter':
                continue
            elif action == 'esc':
                print("Exiting the program.")
                break
            else:
                continue

        # Convert entered host counts to a list of integers
        hosts_list = []
        for h in hosts_input.split(','):
            h = h.strip()
            try:
                h_int = int(h)
                if h_int <= 0:
                    print(f"Invalid number of hosts: {h_int}")
                    action = wait_for_key()
                    if action == 'enter':
                        continue
                    elif action == 'esc':
                        print("Exiting the program.")
                        break
                    else:
                        continue
                hosts_list.append(h_int)
            except ValueError:
                print(f"Invalid input for number of hosts: {h}")
                action = wait_for_key()
                if action == 'enter':
                    continue
                elif action == 'esc':
                    print("Exiting the program.")
                    break
                else:
                    continue

        # Sort the list of host counts in descending order
        hosts_list.sort(reverse=True)

        # Check if there are enough IP addresses in the given range
        total_hosts_needed = sum([2 ** math.ceil(math.log2(h + 2)) for h in hosts_list])
        total_ips_available = end_ip_int - start_ip_int + 1

        if total_hosts_needed > total_ips_available:
            print("Not enough IP addresses in the given range to fulfill all requests.")
            print(f"Required IP addresses: {total_hosts_needed}, available: {total_ips_available}")
            action = wait_for_key()
            if action == 'enter':
                continue
            elif action == 'esc':
                print("Exiting the program.")
                break
            else:
                continue

        current_ip_int = start_ip_int
        allocated_networks = []

        for n_hosts in hosts_list:
            # Calculate the required subnet mask length
            required_hosts = n_hosts + 2  # +2 for network and broadcast addresses
            subnet_mask_length = 32 - math.ceil(math.log2(required_hosts))

            if subnet_mask_length < 0 or subnet_mask_length > 32:
                print(f"Invalid number of hosts: {n_hosts}")
                continue

            subnet_size = 2 ** (32 - subnet_mask_length)

            # Align the current IP to the subnet boundary
            if current_ip_int % subnet_size != 0:
                current_ip_int = ((current_ip_int // subnet_size) + 1) * subnet_size

            # Check if the subnet fits in the range
            if current_ip_int + subnet_size - 1 > end_ip_int:
                print(f"Not enough IP addresses for a network with {n_hosts} hosts.")
                continue

            network = ipaddress.IPv4Network((current_ip_int, subnet_mask_length), strict=False)
            allocated_networks.append((network, n_hosts))
            current_ip_int += subnet_size

        if allocated_networks:
            print("\nAllocated subnets:")
            for net, hosts in allocated_networks:
                print(f"{net} - for {hosts} hosts")
        else:
            print("Failed to allocate subnets with the given parameters.")

        # Prompt user to continue or exit
        action = wait_for_key()
        if action == 'enter':
            continue
        elif action == 'esc':
            print("Exiting the program.")
            break
        else:
            continue

if __name__ == '__main__':
    main()
