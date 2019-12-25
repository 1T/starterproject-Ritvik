"""Core functions."""
from typing import List


class TSVFileProcessor:
    """
    TSV (tab-separated values, similar to CSV) Files are commonly
    used as a medium for brokers and marketplaces to exchange
    information about their inventory.

    This class provides utilities and a single method `total_value`,
    that will calculate the total value of inventory that is being
    broad-casted, which is important for verification and billing
    purposes.

    Note: For more info on the calculation, please see the
    documentation on the `total_value` method.

    """

    def __init__(self, file_contents: str):
        self.rows = file_contents.strip().split('\n')
        self._total_value = 0.0
        if self.rows:
            self.header_row = self.rows.pop(0)
            try:
                FileGlobals.process_headers(self.header_row)
            except ValueError as e:
                # Handle the case when either the 'Quantity' or 'Cost' column
                # headers are missing.
                self.rows = []
                print(e)
        else:
            self.header_row = []

    @property
    def total_value(self) -> float:
        """Calculate the "total value" of inventory present in the file.

        The important columns are ‘Cost’ and ‘Quantity’, which will be there
        in all files. Please refer to the :class:`FileGlobals` class for the
        declarations on these column header names.

        The value of a single row is calculated by multiplying the ‘Cost’ field
        with the ‘Quantity’ field. The value of the whole file is calculated by
        adding up the value of each row in it.

        :rtype: float
        :return: The "total value" of the inventory being broadcasted
        """
        if not self.rows:
            return self._total_value

        self._total_value = 0.0

        for r in self.rows:
            self._total_value += Row(r)()

        return self._total_value

    def __repr__(self):
        """Get a string representation of the TSV File's contents."""
        rows = self._row_objects()
        parts = [f'{self.__class__.__name__}(',
                 f'  num_rows={len(rows)},',
                 f'{FileGlobals.string(2)},']
        parts.extend(
            [r.string(False, 2) + ',' for r in rows])
        parts.append(')')

        return '\n'.join(parts)

    def _row_objects(self):
        """Return the list of :class:`Row` objects for the file"""
        row_objects = []
        if not self.rows:
            return row_objects
        for r in self.rows:
            row_objects.append(Row(r))
            row_objects[-1]()

        return row_objects


class FileGlobals:
    """
    This class manages known globals for a TSV file, including the header names
    for the 'Quantity' and 'Cost' columns (case-insensitive). It also provides
    a utility method to process column headers in the file, which is generally
    the first line of the file.

    """
    quantity_header = 'Quantity'
    cost_header = 'Cost'

    headers: List[str]
    quantity_index: int
    cost_index: int

    @classmethod
    def process_headers(cls, header_line: str):
        """Calculates the indices for the 'Quantity' and 'Cost' columns

        :param header_line: The line containing the column headers,
          which will generally be the first line in the file.

        :raises: ValueError, when either the 'Quantity' or 'Cost' columns
          headers could not be found in the file.
        """
        cls._reset_globals()

        cls.headers = Row.get_tab_separated_values(header_line)

        for i, h in enumerate(cls.headers):
            h = h.lower()
            if h == cls.quantity_header:
                cls.quantity_index = i
                if cls._are_cost_and_quantity_fields_found():
                    break
            elif h == cls.cost_header:
                cls.cost_index = i
                if cls._are_cost_and_quantity_fields_found():
                    break
        else:
            msg = (f'Either of the required columns headers (case-insensitive) '
                   f'were not found:\n'
                   f'  {(cls.cost_header, cls.quantity_header)}')
            raise ValueError(msg)

    @classmethod
    def _reset_globals(cls):
        """Reset globals for the file."""
        cls.headers = []
        cls.quantity_index = -1
        cls.cost_index = -1

        cls.quantity_header = cls.quantity_header.lower()
        cls.cost_header = cls.cost_header.lower()

    @classmethod
    def _are_cost_and_quantity_fields_found(cls):
        """Return true if both 'Quantity' and 'Cost' column headers are found."""
        return cls.quantity_index != -1 and cls.cost_index != -1

    @classmethod
    def string(cls, start_indent_level=0):
        """Return a string representation of the File Globals."""
        indent = start_indent_level * ' '
        return (f'{indent}{cls.__name__}(\n'
                f'{indent}  headers={cls.headers},\n'
                f'{indent}  quantity_index={cls.quantity_index},\n'
                f'{indent}  cost_index={cls.cost_index},\n'
                f'{indent})')


class Row:
    """
    Contains utilities for processing lines in a TSV file where each line
    is assumed to be a row of data.

    See the `__call__` method which calculates and returns the "total value"
    of a row.

    """

    def __init__(self, line: str):
        self.columns = self.get_tab_separated_values(line)
        self.cost, self.quantity = 0.0, 0

    def __call__(self) -> float:
        """
        Calculate the "total value" for a row, which is given as the product
        of the 'Quantity' and 'Cost' columns.

        :rtype: float
        :return: The total value of the current row
        """
        try:
            self.cost = float(self.columns[FileGlobals.cost_index])
            self.quantity = int(self.columns[FileGlobals.quantity_index])
            # Calculate the total value for the row
            self.total = self.cost * self.quantity
        except (ValueError, IndexError) as e:
            print(f'Error in processing row: {e}\n'
                  f'  Columns: {self.columns}')
            self.total = 0.0

        return self.total

    @staticmethod
    def get_tab_separated_values(line: str) -> List[str]:
        """Split a `line` on the tab character and return the row's `columns`"""
        return line.split('\t')

    def __repr__(self):
        """
        Get a string representation of the current row,
        omitting the File Globals.
        """
        return self.string(False)

    def string(self, show_globals=True, start_indent_level=0):
        """Return a string representation of the current row.

        :type show_globals: bool
        :param show_globals: When enabled (default), the File
          Globals are included in the string representation.

        :type start_indent_level: int
        :param start_indent_level: Initial depth of indent
          for the string representation (default none)
        """
        indent = start_indent_level * ' '
        string = f'{indent}{self.__class__.__name__}(\n'
        if show_globals:
            string += f'{FileGlobals.string(start_indent_level + 2)},\n'
        string += (f'{indent}  columns={self.columns},\n'
                   f'{indent}  cost={self.cost},\n'
                   f'{indent}  quantity={self.quantity},\n'
                   f'{indent}  total_value={self.total},\n'
                   f'{indent})')

        return string
