from unittest.mock import patch
import pytest
from race_report.report import RaceData, Record


@pytest.fixture
def race_data_with_duplicate_abbr():
    race_data = RaceData("mock_folder")

    rec = Record(abbr="DRR", name="Daniel Ricciardo", team="Red Bull", errors=["Дублікати абревіатури DRR у логах"])

    race_data.records = [rec]
    return race_data

def test_build_report_duplicate_abbr(race_data_with_duplicate_abbr):
    race_data = race_data_with_duplicate_abbr

    with patch.object(RaceData, "read_times", return_value=([], race_data.records)):
        report = race_data.build_report(order="asc")

    print("\n--- Звіт ---\n")
    print(report)

    assert "=== Валідні записи ===" in report
    assert "=== Невалідні записи ===" in report
    assert "Помилка для DRR: Дублікати абревіатури DRR у логах" in report