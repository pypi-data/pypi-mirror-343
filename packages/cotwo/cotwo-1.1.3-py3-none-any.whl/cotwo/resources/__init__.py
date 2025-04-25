from pathlib import Path

import polars as pl


class PeriodicTable:
    def __init__(self) -> None:
        self.pse: pl.DataFrame = pl.read_json(
            Path(__file__).parent / "periodic_table.json"
        )

    def get_element(self, symbol: str) -> dict:
        return self.pse.filter(pl.col("symbol") == symbol).to_dict(as_series=False)


PERIODIC_TABLE = PeriodicTable()
