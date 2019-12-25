import unittest

from starterproject.core import TSVFileProcessor


class TestCore(unittest.TestCase):

    def assertTotalEquals(self, expected, actual):
        self.assertEqual(expected, actual,
                         "Total value not as expected")

    def test_total_value_success_sample_input(self):
        """Test case for sample working input."""
        with open('sample-input') as f:
            data = f.read()

        expected_total = 754651.29

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)

    def test_total_value_success_quantity_and_cost_zero(self):
        data = """
        dummy-col1\tdummy-col2\tquantity\tdummy-col3\tcost
        -\tsample value\t0\t-\t0
        """
        expected_total = 0

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)

    def test_total_value_success_quantity_and_cost_zero_2(self):
        data = """
        dummy-col1\tdummy-col2\tquantity\tdummy-col3\tcost
        -\tsample value\t4\t-\t0
        -\t-\t0\t-\t999.9
        """
        expected_total = 0

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)

    def test_total_value_success_sample_input_2(self):
        data = """
        dummy-col1\tdummy-col2\tquantity\tdummy-col3\tcost
        -\tsample value\t0\t-\t7
        -\tsample value\t1\tanother sample value\t0.15
        -\tsample value\t2\tanother sample value\t5.25
        """
        expected_total = 10.65

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)

    def test_total_value_success_sample_input_3(self):
        data = """
        dummy-col1\tCOST\tdummy-col3\tQuAnTiTy\tdummy-col4
        -\t0.00\t-\t17\t-
        -\t3\t-\t5\t-
        -\t5.21\t-\t1\t-
        """
        expected_total = 20.21

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)

    def test_total_value_warning_non_numeric_quantity_or_cost(self):
        data = """
        dummy-col1\tdummy-col2\tquantity\tdummy-col3\tcost
        -\tsample value\tZero\t-\t0
        """
        expected_total = 0

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)

    def test_total_value_warning_cost_header_not_found(self):
        data = """
        dummy-col1\tdummy-col2\tquantity\tdummy-col3\tcsot
        -\tsample value\t99\t-\t99
        """
        expected_total = 0

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)

    def test_total_value_warning_quantity_header_not_found(self):
        data = """
        dummy-col1\tdummy-col2\tunknown-quantity\tdummy-col3\tCOST
        -\tsample value\t99\t-\t99
        """
        expected_total = 0

        t = TSVFileProcessor(data)

        self.assertTotalEquals(expected_total, t.total_value)
