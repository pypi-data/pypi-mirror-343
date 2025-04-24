import pytest

from race_report.report import RaceData, Record
from unittest.mock import patch

@pytest.fixture
def race_data_with_malformed_log_line():
    race_data = RaceData("mock_folder")

    rec1 = Record(
        abbr="DRR", name="", team="", errors=["Неправильний формат рядка у start.log"]
    )
    rec2 = Record(
        abbr="SVF", name="", team="", errors=["Неправильний формат рядка у end.log"]
    )

    return race_data, [rec1, rec2]

def test_build_report_malformed_log_line(race_data_with_malformed_log_line):
    race_data, invalid_records = race_data_with_malformed_log_line

    with patch.object(RaceData, "read_times", return_value=([], invalid_records)):
        race_data.records = invalid_records
        report = race_data.build_report(order="asc")

    print("\n===== Звіт з некоректним рядком у логах =====")
    print(report)
    print("=============================================\n")

    assert "=== Валідні записи ===" in report
    assert "=== Невалідні записи ===" in report
    for record in invalid_records:
        assert record.abbr in report
        for err in record.errors:
            assert err in report
