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

def test_read_abbreviations_valid(race_data):
    """
    Тест для перевірки валідних абревіатур у файлі.
    """
    mock_data = (
        "DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\n"
        "SVF_Sebastian Vettel_FERRARI\n"
        "LHM_Lewis Hamilton_MERCEDES"
    )
    with patch("pathlib.Path.open", mock_open(read_data=mock_data)):
        result, invalid = race_data.read_abbreviations()
        assert len(result) == 3  # Три валідні записи
        assert len(invalid) == 0  # Без помилок
        assert "DRR" in result  # Перевірка, що абревіатура присутня
        assert "SVF" in result  # Перевірка, що абревіатура присутня

def test_read_abbreviations_invalid_format(race_data):
    """
    Тест для перевірки обробки некоректного формату рядків у файлі.
    """
    mock_data = (
        "DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\n"
        "INVALID_LINE\n"
        "SVF_Sebastian Vettel_FERRARI"
    )
    with patch("pathlib.Path.open", mock_open(read_data=mock_data)):
        result, invalid = race_data.read_abbreviations()
        assert len(result) == 2  # Два валідні записи
        assert len(invalid) == 1  # Один некоректний запис
        assert "INVALID_LINE" in invalid[0].errors[0]  # Перевірка на помилку

def test_read_abbreviations_file_not_found(race_data):
    """
    Тест для перевірки поведінки при відсутності файлу.
    """
    with patch("pathlib.Path.open", side_effect=FileNotFoundError):
        result, invalid = race_data.read_abbreviations()
        assert len(result) == 0  # Без валідних записів
        assert len(invalid) == 1  # Одна помилка
        assert "Файл mock_folder\\abbreviations.txt не знайдено." in invalid[0].errors[0]

def test_read_abbreviations_other_exception(race_data):
    """
    Тест для перевірки поведінки при іншій помилці під час зчитування.
    """
    with patch("pathlib.Path.open", side_effect=Exception("Щось пішло не так")):
        result, invalid = race_data.read_abbreviations()
        assert len(result) == 0  # Без валідних записів
        assert len(invalid) == 1  # Одна помилка
        assert "Сталася помилка при зчитуванні" in invalid[0].errors[0]

