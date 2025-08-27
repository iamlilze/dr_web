import unittest
from app import InMemoryDB


class TestInMemoryDB(unittest.TestCase):
    def test_set_get_unset(self):
        db = InMemoryDB()
        db.set("A", "10")
        self.assertEqual(db.get("A"), "10")
        db.unset("A")
        self.assertIsNone(db.get("A"))

    def test_counts_and_find(self):
        db = InMemoryDB()
        db.set("A", "10")
        db.set("B", "20")
        db.set("C", "10")
        self.assertEqual(db.counts("10"), 2)
        self.assertEqual(set(db.find("10")), {"A", "C"})
        self.assertEqual(db.counts("30"), 0)
        self.assertEqual(db.find("30"), [])

    def test_transactions(self):
        db = InMemoryDB()
        db.set("A", "10")
        db.begin()
        db.set("A", "20")
        self.assertEqual(db.get("A"), "20")
        db.rollback()
        self.assertEqual(db.get("A"), "10")

    def test_nested_transactions(self):
        db = InMemoryDB()
        db.set("A", "10")
        db.begin()
        db.set("A", "20")
        db.begin()
        db.set("A", "30")
        self.assertEqual(db.get("A"), "30")
        db.rollback()
        self.assertEqual(db.get("A"), "20")
        db.commit()
        self.assertEqual(db.get("A"), "20")


if __name__ == "__main__":
    unittest.main()
