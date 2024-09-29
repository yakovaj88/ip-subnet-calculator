# tests/test_app.py
import unittest
from app import calculate_subnets

class TestIPSubnetCalculator(unittest.TestCase):

    def test_valid_input_exit(self):
        ip_range = '192.168.1.0/24'
        hosts = '50,20,30'
        expected = [
            "192.168.1.0/26 - for 50 hosts",
            "192.168.1.64/27 - for 30 hosts",
            "192.168.1.96/27 - for 20 hosts"
        ]
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected)

    def test_valid_input_continue_then_exit(self):
        # Поскольку мы тестируем только функцию, этот тест аналогичен предыдущему
        ip_range = '192.168.1.0/24'
        hosts = '50,20,30'
        expected = [
            "192.168.1.0/26 - for 50 hosts",
            "192.168.1.64/27 - for 30 hosts",
            "192.168.1.96/27 - for 20 hosts"
        ]
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected)

    def test_invalid_ip_range_format(self):
        ip_range = '192.168.1.0/24/32'  # Неправильный формат
        hosts = '50,20,30'
        expected_error = "Error: Invalid IP range format."
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected_error)

    def test_invalid_ip_range_values(self):
        ip_range = '999.999.999.999-192.168.1.255'  # Неправильные значения IP
        hosts = '50,20,30'
        expected_error = "Error: Octet 999 (> 255) not permitted in '999.999.999.999'"
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected_error)

    def test_start_ip_greater_than_end_ip(self):
        ip_range = '192.168.1.255-192.168.1.0'  # Начальный IP больше конечного
        hosts = '50,20,30'
        expected_error = "Error: Start IP is greater than End IP."
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected_error)

    def test_invalid_number_of_hosts_negative(self):
        ip_range = '192.168.1.0/24'
        hosts = '-10,20,30'  # Отрицательное количество хостов
        expected_error = "Error: Invalid number of hosts: -10"
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected_error)

    def test_invalid_number_of_hosts_non_integer(self):
        ip_range = '192.168.1.0/24'
        hosts = '50,abc,30'  # Некорректное количество хостов
        expected_error = "Error: invalid literal for int() with base 10: 'abc'"
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected_error)

    def test_insufficient_ips(self):
        ip_range = '192.168.1.0/28'  # Малый диапазон IP
        hosts = '50'  # Требуется 64 IP
        expected_error = "Error: Not enough IP addresses in the given range to fulfill all requests. Required IP addresses: 64, available: 16"
        result = calculate_subnets(ip_range, hosts)
        self.assertEqual(result, expected_error)

if __name__ == '__main__':
    unittest.main()
