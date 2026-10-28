import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from ledger import transfer, upsert_sql  # noqa: E402


class TransferTest(unittest.TestCase):
    def test_moves_amount(self):
        self.assertEqual(transfer({"a": 10}, "a", "b", 3), {"a": 7, "b": 3})

    def test_rejects_overdraft(self):
        with self.assertRaises(ValueError):
            transfer({"a": 1}, "a", "b", 3)

    def test_sql_mentions_every_account(self):
        sql = upsert_sql({"a": 1, "b": 2})
        self.assertIn("('a', 1)", sql)
        self.assertIn("('b', 2)", sql)


if __name__ == "__main__":
    unittest.main()
