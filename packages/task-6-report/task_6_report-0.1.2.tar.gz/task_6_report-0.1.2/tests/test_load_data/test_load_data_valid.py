import tempfile
from pathlib import Path
from race_report.report import RaceData
from datetime import datetime

def test_load_data_creates_valid_records():
    # Створюємо тимчасову папку з потрібними файлами
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # abbreviations.txt
        (temp_path / "abbreviations.txt").write_text(
            "SVF_Sebastian Vettel_FERRARI\n"
            "LHM_Lewis Hamilton_MERCEDES\n",
            encoding="utf-8"
        )

        # start.log
        (temp_path / "start.log").write_text(
            "SVF2018-05-24_12:02:58.917\n"
            "LHM2018-05-24_12:03:18.456\n",
            encoding="utf-8"
        )

        # end.log
        (temp_path / "end.log").write_text(
            "SVF2018-05-24_12:04:03.332\n"
            "LHM2018-05-24_12:04:05.332\n",
            encoding="utf-8"
        )

        # Створюємо об’єкт RaceData і завантажуємо дані
        race = RaceData(temp_path)
        race.load_data()

        # Маємо мати 2 валідні записи
        valid_records = [r for r in race.records if not r.errors]
        assert len(valid_records) == 2

        # Перевіримо одного з них
        vettel = next(r for r in valid_records if r.abbr == "SVF")
        assert vettel.name == "Sebastian Vettel"
        assert vettel.team == "FERRARI"
        assert vettel.lap_time == datetime(2018, 5, 24, 12, 4, 3, 332000) - \
                                   datetime(2018, 5, 24, 12, 2, 58, 917000)
