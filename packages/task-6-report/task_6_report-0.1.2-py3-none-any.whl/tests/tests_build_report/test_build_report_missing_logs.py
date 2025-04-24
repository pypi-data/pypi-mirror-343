from unittest.mock import patch
import pytest
from race_report.report import RaceData, Record

@pytest.fixture
def race_data_with_missing_logs():
    race_data = RaceData("mock_folder")

    rec1 = Record(
        abbr="DRR",
        name="",
        team="",
        errors=["Відсутній файл start.log"])
    rec2 = Record(
        abbr="SVF",
        name="",
        team="",
        errors=["Відсутній файл end.log"])

    return race_data, [rec1, rec2]


def test_build_report_missing_logs(race_data_with_missing_logs):
    race_data, invalid_records = race_data_with_missing_logs

    with patch.object(RaceData, "read_times", return_value=([], invalid_records)):
        race_data.records = invalid_records  # <--- ВАЖЛИВО: вручну оновлюємо записи
        report = race_data.build_report(order="asc")

    print("\n===== Звіт при відсутніх логах =====")
    print(report)
    print("=====================================\n")

    assert "=== Валідні записи ===" in report
    assert "=== Невалідні записи ===" in report

    for record in invalid_records:
        assert record.abbr in report
