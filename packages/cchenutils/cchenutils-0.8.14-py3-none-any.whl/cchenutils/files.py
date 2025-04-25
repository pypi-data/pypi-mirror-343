import csv
import json
import os
import re

from .dictutils import Dict


def csvwrite(fp, headers, data):
    writeheader = not os.path.exists(fp)
    rows = data if isinstance(data, list) else [data]
    rows = (dict(zip(headers, Dict(d).gets(headers))) for d in rows)

    with open(fp, 'a', encoding='utf-8') as o:
        writer = csv.DictWriter(o, fieldnames=headers, lineterminator='\n')
        if writeheader:
            writer.writeheader()
        writer.writerows(rows)


def jsonwrite(fp, data):
    rows = data if isinstance(data, list) else [data]
    with open(fp, 'a', encoding='utf-8') as o:
        o.writelines(json.dumps(d) + '\n' for d in rows)


def writer(queue):
    """
    The function listens to `queue` for input tuples for CSV and JSON files.
    The function continues to process items until it encounters the special 'STOP' message in the queue.

    - For CSV files, the tuple contains:
      - `fp` (str): The file path.
      - `data` (dict or list of dicts): The data to be written.
      - `headers` (list): The headers for the CSV columns.
      - `scrape_time` (optional, datetime in str): The time of scraping, added as the first column.
    - For JSON files, the tuple contains:
      - `fp` (str): The file path.
      - `data` (dict or list of dicts): The data to be written.

    Raises:
        KeyboardInterrupt: If the function is interrupted manually.
        Exception: Any other unexpected error that might occur during file writing.
    """
    while True:
        try:
            inp = queue.get()
            if inp == 'STOP':
                break
            fp, data, *args = inp
            match fp.split('.')[-1]:
                case 'csv':
                    headers = args[0]
                    if len(args) > 1:
                        headers = ['scrape_time'] + headers
                        data['scrape_time'] = args[1]
                    csvwrite(fp, headers, data)
                case 'json':
                    jsonwrite(fp, data)
                case _:
                    print(f'Unsupported file type for {fp}')
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f'Error in writer: {e}')


def read_id(fp, usecols, filter=None):
    """
    Reads specific columns from a CSV file, optionally filtering the rows based on specified conditions.

    The function loads data from a CSV file (`fp`) and extracts values from the specified columns (`usecols`).
    Rows can be filtered according to conditions specified in the `filter` argument. The function returns a
    set of unique values from the selected columns, based on the filtering criteria.

    Args:
        fp (str): The file path to the CSV file.
        usecols (str or tuple): The column name(s) to extract from the CSV file.
                                 Can be a single column name (str) or a tuple of column names for multiple columns.
        filter (dict, optional): A dictionary specifying filtering conditions for the rows. The dictionary should
                                  have 'include' and/or 'exclude' as keys, with the associated values being
                                  dictionaries where keys are column names and values are the expected value(s).
                                  If not provided, no filtering is applied.

    Returns:
        set: A list of unique values extracted from the specified columns, with rows filtered according to the filter.

    Example:
        # Read a single column "mid" from the CSV file with `status`=='active
        read_id('data.csv', 'mid', filter={'include': {'status': 'active'}})

        # Read multiple columns ("mid", "cid") with `status` being empty
        read_id('data.csv', ('mid', 'cid'), filter={'exclude': {'status': True}})
    """
    if not os.path.exists(fp):
        return set()

    if isinstance(usecols, str):
        usecols = (usecols,)

    def matches(expected, value):
        match expected:
            case True:
                return bool(value)
            case False:
                return not bool(value)
            case list() | set() | tuple():
                return value in expected
            case re.Pattern():
                return bool(value and expected.search(value))
            case func if callable(func):
                return func(value)
            case _:
                return value == expected

    def row_passes_filter(row):
        if not filter:
            return True

        for mode, conditions in filter.items():
            is_include = (mode == 'include')
            for field, expected in conditions.items():
                value = row.get(field)
                if matches(expected, value) != is_include:
                    return False
        return True

    def unique(list_of_items):
        seen = set()
        rows = []
        for row in list_of_items:
            if row not in seen:
                rows.append(row)
                seen.add(row)
        return rows

    with open(fp, encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        return unique(
            tuple(row[col] for col in usecols) if len(usecols) > 1 else row[usecols[0]]
            for row in csvreader if row_passes_filter(row)
        )


def read_id_range(fp, id_field, range_field):
    """
    Reads a CSV file and obtains the minimum and maximum for a specified range field, grouped by an ID field.

    The function loads data from a CSV file (`fp`), and for each unique value in the `id_field`, it calculates the
    minimum and maximum values from the `range_field`. The `range_field` values must be convertible to integers.
    The results are returned as a dictionary where the keys are the values from the `id_field`, and the values are
    tuples containing the minimum and maximum values of the `range_field`.

    Args:
        fp (str): The file path to the CSV file.
        id_field (str): The name of the field used to group the rows.
        range_field (str): The name of the field whose minimum and maximum values are calculated for each group.
                          The values in this field must be convertible to integers.

    Returns:
        dict: A dictionary where the keys are the values from the `id_field`, and the values are tuples with the
              minimum and maximum values from the `range_field` for each unique `id_field`.

    Example:
        # Read a CSV and calculate the min and max values of 'cid' for each 'mid' field
        > read_id_range('data.csv', 'mid', 'cid')
        {'A': (1, 5), 'B': (2, 8)}
    """
    if not os.path.exists(fp):
        return {}

    result = {}
    with open(fp, encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            id_value, range_value = row[id_field], int(row[range_field])
            if id_value not in result:
                result[id_value] = (range_value, range_value)
            else:
                current_min, current_max = result[id_value]
                result[id_value] = (min(current_min, range_value), max(current_max, range_value))
    return result
