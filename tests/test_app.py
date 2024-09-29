import unittest
from io import StringIO
import sys
from unittest.mock import patch
from app import main

class TestIPSubnetCalculator(unittest.TestCase):

    def test_valid_input(self):
        user_input = ['192.168.1.0/24', '50,20,30']
        expected_output = (
            "\nРаспределенные подсети:\n"
            "192.168.1.0/26 - для 50 хостов\n"
            "192.168.1.64/27 - для 30 хостов\n"
            "192.168.1.96/27 - для 20 хостов\n"
        )
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertIn(expected_output.strip(), fake_out.getvalue().strip())

    def test_invalid_ip_range(self):
        user_input = ['999.999.999.999-192.168.1.255', '50']
        expected_output = "Ошибка при разборе диапазона IP-адресов"
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertIn(expected_output, fake_out.getvalue())

    def test_insufficient_ips(self):
        user_input = ['192.168.1.0/28', '50']
        expected_output = "Недостаточно IP-адресов в заданном диапазоне для удовлетворения всех запросов."
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertIn(expected_output, fake_out.getvalue())

    def test_negative_hosts(self):
        user_input = ['192.168.1.0/24', '-10']
        expected_output = "Некорректное количество хостов: -10"
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertIn(expected_output, fake_out.getvalue())

    def test_zero_hosts(self):
        user_input = ['192.168.1.0/24', '0']
        expected_output = "Некорректное количество хостов: 0"
        with patch('builtins.input', side_effect=user_input), \
             patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertIn(expected_output, fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()
