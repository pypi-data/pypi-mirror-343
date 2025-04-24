from unittest.mock import patch
import pytest
from race_report.report import RaceData, Record


@pytest.fixture
def race_data_missing_start_or_end():
    race_data = RaceData("mock_folder")

    rec1 = Record(abbr="DRR", name="Daniel Ricciardo", team="Red Bull", errors=["Час початку не знайдено"])
    rec2 = Record(abbr="SVF", name="Sebastian Vettel", team="Ferrari", errors=["Час фінішу не знайдено"])

    race_data.records = [rec1, rec2]
    return race_data

def test_build_report_missing_start_or_end(race_data_missing_start_or_end):
    race_data = race_data_missing_start_or_end

    # Підставляємо порожні списки валідних start/end, а Record-и вже містять помилки
    with patch.object(RaceData, "read_times", return_value=([], race_data.records)):
        report = race_data.build_report(order="asc")

    print("\n--- Звіт ---\n")
    print(report)

    assert "=== Валідні записи ===" in report
    assert "=== Невалідні записи ===" in report

    assert "Помилка для DRR: Час початку не знайдено" in report
    assert "Помилка для SVF: Час фінішу не знайдено" in report