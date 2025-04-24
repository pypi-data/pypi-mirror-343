import unittest
from chdb.dbapi import connect


class TestDBAPI(unittest.TestCase):
    def setUp(self):
        self.conn = connect()
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_select_version(self):
        """Test simple version query"""
        self.cur.execute("select version()")  # ClickHouse version
        row = self.cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(len(row), 1)
        self.assertIsInstance(row[0], str)

    def test_description(self):
        """Test cursor description"""
        # Test with multiple columns of different types
        self.cur.execute(
            """
            SELECT 
                1 as int_col,
                'test' as str_col,
                now() as time_col,
                NULL as null_col,
                '6bbd51ac-b0cc-43a2-8cb2-eab06ff7de7b'::UUID as uuid_col
        """
        )

        # Check description format
        self.assertIsNotNone(self.cur.description)
        self.assertEqual(len(self.cur.description), 5)

        # Check each column's metadata
        int_col = self.cur.description[0]
        str_col = self.cur.description[1]
        time_col = self.cur.description[2]
        null_col = self.cur.description[3]
        uuid_col = self.cur.description[4]

        # Check column names
        self.assertEqual(int_col[0], "int_col")
        self.assertEqual(str_col[0], "str_col")
        self.assertEqual(time_col[0], "time_col")
        self.assertEqual(null_col[0], "null_col")
        self.assertEqual(uuid_col[0], "uuid_col")

        # Check that type info is present
        self.assertTrue(int_col[1].startswith("Int") or int_col[1].startswith("UInt"))
        self.assertTrue(str_col[1] in ("String", "FixedString"))
        self.assertTrue(time_col[1].startswith("DateTime"))
        self.assertTrue(uuid_col[1] == "UUID")

        # Check that other fields are None as per DB-API 2.0
        for col in self.cur.description:
            self.assertEqual(len(col), 7)  # DB-API 2.0 specifies 7 fields
            self.assertTrue(
                all(x is None for x in col[2:])
            )  # All fields after name and type should be None

    def test_rowcount(self):
        """Test rowcount attribute"""
        # Test with empty result
        self.cur.execute("SELECT 1 WHERE 1=0")
        self.assertEqual(self.cur.rowcount, 0)

        # Test with single row
        self.cur.execute("SELECT 1")
        self.assertEqual(self.cur.rowcount, 1)

        # Test with multiple rows
        self.cur.execute("SELECT number FROM system.numbers LIMIT 10")
        self.assertEqual(self.cur.rowcount, 10)


if __name__ == "__main__":
    unittest.main()
