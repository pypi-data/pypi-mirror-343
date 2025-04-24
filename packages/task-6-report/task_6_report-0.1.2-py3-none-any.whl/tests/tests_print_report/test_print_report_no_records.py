import pytest
from race_report.report import RaceData


@pytest.fixture
def race_data_no_records():
    race_data = RaceData(folder="test_folder")
    race_data.records = []  # Порожній список записів
    return race_data


def test_print_report_no_records(race_data_no_records, capsys):
    # Викликаємо print_report
    race_data_no_records.print_report(order="asc")

    # Захоплюємо вивід
    captured = capsys.readouterr()
    output = captured.out.strip().splitlines()

    # Перевірка, чи виводиться повідомлення про відсутність записів
    assert "Знайдено 0 записів" in output
