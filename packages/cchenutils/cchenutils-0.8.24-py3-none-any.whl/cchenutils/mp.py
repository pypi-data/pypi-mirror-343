import random
import traceback

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
        except Exception:
            print(traceback.print_exc())


def scraper(func, *func_args, proxy_list=None, **kwargs):
    retries = kwargs.get('retries', 3)
    if proxy_list is None:
        retries = min([1, retries])
    for _ in range(retries):
        try:
            proxy = random.choice(proxy_list) if proxy_list else None
            return func(*func_args, **kwargs, proxy=proxy)
        except Exception:
            print(*func_args)
            print(traceback.print_exc())
    return None
