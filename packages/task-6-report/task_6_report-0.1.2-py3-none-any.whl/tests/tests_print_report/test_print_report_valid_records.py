from datetime import datetime
from pathlib import Path

import pytest

from race_report.report import RaceData, Record


@pytest.fixture
def race_data_valid():
    race = RaceData(Path("fake/path"))
    race.records = [
        Record(
            abbr="SVF",
            name="Sebastian Vettel",
            team="FERRARI",
            _start_time=datetime(2018, 5, 24, 12, 2, 0, 0),
            _end_time=datetime(2018, 5, 24, 12, 3, 20, 0),
        ),
        Record(
            abbr="LHM",
            name="Lewis Hamilton",
            team="MERCEDES",
            _start_time=datetime(2018, 5, 24, 12, 2, 0, 0),
            _end_time=datetime(2018, 5, 24, 12, 3, 0, 0),
        ),
        Record(
            abbr="KRF",
            name="Kimi Räikkönen",
            team="FERRARI",
            _start_time=datetime(2018, 5, 24, 12, 2, 0, 0),
            _end_time=datetime(2018, 5, 24, 12, 3, 30, 0),
        ),
    ]
    return race

def test_print_report_valid_records(race_data_valid, capsys):
    race_data_valid.print_report(order="asc")
    captured = capsys.readouterr()

    # Перевіримо весь вивід, щоб зрозуміти формат
    print(captured.out)  # Це допоможе побачити весь вивід

    # Перевіримо очікуваний формат і порядок
    output = captured.out.strip().splitlines()

    # Перевірка кількості записів
    assert len(output) >= 3

    # Перевірка першого запису (повинно бути Lewis Hamilton, бо він найшвидший)
    assert "Lewis Hamilton" in output[3]  # Перевірка імені
    assert "MERCEDES" in output[3]        # Перевірка команди
    assert "1:60,000" in output[3]        # Перевірка часу

    # Перевірка другого запису (Sebastian Vettel)
    assert "Sebastian Vettel" in output[4]
    assert "FERRARI" in output[4]
    assert "1:80,000" in output[4]  # Перевірка часу

    # Перевірка третього запису (Kimi Räikkönen)
    assert "Kimi Räikkönen" in output[5]
    assert "FERRARI" in output[5]
    assert "1:90,000" in output[5]  # Перевірка часу