from unittest.mock import patch
from race_report.report import RaceData


def test_build_report_desc_valid(race_data_with_two_valid_records):
    race_data, records = race_data_with_two_valid_records

    # Мокаємо read_times, щоб не лізла у файлову систему
    with patch.object(RaceData, "read_times", return_value=(None, [])):
        report = race_data.build_report(order="desc")

    # Перевіряємо порядок у звіті
    assert "=== Валідні записи ===" in report
    assert report.index("LHM") < report.index(
        "DRR")  # Перевірка спадного порядку
    assert "=== Невалідні записи ===" in report
