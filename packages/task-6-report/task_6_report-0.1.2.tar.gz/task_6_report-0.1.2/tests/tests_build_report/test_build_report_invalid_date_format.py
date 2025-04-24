from unittest.mock import patch

import pytest

from race_report.report import RaceData, Record


@pytest.fixture
def race_data_with_invalid_date():
    race_data = RaceData("mock_folder")

    rec1 = Record(
        abbr="DRR", name="", team="", errors=["Неправильний формат дати у start.log"]
    )
    rec2 = Record(
        abbr="SVF", name="", team="", errors=["Неправильний формат дати у end.log"]
    )

    return race_data, [rec1, rec2]


def test_build_report_invalid_date_format(race_data_with_invalid_date):
    race_data, invalid_records = race_data_with_invalid_date

    with patch.object(RaceData, "read_times", return_value=([], invalid_records)):
        race_data.records = invalid_records  # Оновлюємо записи вручну

        report = race_data.build_report(order="asc")

    print("\n===== Звіт з некоректною датою у логах =====")
    print(report)
    print("=====================================\n")

    # Перевіряємо наявність розділів звіту
    assert "=== Валідні записи ===" in report
    assert "=== Невалідні записи ===" in report

    # Перевіряємо, що помилки правильного формату потрапляють в звіт
    for record in invalid_records:
        assert f"Помилка для {record.abbr}: {record.errors[0]}" in report