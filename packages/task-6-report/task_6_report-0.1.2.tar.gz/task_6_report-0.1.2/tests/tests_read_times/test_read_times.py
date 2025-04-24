import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from race_report.report import RaceData


@pytest.fixture
def race_data():
    """
    Фікстура для підготовки тестового середовища.
    Створює об'єкт класу RaceData.
    """
    mock_folder = Path("mock_folder")
    return RaceData(mock_folder)


def test_read_times_valid(race_data):
    """
    Тест для перевірки валідних часів у файлі.
    """
    mock_data = "DRR2018-05-24_12:00:00.000\nSVF2018-05-24_12:01:00.000"
    with patch("pathlib.Path.open", mock_open(read_data=mock_data)):
        valid_times, invalid = race_data.read_times("start.log", is_start=True)
        assert len(valid_times) == 2  # Два валідні часи
        assert len(invalid) == 0  # Без помилок


def test_read_times_invalid_format(race_data):
    """
    Тест для перевірки обробки некоректного формату часу у файлі.
    """
    mock_data = "DRR2018-05-24_12:00:00.000\nINVALID_TIME_FORMAT"
    with patch("pathlib.Path.open", mock_open(read_data=mock_data)):
        valid_times, invalid = race_data.read_times("start.log", is_start=True)
        assert len(valid_times) == 1  # Один валідний час
        assert len(invalid) == 1  # Одна помилка
