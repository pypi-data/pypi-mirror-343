import pytest
from pathlib import Path
from race_report.report import RaceData, Record


@pytest.mark.parametrize("num_participants", [100, 200, 300])  # Параметризація тесту для різної кількості учасників
def test_load_data_many_participants(monkeypatch, num_participants):
    fake_path = Path("fake_path")

    # Генеруємо учасників
    def mock_read_abbreviations(self):
        records = {}
        for i in range(1, num_participants + 1):
            record = Record(abbr=f"ABBR{i}", name=f"Driver {i}", team="TeamX")
            records[f"ABBR{i}"] = record
        return records, []  # повертаємо кортеж

    def mock_read_times(self, filename, is_start):
        times = {}
        for i in range(1, num_participants + 1):
            if filename == "start.log":
                times[f"ABBR{i}"] = f"2025-05-24 12:{i:02d}:00.000" if i % 2 == 0 else None
            elif filename == "end.log":
                times[f"ABBR{i}"] = f"2025-05-24 12:{i + 1:02d}:00.000" if i % 2 != 0 else None
        return times, []

    # Патчимо методи
    monkeypatch.setattr(RaceData, "read_abbreviations", mock_read_abbreviations)
    monkeypatch.setattr(RaceData, "read_times", mock_read_times)

    race = RaceData(fake_path)
    race.load_data()

    # Перевіряємо кількість записів
    assert len(race.records) == num_participants

    # Перевірка на наявність помилок
    for i in range(1, num_participants + 1):
        abbr = f"ABBR{i}"
        record = next((r for r in race.records if r.abbr == abbr), None)
        assert record is not None, f"Запис для {abbr} не знайдено"

        # Перевіряємо помилки та часи
        if i % 2 == 0:
            assert record.start_time == f"2025-05-24 12:{i:02d}:00.000"
            assert record.end_time is None
            assert "Немає end часу" in record.errors
        else:
            assert record.start_time is None
            assert record.end_time == f"2025-05-24 12:{i + 1:02d}:00.000"
            assert "Немає start часу" in record.errors