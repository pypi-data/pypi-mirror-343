# Пакет task_6_report

`task_6_report` — Python package for analyzing Formula 1 race results: loading logs, building reports, output via CLI.

---

## 
Installation

```bash
pip install task_6_report
```

---

## 
Using

```python
from race_report.report import RaceData

data = RaceData()
data.load_data('abbreviations.txt', 'start.log', 'end.log')
report = data.build_report(order='asc')
data.print_report(report)
```

### An example of a report:

```
1. DRR_Daniel Ricciardo | RED BULL RACING TAG HEUER | 1:14.345
2. SVF_Sebastian Vettel | FERRARI | 1:14.788
...
```

---

## Call in GitBash GitBash (CLI)

Direct path transfer:

```bash
task-6-report --abbreviations abbreviations.txt --start start.log --end end.log --order asc
```

Or in reverse order:

```bash
task-6-report --abbreviations abbreviations.txt --start start.log --end end.log --order desc
```

---

## The structure of the project

```
task_6_report/

├── race_report/
│   ├── __init__.py
│   └── report.py

├── tests/
│   ├── __init__.py
│   ├── tests_load_data/
│   ├── tests_build_report/
│   ├── tests_print_report/
│   ├── tests_read_abbreviations/
│   ├── test_race_report(CLI)/


├── LICENSE
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## Testing

To run the tests, execute:

```bash
pytest tests/
```

---

## License

This project is licensed under the MIT License.