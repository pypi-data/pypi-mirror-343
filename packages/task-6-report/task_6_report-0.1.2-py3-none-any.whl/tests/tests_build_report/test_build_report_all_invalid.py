import pytest
from race_report.report import RaceData, Record
from unittest.mock import patch

# Фікстура для створення об'єкта RaceData з невалідними записами


@pytest.fixture
def race_data_with_all_invalid_records():
    race_data = RaceData("mock_folder")

    # Імітуємо два невалідні записи
    invalid_record1 = Record("SVF", "Sebastian Vettel", "FERRARI")
    invalid_record1.errors.append("Некоректний формат start.log")

    invalid_record2 = Record("LHM", "Lewis Hamilton", "MERCEDES")
    invalid_record2.errors.append("Некоректний формат end.log")

    race_data.records = []  # немає валідних записів
    return race_data, invalid_record1, invalid_record2


def test_build_report_all_invalid(race_data_with_all_invalid_records):
    race_data, invalid_record1, invalid_record2 = race_data_with_all_invalid_records

    # Патчимо read_times, щоб поверталися лише невалідні
    with patch.object(RaceData, 'read_times', side_effect=[
        (None, [invalid_record1]),  # для start.log
        (None, [invalid_record2])   # для end.log
    ]):
        report = race_data.build_report(order="asc")

    # Перевірки
    assert "=== Валідні записи ===" in report
    assert "=== Невалідні записи ===" in report
    assert "SVF" in report
    assert "LHM" in report
    assert "Некоректний формат start.log" in report
    assert "Некоректний формат end.log" in report
