# app.py
import sys
import ipaddress
import math

# Кроссплатформенная обработка нажатий клавиш
def wait_for_key():
    if sys.platform == 'win32':
        import msvcrt
        print("\nPress Enter to continue or Esc to exit.")
        while True:
            key = msvcrt.getch()
            if key == b'\r':  # Enter key
                return 'enter'
            elif key == b'\x1b':  # Esc key
                return 'esc'
    else:
        import termios
        import tty

        print("\nPress Enter to continue or Esc to exit.")
        fd = sys.stdin.fileno()
        try:
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if key in ['\r', '\n']:
                return 'enter'
            elif key == '\x1b':
                return 'esc'
            else:
                return 'other'
        except termios.error:
            # В случае ошибки, например, отсутствия терминала, завершаем программу
            return 'esc'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def calculate_subnets(ip_range_str, hosts_input):
    try:
        # Определяем начальный и конечный IP
        if '/' in ip_range_str:
            if ip_range_str.count('/') > 1:
                raise ValueError("Invalid IP range format.")
            network = ipaddress.IPv4Network(ip_range_str.strip(), strict=False)
            start_ip = network.network_address
            end_ip = network.broadcast_address
        elif '-' in ip_range_str:
            parts = ip_range_str.split('-')
            if len(parts) != 2:
                raise ValueError("Invalid IP range format.")
            start_ip_str, end_ip_str = parts
            start_ip = ipaddress.IPv4Address(start_ip_str.strip())
            end_ip = ipaddress.IPv4Address(end_ip_str.strip())
        else:
            raise ValueError("Invalid IP range format.")

        start_ip_int = int(start_ip)
        end_ip_int = int(end_ip)

        if start_ip_int > end_ip_int:
            raise ValueError("Start IP is greater than End IP.")

        # Преобразуем количество хостов в список целых чисел
        hosts_list = []
        for h in hosts_input.split(','):
            h = h.strip()
            try:
                h_int = int(h)
            except ValueError:
                raise ValueError(f"invalid literal for int() with base 10: '{h}'")
            if h_int <= 0:
                raise ValueError(f"Invalid number of hosts: {h_int}")
            hosts_list.append(h_int)

        # Сортируем по убыванию для эффективного разбиения
        hosts_list.sort(reverse=True)

        # Вычисляем общее количество необходимых IP
        total_hosts_needed = sum([2 ** math.ceil(math.log2(h + 2)) for h in hosts_list])
        total_ips_available = end_ip_int - start_ip_int + 1

        if total_hosts_needed > total_ips_available:
            raise ValueError(f"Not enough IP addresses in the given range to fulfill all requests. Required IP addresses: {total_hosts_needed}, available: {total_ips_available}")

        current_ip_int = start_ip_int
        allocated_networks = []

        for n_hosts in hosts_list:
            required_hosts = n_hosts + 2  # +2 для сетевого и широковещательного адресов
            subnet_mask_length = 32 - math.ceil(math.log2(required_hosts))
            subnet_size = 2 ** (32 - subnet_mask_length)

            # Выравниваем текущий IP на границу подсети
            if current_ip_int % subnet_size != 0:
                current_ip_int = ((current_ip_int // subnet_size) + 1) * subnet_size

            if current_ip_int + subnet_size - 1 > end_ip_int:
                raise ValueError(f"Not enough IP addresses for a network with {n_hosts} hosts.")

            network = ipaddress.IPv4Network((current_ip_int, subnet_mask_length), strict=False)
            allocated_networks.append((network, n_hosts))
            current_ip_int += subnet_size

        return [f"{net} - for {hosts} hosts" for net, hosts in allocated_networks]

    except ValueError as e:
        return f"Error: {e}"

def main():
    while True:
        try:
            ip_range_str = input("Enter IP range (e.g., 192.168.0.0-192.168.0.255 or 192.168.1.0/27): ")
            hosts_input = input("Enter required number of hosts separated by commas (e.g., 50,20,30): ")

            subnets = calculate_subnets(ip_range_str, hosts_input)
            if isinstance(subnets, list):
                print("\nAllocated subnets:")
                for subnet in subnets:
                    print(subnet)
            else:
                print(subnets)  # Сообщение об ошибке

            # Запрос пользователю продолжить или выйти
            action = wait_for_key()
            if action == 'enter':
                continue
            elif action == 'esc':
                print("Exiting the program.")
                break
            else:
                continue
        except EOFError:
            print("\nExiting the program due to unexpected EOF.")
            break

if __name__ == "__main__":
    main()
