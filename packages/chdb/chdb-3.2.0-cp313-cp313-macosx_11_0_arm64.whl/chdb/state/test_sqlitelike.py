import unittest
from datetime import datetime, date
from chdb.state.sqlitelike import connect


class TestCursor(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_basic_types(self):
        # Test basic types including NULL values
        self.cursor.execute(
            """
            SELECT 
                42 as int_val,
                3.14 as float_val,
                'hello' as str_val,
                true as bool_val,
                NULL as null_val
        """
        )
        row = self.cursor.fetchone()
        self.assertEqual(row, (42, 3.14, "hello", True, None))

    def test_date_time_types(self):
        # Test date and datetime types with various formats
        self.cursor.execute(
            """
            SELECT 
                toDateTime('2024-03-20 15:30:00') as datetime_str,
                toDateTime64('2024-03-20 15:30:00.123456', 6) as datetime64_str,
                toDate('2024-03-20') as date_str,
                toDateTime(1710945000) as datetime_ts,  -- 2024-03-20 15:30:00
                toDate(19437) as date_ts  -- 2024-03-20 (days since 1970-01-01)
        """
        )
        row = self.cursor.fetchone()
        self.assertEqual(len(row), 5)

        # Test datetime string format
        self.assertIsInstance(row[0], datetime)
        self.assertEqual(row[0].strftime("%Y-%m-%d %H:%M:%S"), "2024-03-20 15:30:00")

        # Test datetime64 with microseconds
        self.assertIsInstance(row[1], datetime)
        self.assertEqual(
            row[1].strftime("%Y-%m-%d %H:%M:%S.%f"), "2024-03-20 15:30:00.123456"
        )

        # Test date string format
        self.assertIsInstance(row[2], date)
        self.assertEqual(row[2].isoformat(), "2024-03-20")

        # Test datetime from timestamp
        self.assertIsInstance(row[3], datetime)
        self.assertEqual(row[3].strftime("%Y-%m-%d %H:%M:%S"), "2024-03-20 15:30:00")

        # Test date from timestamp
        self.assertIsInstance(row[4], date)
        self.assertEqual(row[4].isoformat(), "2024-03-20")

    def test_array_types(self):
        # Test array types (should be converted to string)
        self.cursor.execute(
            """
            SELECT 
                [1, 2, 3] as int_array,
                ['a', 'b', 'c'] as str_array
        """
        )
        row = self.cursor.fetchone()
        self.assertIsInstance(row[0], str)
        self.assertIsInstance(row[1], str)

    def test_complex_types(self):
        # Test more complex ClickHouse types
        self.cursor.execute(
            """
            SELECT 
                toDecimal64(123.45, 2) as decimal_val,
                toFixedString('test', 10) as fixed_str_val,
                tuple(1, 'a') as tuple_val,
                map('key', 'value') as map_val
        """
        )
        row = self.cursor.fetchone()
        # All complex types should be converted to strings
        for val in row:
            self.assertIsInstance(val, (str, type(None)))

    def test_fetch_methods(self):
        # Test different fetch methods
        self.cursor.execute(
            """
            SELECT number 
            FROM system.numbers 
            LIMIT 5
        """
        )

        # Test fetchone
        self.assertEqual(self.cursor.fetchone(), (0,))

        # Test fetchmany
        self.assertEqual(self.cursor.fetchmany(2), ((1,), (2,)))

        # Test fetchall
        self.assertEqual(self.cursor.fetchall(), ((3,), (4,)))

        # Test fetchone after end
        self.assertIsNone(self.cursor.fetchone())

    def test_empty_result(self):
        # Test empty result handling
        self.cursor.execute("SELECT 1 WHERE 1=0")
        self.assertIsNone(self.cursor.fetchone())
        self.assertEqual(self.cursor.fetchall(), ())

    def test_iterator(self):
        # Test cursor as iterator
        self.cursor.execute(
            """
            SELECT number 
            FROM system.numbers 
            LIMIT 3
        """
        )
        rows = [row for row in self.cursor]
        self.assertEqual(rows, [(0,), (1,), (2,)])

    def test_error_handling(self):
        # Test invalid SQL
        with self.assertRaises(Exception):
            self.cursor.execute("SELECT invalid_column")

    def test_large_result(self):
        # Test handling of larger result sets
        self.cursor.execute(
            """
            SELECT 
                number,
                toString(number) as str_val,
                toDateTime('2024-03-20 15:30:00') + interval number second as time_val
            FROM system.numbers
            LIMIT 1000
        """
        )
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 1000)
        self.assertEqual(rows[0], (0, "0", datetime(2024, 3, 20, 15, 30, 0)))
        self.assertEqual(rows[-1], (999, "999", datetime(2024, 3, 20, 15, 46, 39)))

    def test_column_names(self):
        # Test that column names are stored and accessible
        self.cursor.execute(
            """
            SELECT 
                42 as int_col,
                'hello' as str_col,
                now() as time_col
        """
        )

        # Test the column names method
        self.assertEqual(self.cursor.column_names(), ["int_col", "str_col", "time_col"])

        # Test the column types method
        self.assertEqual(len(self.cursor.column_types()), 3)

        # Test the description property (DB-API 2.0)
        description = self.cursor.description
        self.assertEqual(len(description), 3)
        self.assertEqual(description[0][0], "int_col")  # First column name
        self.assertEqual(description[1][0], "str_col")  # Second column name

        # Test fetchone
        row = self.cursor.fetchone()
        self.assertEqual(len(row), 3)

        # Test that all data was properly converted
        self.assertIsInstance(row[0], int)
        self.assertIsInstance(row[1], str)
        self.assertIsInstance(
            row[2], (str, datetime)
        )  # May be str or datetime depending on conversion

    def test_uuid_type(self):
        # Test UUID type handling
        self.cursor.execute(
            "SELECT '6bbd51ac-b0cc-43a2-8cb2-eab06ff7de7b'::UUID as uuid_val"
        )
        row = self.cursor.fetchone()
        self.assertEqual(row[0], "6bbd51ac-b0cc-43a2-8cb2-eab06ff7de7b")

        # Test UUID in a more complex query
        self.cursor.execute(
            """
            SELECT 
                '6bbd51ac-b0cc-43a2-8cb2-eab06ff7de7b'::UUID as uuid_val1,
                NULL::UUID as uuid_val2
        """
        )
        row = self.cursor.fetchone()
        self.assertEqual(row[0], "6bbd51ac-b0cc-43a2-8cb2-eab06ff7de7b")
        self.assertIsNone(row[1])

    def test_null_handling(self):
        # Test NULL handling
        self.cursor.execute("SELECT NULL")
        row = self.cursor.fetchone()
        self.assertEqual(row, (None,))

        # Test NULL with different types
        self.cursor.execute(
            """
            SELECT 
                NULL::Int32 as null_int,
                NULL::String as null_str,
                NULL::UUID as null_uuid,
                NULL::DateTime as null_datetime,
                NULL::Date as null_date
        """
        )
        row = self.cursor.fetchone()
        self.assertEqual(len(row), 5)
        for val in row:
            self.assertIsNone(val)


if __name__ == "__main__":
    unittest.main()
