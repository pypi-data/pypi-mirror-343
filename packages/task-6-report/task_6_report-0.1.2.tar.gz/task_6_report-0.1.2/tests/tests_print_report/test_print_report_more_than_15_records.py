from datetime import datetime, timedelta
from pathlib import Path

import pytest

from race_report.report import RaceData, Record


@pytest.fixture
def race_data_more_than_15():
    race = RaceData(Path("fake/path"))

    base_time = datetime(2018, 5, 24, 12, 0, 0)

    race.records = [
        Record(
            abbr=f"DRV{i:02}",
            name=f"Driver {i}",
            team=f"TEAM{i%3}",
            _start_time=base_time,
            _end_time=base_time + timedelta(seconds=60 + i),  # трохи різні lap_time
        )
        for i in range(16)
    ]

    return race


def test_print_report_more_than_15_records(race_data_more_than_15, capsys):
    race_data_more_than_15.print_report(order="asc")
    captured = capsys.readouterr()
    print(captured.out)
    output = captured.out.strip().splitlines()

    # Перевірка, що надруковано 16 записів
    valid_section_start = output.index("=== Валідні записи ===") + 1
    valid_section = output[valid_section_start:]

    # Має бути щонайменше 16 рядків + 1 роздільна лінія
    assert len(valid_section) >= 17

    # Має бути горизонтальна лінія після 15 запису
    line_after_15 = valid_section[15]
    assert line_after_15 == "-" * len(line_after_15), (
        "Має бути горизонтальна лінія після 15-го запису"
    )

