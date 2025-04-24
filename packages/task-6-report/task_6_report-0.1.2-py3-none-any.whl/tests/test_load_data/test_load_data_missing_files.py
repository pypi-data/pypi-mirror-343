from pathlib import Path
from race_report.report import RaceData, Record

def test_load_data_missing_start_and_end_logs(monkeypatch, capsys):
    fake_path = Path("fake_path")

    def mock_read_abbreviations(self):
        valid = {"SVF": Record(abbr="SVF", name="Sebastian Vettel", team="FERRARI")}
        invalid = []  # Тут можна додати невалідні записи, якщо потрібно
        return valid, invalid

    def mock_read_times(self, filename, is_start):
        if filename == "start.log":
            return {}, [Record(abbr="", errors=[f"Файл {filename} не знайдено."])]
        elif filename == "end.log":
            return {}, [Record(abbr="", errors=[f"Файл {filename} не знайдено."])]
        else:
            raise ValueError(f"Невідомий файл: {filename}")

    monkeypatch.setattr(RaceData, "read_abbreviations", mock_read_abbreviations)
    monkeypatch.setattr(RaceData, "read_times", mock_read_times)

    race = RaceData(fake_path)
    race.load_data()

    # Перевіряємо стандартний вивід
    captured = capsys.readouterr()

    # Перевіряємо, чи є повідомлення про відсутні файли
    assert "Файл start.log не знайдено." in captured.out
    assert "Файл end.log не знайдено." in captured.out

    # Перевіряємо записи
    assert len(race.records) == 3

    error_messages = [err for r in race.records for err in r.errors]
    assert "Файл start.log не знайдено." in error_messages
    assert "Файл end.log не знайдено." in error_messages

    svf = next(r for r in race.records if r.abbr == "SVF")
    assert "Немає start часу для SVF" in svf.errors
    assert "Немає end часу для SVF" in svf.errors

    print(captured.out)  # Це виведе весь стандартний вивід