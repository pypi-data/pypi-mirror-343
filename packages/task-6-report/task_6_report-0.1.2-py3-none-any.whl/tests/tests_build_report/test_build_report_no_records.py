import pytest
from race_report.report import RaceData
from unittest.mock import patch

# Фікстура для створення порожнього списку записів


@pytest.fixture
def race_data_with_no_records():
    race_data = RaceData("mock_folder")
    race_data.records = []  # Порожній список записів
    return race_data


def test_build_report_no_records(race_data_with_no_records):
    race_data = race_data_with_no_records

    with patch.object(RaceData, "read_times", return_value=([], [])):
        report = race_data.build_report(order="asc")

    # Очікуємо дві секції без записів
    assert report.strip() == (
        "=== Валідні записи ===\n\n=== Невалідні записи ==="
    )
