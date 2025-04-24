from datetime import datetime
import pytest
from race_report.report import RaceData, Record

# Фікстури для створення тестових даних

@pytest.fixture
def race_data_with_two_valid_records():
    race_data = RaceData("mock_folder")

    # Створюємо два валідні записи
    record1 = Record("DRR", "Daniel Ricciardo", "RED BULL")
    record1.start_time = datetime(2021, 5, 1, 12, 0, 0, 0)
    record1.end_time = datetime(2021, 5, 1, 12, 1, 15, 123000)

    record2 = Record("LHM", "Lewis Hamilton", "MERCEDES")
    record2.start_time = datetime(2021, 5, 1, 12, 0, 5, 0)
    record2.end_time = datetime(2021, 5, 1, 12, 1, 20, 456000)

    race_data.records = [record2, record1]  # У невпорядкованому вигляді
    return race_data, [record1, record2]  # Повертаємо кортеж


