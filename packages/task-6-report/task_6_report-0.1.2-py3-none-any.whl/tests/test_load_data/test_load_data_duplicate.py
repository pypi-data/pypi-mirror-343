from pathlib import Path
from unittest.mock import patch, mock_open
from race_report.report import RaceData

def test_load_data_duplicate():
    #Текст файлів, які будемо мокати  (повторяється абривіатура SVF)
    abbreviations = "SVF_Sebastian Vettel_FERRARI\nSVF_Sebastian Vettel_FERRARI\n"

    start_log = "SVF2018-05-24_12:02:58.917\nSVF2018-05-24_12:02:58.917\n"

    end_log = "SVF2018-05-24_12:04:03.332\nSVF2018-05-24_12:04:03.332\n"

    #Вміст файлів для мокування
    file_contents = {
        "abbreviations.txt": abbreviations,
        "start.log": start_log,
        "end.log": end_log,
    }

    #Мокування відкриття файлів для читання
    def open_side_effect(file, *args, **kwargs):
        filename = Path(file).name
        if filename in file_contents:
            m = mock_open(read_data=file_contents[filename]).return_value
            m.__enter__.return_value = m
            return m
        raise FileNotFoundError(f"Файл {filename} не знайдено.")

    #Мокування функцій для перевірки існування файлів
    with patch("builtins.open", side_effect=open_side_effect):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.is_file", return_value=True),
        ):
            # Створюємо об'єкт RaceData
            race = RaceData(Path("fake_path"))

            #Завантажуємо дані
            race.load_data()

            # Фільтруємо записи на валідні та невалідні
            valid_records = [r for r in race.records if not r.errors]
            invalid_records = [r for r in race.records if r.errors]

            assert len(valid_records) == 0
            assert len(invalid_records) == 2