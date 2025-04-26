import csv
import json
import os
import re
from ordered_set import OrderedSet
from .dictutils import Dict


def csv_write(fp, data, headers=None):
    writeheader = not os.path.exists(fp) and headers is not None
    rows = data if isinstance(data, list) else [data]
    rows = (dict(zip(headers, Dict(d).gets(headers, serialize=True))) for d in rows)

    with open(fp, 'a', encoding='utf-8') as o:
        writer = csv.DictWriter(o, fieldnames=headers, lineterminator='\n')
        if writeheader:
            writer.writeheader()
        writer.writerows(rows)


def jsonl_write(fp, data):
    rows = data if isinstance(data, list) else [data]
    with open(fp, 'a', encoding='utf-8') as o:
        o.writelines(json.dumps(d) + '\n' for d in rows)


def write(fp, data, *args):
    """
    Writes data to a file based on its extension.

    Supported formats:
    - For CSV files (.csv), the tuple contains:
      - `fp` (str): The file path.
      - `data` (dict or list of dicts): The data to be written.
      - `headers` (iterable): The headers for the CSV columns.
      - `scrape_time` (optional, datetime in str): The time of scraping, added as the first column.
    - For JSON Line (.jsonl) files, the tuple contains:
      - `fp` (str): The file path.
      - `data` (dict or list of dicts): The data to be written.
    """
    match os.path.splitext(fp)[1].lower():
        case '.csv':
            match len(args):
                case 0:
                    headers = None
                case 1:
                    headers = args[0]
                case _:
                    headers = ['scrape_time'] + args[0]
                    data['scrape_time'] = args[1]
            csv_write(fp, data, headers)
        case '.jsonl':
            jsonl_write(fp, data)
        case _:
            print(f'Unsupported file type for {fp}')


def read_id(fp, usecols, filter=None) -> OrderedSet:
    """
    Reads specific columns from a CSV file, optionally filtering the rows based on specified conditions.

    The function loads data from a CSV file (`fp`) and extracts values from the specified columns (`usecols`).
    Rows can be filtered according to conditions specified in the `filter` argument. The function returns a
    set of unique values from the selected columns, based on the filtering criteria.

    Args:
        fp (str): The file path to the CSV file.
        usecols (str | iterable): The column name(s) to extract from the CSV file.
                                  Can be one name (str) or names (iterable) for multiple fields.
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
        return OrderedSet()

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

    with open(fp, encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        return OrderedSet(tuple(row[col] for col in usecols) if len(usecols) > 1 else row[usecols[0]]
                          for row in csvreader if row_passes_filter(row))


def read_id_range(fp, id_field, range_field) -> Dict:
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
        Dict: A dictionary where the keys are the values from the `id_field`, and the values are tuples with the
              minimum and maximum values from the `range_field` for each unique `id_field`.

    Example:
        # Read a CSV and calculate the min and max values of 'cid' for each 'mid' field
        > read_id_range('data.csv', 'mid', 'cid')
        {'A': (1, 5), 'B': (2, 8)}
    """
    if not os.path.exists(fp):
        return Dict()

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
    return Dict(result)
