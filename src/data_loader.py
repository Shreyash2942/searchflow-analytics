"""Load the project's strict one-column integer CSV format."""

import csv
import re
from pathlib import Path

from src.data_processor import validate_dataset


def load_dataset(path: str | Path, expected_size: int | None = None) -> list[int]:
    """Load a CSV headed value, validate its integers, and optionally check count.

    Accept UTF-8 with an optional BOM and surrounding whitespace on integer
    cells. Reject missing/wrong headers, blank rows, extra columns, decimal
    fractions, and nonnumeric cells. Raise ValueError for invalid file content;
    preserve FileNotFoundError and other OSError types for filesystem failures.
    """
    source = Path(path)
    values = []
    try:
        with source.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            if next(reader, None) != ["value"]:
                raise ValueError(f"{source.name}: expected a single 'value' column header.")
            for row in reader:
                if len(row) != 1 or re.fullmatch(r"[+-]?[0-9]+", row[0].strip()) is None:
                    raise ValueError(
                        f"{source.name}: row ending at line {reader.line_num} "
                        "must contain exactly one integer."
                    )
                values.append(int(row[0].strip()))
    except (csv.Error, UnicodeError) as exc:
        raise ValueError(f"{source.name}: invalid UTF-8 CSV data ({exc}).") from exc
    validate_dataset(values, expected_size)
    return values
