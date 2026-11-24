import sqlite3
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from pipeline import engineer_features, save_data


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.raw = pd.DataFrame({
            "coin": ["bitcoin"] * 3,
            "timestamp": ["2025-01-01", "2025-01-02", "2025-01-03"],
            "price": [100.0, 110.0, 121.0],
        })

    def test_features(self):
        result = engineer_features(self.raw)
        self.assertAlmostEqual(result["return"].iloc[1], 0.1)
        self.assertAlmostEqual(result["price_indexed"].iloc[2], 121)
        self.assertAlmostEqual(result["ma7"].iloc[2], 331 / 3)

    def test_empty_data(self):
        with self.assertRaises(ValueError):
            engineer_features(pd.DataFrame())

    def test_database(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.db"
            save_data(engineer_features(self.raw), path)
            with sqlite3.connect(path) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM crypto_prices").fetchone()[0], 3)
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM crypto_summary").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
