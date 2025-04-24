import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Імпортуємо функції, які тестуємо
from race_report.report import get_report_input, main


class TestRaceReport(unittest.TestCase):
    # Тест для get_report_input()
    def test_get_report_input_order_asc(self):
        with patch("sys.argv", ["report.py", "--order", "asc"]):
            args = get_report_input()
            self.assertEqual(args["order"], "asc")
            self.assertIsNone(args["driver"])

    def test_get_report_input_order_desc(self):
        with patch("sys.argv", ["report.py", "--order", "desc"]):
            args = get_report_input()
            self.assertEqual(args["order"], "desc")
            self.assertIsNone(args["driver"])

    def test_get_report_input_with_driver(self):
        with patch("sys.argv", ["report.py", "--driver", "Lewis Hamilton"]):
            args = get_report_input()
            self.assertEqual(args["driver"], "Lewis Hamilton")
            self.assertEqual(args["order"], "asc")

    @patch("sys.stdout", new_callable=StringIO)
    @patch("race_report.report.RaceData")  # Мокуємо клас RaceData
    def test_main_without_driver(self, mock_race_data, mock_stdout):
        # Фейковий print_report, який друкує в stdout
        mock_race_data.return_value.print_report.side_effect = lambda order: print(
            "Знайдено 2 пілотів.")

        mock_race_data.return_value.records = [
            MagicMock(
                lap_time=MagicMock(total_seconds=10),
                team="Team A",
                name="Pilot 1",
                errors="",
            ),
            MagicMock(
                lap_time=MagicMock(total_seconds=12),
                team="Team B",
                name="Pilot 2",
                errors="",
            ),
        ]

        with patch("sys.argv", ["report.py", "--order", "asc"]):
            main()

        output = mock_stdout.getvalue()
        print(f"Output: {output}")  # Можна залишити для дебагу
        self.assertIn("Знайдено", output)

    def test_get_report_input_defaults(self):
        with patch("sys.argv", ["report.py"]):
            args = get_report_input()
            self.assertEqual(args["order"], "asc")
            self.assertIsNone(args["driver"])

    def test_get_report_input_missing_params(self):
        with patch("sys.argv", ["report.py"]):
            args = get_report_input()
            self.assertEqual(args["order"], "asc")
            self.assertIsNone(args["driver"])


if __name__ == "__main__":
    unittest.main()
