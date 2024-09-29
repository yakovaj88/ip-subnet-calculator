import ipaddress
import math

def main():
    ip_range_str = input("Введите диапазон IP-адресов (например, 192.168.0.0-192.168.0.255 или 192.168.1.0/27): ")
    hosts_input = input("Введите количество необходимых хостов через запятую (например, 50,20,30): ")

    # Определяем начальный и конечный IP из заданного диапазона
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
            print("Неверный формат диапазона IP-адресов")
            return
    except ValueError as e:
        print(f"Ошибка при разборе диапазона IP-адресов: {e}")
        return

    start_ip_int = int(start_ip)
    end_ip_int = int(end_ip)

    # Проверяем корректность диапазона
    if start_ip_int > end_ip_int:
        print("Начальный IP больше конечного IP")
        return

    # Преобразуем введенные количества хостов в список целых чисел
    hosts_list = []
    for h in hosts_input.split(','):
        h = h.strip()
        try:
            h_int = int(h)
            if h_int <= 0:
                print(f"Некорректное количество хостов: {h_int}")
                return
            hosts_list.append(h_int)
        except ValueError:
            print(f"Некорректный ввод количества хостов: {h}")
            return

    # Сортируем список количества хостов в порядке убывания
    hosts_list.sort(reverse=True)

    # Проверяем, хватает ли IP-адресов в заданном диапазоне
    total_hosts_needed = sum([2 ** math.ceil(math.log2(h + 2)) for h in hosts_list])
    total_ips_available = end_ip_int - start_ip_int + 1

    if total_hosts_needed > total_ips_available:
        print(f"Недостаточно IP-адресов в заданном диапазоне для удовлетворения всех запросов.")
        print(f"Требуется IP-адресов: {total_hosts_needed}, доступно: {total_ips_available}")
        return

    current_ip_int = start_ip_int
    allocated_networks = []

    for n_hosts in hosts_list:
        # Вычисляем необходимую длину маски подсети
        required_hosts = n_hosts + 2  # +2 для адреса сети и широковещательного адреса
        subnet_mask_length = 32 - math.ceil(math.log2(required_hosts))

        if subnet_mask_length < 0 or subnet_mask_length > 32:
            print(f"Некорректное количество хостов: {n_hosts}")
            continue

        subnet_size = 2 ** (32 - subnet_mask_length)

        # Выравниваем текущий IP по границе подсети
        if current_ip_int % subnet_size != 0:
            current_ip_int = ((current_ip_int // subnet_size) + 1) * subnet_size

        # Проверяем, вписывается ли подсеть в диапазон
        if current_ip_int + subnet_size - 1 > end_ip_int:
            print(f"Недостаточно IP-адресов для сети с {n_hosts} хостами")
            continue

        network = ipaddress.IPv4Network((current_ip_int, subnet_mask_length), strict=False)
        allocated_networks.append((network, n_hosts))
        current_ip_int += subnet_size

    if allocated_networks:
        print("\nРаспределенные подсети:")
        for net, hosts in allocated_networks:
            print(f"{net} - для {hosts} хостов")
    else:
        print("Не удалось распределить подсети с заданными параметрами")

if __name__ == '__main__':
    main()
