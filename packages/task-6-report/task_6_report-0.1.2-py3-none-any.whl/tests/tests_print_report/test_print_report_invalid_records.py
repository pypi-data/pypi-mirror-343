from datetime import datetime
from pathlib import Path

import pytest

from race_report.report import RaceData, Record


@pytest.fixture
def race_data_invalid():
    race = RaceData(Path("fake/path"))
    race.records = [
        Record(
            abbr="SVF",
            name="Sebastian Vettel",
            team="FERRARI",
            _start_time=None,
            _end_time=datetime(2018, 5, 24, 12, 3, 20),
            errors=["Missing start time"]
        ),
        Record(
            abbr="LHM",
            name="Lewis Hamilton",
            team="MERCEDES",
            _start_time=datetime(2018, 5, 24, 12, 2, 0),
            _end_time=None,
            errors=["Missing end time"]
        ),
    ]
    return race


def test_print_report_invalid_records(race_data_invalid, capsys):
    race_data_invalid.print_report(order="asc")
    captured = capsys.readouterr()
    output = captured.out.strip().splitlines()

    # Перевірка заголовків
    assert "=== Невалідні записи ===" in output

    # Перевірка першого невалідного запису
    assert any("Sebastian Vettel" in line and "Missing start time" in line for line in output)

    # Перевірка другого невалідного запису
    assert any("Lewis Hamilton" in line and "Missing end time" in line for line in output)
