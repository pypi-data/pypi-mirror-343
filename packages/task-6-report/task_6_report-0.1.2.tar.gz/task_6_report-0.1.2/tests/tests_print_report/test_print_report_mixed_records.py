import pytest
from race_report.report import RaceData, Record
from datetime import datetime


# Фікстура з мішаними записами
@pytest.fixture
def race_data_mixed_records():
    race_data = RaceData(folder="test_folder")

    # Валідні записи
    valid_record_1 = Record(
        abbr="DR1",
        team="TEAM0",
        _start_time=datetime(2025, 4, 19, 12, 0, 0),
        _end_time=datetime(2025, 4, 19, 12, 1, 0),
    )
    valid_record_2 = Record(
        abbr="DR2",
        team="TEAM1",
        _start_time=datetime(2025, 4, 19, 12, 2, 0),
        _end_time=datetime(2025, 4, 19, 12, 3, 0),
    )

    # Невалідні записи
    invalid_record_1 = Record(
        abbr="DR3",
        team="TEAM2",
        _start_time=datetime(2025, 4, 19, 12, 4, 0),
        _end_time=datetime(2025, 4, 19, 12, 5, 0),
    )
    invalid_record_2 = Record(
        abbr="DR4",
        team="TEAM3",
        _start_time=None,  # Пустий start_time
        _end_time=datetime(2025, 4, 19, 12, 6, 0),
    )

    # Додаємо записи до списку
    race_data.records = [
        valid_record_1,
        valid_record_2,
        invalid_record_1,
        invalid_record_2,
    ]
    return race_data


def test_print_report_mixed_records(race_data_mixed_records, capsys):
    # Викликаємо print_report
    race_data_mixed_records.print_report(order="asc")

    # Захоплюємо вивід
    captured = capsys.readouterr()
    output = captured.out.strip().splitlines()

    # Перевірка, чи є заголовок для валідних записів
    assert "=== Валідні записи ===" in output
    # Перевірка на наявність абревіатур в валідних записах
    assert "1. None | TEAM0 | 1:60,000" in output
    assert "2. None | TEAM1 | 1:60,000" in output

    # Перевірка, чи є заголовок для невалідних записів
    assert "=== Невалідні записи ===" in output
    # Перевірка на наявність невалідного запису з некоректним lap_time
    assert "1. None | TEAM3 | []" in output

    # Перевірка тексту на українській мові (для заголовків і повідомлень)
    assert "Знайдено 4 записів" in output