from .files import write


def writer(queue):
    """
    Listens to `queue` for file writing tasks. Expects a tuple:

    - For CSV:
        (fp, data, headers, [optional scrape_time])
    - For JSON/JSONL:
        (fp, data)

    Use 'STOP' to end the loop.
    """
    while True:
        try:
            inp = queue.get()
            if inp == 'STOP':
                break
            if len(inp) < 2:
                print(f'[writer] Invalid input: {inp}')
                continue

            fp, data, *args = inp
            write(fp, data, *args)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f'Error in writer: {e}')
