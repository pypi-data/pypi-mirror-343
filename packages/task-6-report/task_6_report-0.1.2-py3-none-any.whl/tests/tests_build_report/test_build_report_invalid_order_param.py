from datetime import datetime
from unittest.mock import patch

import pytest

from race_report.report import RaceData, Record


# Фікстура універсальна, коли потрібно перевіряти загальну поведінку з об'єктом RaceData, і немає необхідності в окремих записах.
@pytest.fixture
def race_data_with_records():
    race_data = RaceData("mock_folder")

    # Створюємо записи
    rec1 = Record("DRR", "Daniel Ricciardo", "RED BULL")
    rec1.start_time = datetime(2021, 5, 1, 12, 0, 0)
    rec1.end_time = datetime(2021, 5, 1, 12, 1, 30)

    rec2 = Record("SVF", "Sebastian Vettel", "FERRARI")
    rec2.start_time = datetime(2021, 5, 1, 12, 0, 0)
    rec2.end_time = datetime(2021, 5, 1, 12, 1, 0)

    race_data.records = [rec1, rec2]
    return race_data



def test_build_report_invalid_order_param(race_data_with_records):
    race_data = race_data_with_records

    with patch.object(RaceData, "read_times", return_value=([race_data.records[0], race_data.records[1]], [])):
        report = race_data.build_report(order="wrong_param")
        print("\n===== Сформований звіт =====\n")
        print(report)
        print("\n=============================\n")

    ricciardo_index = report.find("Daniel Ricciardo")
    vettel_index = report.find("Sebastian Vettel")

    assert ricciardo_index < vettel_index