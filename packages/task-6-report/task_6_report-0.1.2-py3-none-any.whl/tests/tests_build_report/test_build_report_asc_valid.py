from unittest.mock import patch
from race_report.report import RaceData


def test_build_report_asc_valid(race_data_with_two_valid_records):
    race_data, _ = (
        race_data_with_two_valid_records  # розпаковка  # Отримуємо дані з фікстури
    )

    # Мокаємо read_times, щоб не лізла у файлову систему
    with patch.object(RaceData, "read_times", return_value=(None, [])):
        report = race_data.build_report(order="asc")

    # Перевіряємо порядок у звіті
    assert "=== Валідні записи ===" in report
    assert report.index("DRR") < report.index("LHM")
    assert "=== Невалідні записи ===" in report
