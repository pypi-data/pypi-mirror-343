from datetime import datetime

import pytest

from race_report.report import RaceData, Record
from unittest.mock import patch

# Фікстура для створення об'єкта RaceData з валідними і невалідними записами
@pytest.fixture
def race_data_with_mixed_records():
    race_data = RaceData("mock_folder")

    # Створюємо валідний запис
    valid_record = Record(
        abbr="SVF",
        name="Sebastian Vettel",
        team="FERRARI"
    )
    valid_record.start_time = datetime(2025, 4, 17, 12, 0, 0)  # Старт 17 квітня, 12:00
    valid_record.end_time = datetime(2025, 4, 17, 12, 1, 0)    # Фініш через 1 хвилину

    # Створюємо невалідний запис
    invalid_record = Record(
        abbr="LHM",
        name="Lewis Hamilton",
        team="MERCEDES"
    )
    invalid_record.start_time = datetime(2025, 4, 17, 12, 0, 0)  # Старт 17 квітня, 12:00
    invalid_record.end_time = datetime(2025, 4, 17, 11, 59, 0)    # Фініш до старту
    invalid_record.errors.append("Invalid lap time format")

    race_data.records = [valid_record, invalid_record]  # Змішаний список
    return race_data, valid_record, invalid_record

# Тест для перевірки змішаного списку валідних і невалідних записів
def test_build_report_mixed_valid_invalid(race_data_with_mixed_records):
    race_data, valid_record, invalid_record = race_data_with_mixed_records

    # Мокаємо read_times для повернення валідних та невалідних записів
    with patch.object(RaceData, 'read_times', return_value=(None, [valid_record, invalid_record])):
        report = race_data.build_report(order="asc")

    # Перевірки
    assert "=== Валідні записи ===" in report
    assert "=== Невалідні записи ===" in report
    assert valid_record.abbr in report  # Перевірка валідного запису
    assert invalid_record.abbr in report  # Перевірка невалідного запису
    assert "Invalid lap time format" in report  # Перевірка помилки для невалідного запису