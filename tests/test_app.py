import unittest
from io import StringIO
from unittest.mock import patch
from app import main

class TestIPSubnetCalculator(unittest.TestCase):

    def test_valid_input(self):
        user_input = [
            '192.168.1.0/24',  # IP range
            '50,20,30',        # Number of hosts
        ]
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            main()
            output = fake_out.getvalue()
            # Проверка наличия основных сообщений
            self.assertIn("Allocated subnets:", output)
            self.assertIn("192.168.1.0/26 - for 50 hosts", output)
            self.assertIn("192.168.1.64/27 - for 30 hosts", output)
            self.assertIn("192.168.1.96/27 - for 20 hosts", output)

    def test_invalid_ip_range_format(self):
        user_input = [
            '192.168.1.0/24/32',  # Invalid IP range format
            '50,20,30',           # Number of hosts
        ]
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Error parsing IP range", output)

    def test_invalid_ip_range_values(self):
        user_input = [
            '999.999.999.999-192.168.1.255',  # Invalid IP range
            '50,20,30',                        # Number of hosts
        ]
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Error parsing IP range", output)

    def test_start_ip_greater_than_end_ip(self):
        user_input = [
            '192.168.1.255-192.168.1.0',  # Start IP > End IP
            '50,20,30',                     # Number of hosts
        ]
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Start IP is greater than End IP", output)

    def test_invalid_number_of_hosts_negative(self):
        user_input = [
            '192.168.1.0/24',  # IP range
            '-10,20,30',        # Negative number of hosts
        ]
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Invalid number of hosts: -10", output)

    def test_invalid_number_of_hosts_non_integer(self):
        user_input = [
            '192.168.1.0/24',  # IP range
            '50,abc,30',        # Non-integer number of hosts
        ]
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Invalid input for number of hosts: abc", output)

    def test_insufficient_ips(self):
        user_input = [
            '192.168.1.0/28',  # Small IP range
            '50',              # Number of hosts
        ]
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Not enough IP addresses in the given range to fulfill all requests.", output)
            self.assertIn("Required IP addresses: 64, available: 16", output)

if __name__ == '__main__':
    unittest.main()
