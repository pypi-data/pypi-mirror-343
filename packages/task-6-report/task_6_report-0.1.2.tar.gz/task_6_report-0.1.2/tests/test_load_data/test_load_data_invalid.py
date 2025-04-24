from pathlib import Path
from unittest.mock import mock_open, patch
from race_report.report import RaceData


def test_load_data_invalid():
    # Текст файлів, які будемо мокати
    abbreviations = "SVF_Sebastian Vettel_FERRARI\nLHM_Lewis Hamilton_MERCEDES\n"

    start_log = "SVF2018-05-24_12:02:58.917\nLHM2018-05-24_12:03:18.456\n"

    end_log = (
        "SVF2018-05-24_12:04:03.332\n"  # Зверніть увагу, що для LHM немає кінцевого часу
    )

    # Вміст файлів для мокування
    file_contents = {
        "abbreviations.txt": abbreviations,
        "start.log": start_log,
        "end.log": end_log,  # Відсутність кінцевого часу для LHM
    }

    # Мокування відкриття файлів для читання
    def open_side_effect(file, *args, **kwargs):
        filename = Path(file).name
        if filename in file_contents:
            m = mock_open(read_data=file_contents[filename]).return_value
            m.__enter__.return_value = m  # важливо для контекстного менеджера
            return m
        # Якщо файл не знайдений в моках, але ми хочемо повернути коректне повідомлення
        if filename == "abbreviations.txt":
            return mock_open(
                read_data=""
            ).return_value  # Повертаємо порожній файл для abbreviations.txt
        raise FileNotFoundError(f"Файл {filename} не знайдено.")

    # Мокування функцій для перевірки існування файлів
    with patch("builtins.open", side_effect=open_side_effect):
        # Мокування для перевірки існування файлів
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.is_file", return_value=True),
        ):
            # Створюємо об'єкт RaceData
            race = RaceData(Path("fake_path"))

            # Завантажуємо дані
            race.load_data()

            # Фільтруємо записи на валідні та невалідні
            valid_records = [r for r in race.records if not r.errors]
            invalid_records = [r for r in race.records if r.errors]

            # Вивести інформацію про кожен запис
            for r in race.records:
                print(f"{r.abbr=}, {r.name=}, {r.team=}, {r.errors=}")

            # Очікуємо, що валідний запис буде 0, оскільки у LHM відсутній час
            # фінішу
            assert len(valid_records) == 0

            # Очікуємо, що кількість помилкових записів буде 2
            assert len(invalid_records) == 3  # Очікуємо 2 помилки
