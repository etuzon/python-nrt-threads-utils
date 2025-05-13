from time import sleep

from nrt_threads_utils.threads_pool_manager.tasks import MethodTask
from nrt_threads_utils.threads_pool_manager.threads_pool_manager import ThreadsPoolManager


def sleep_10_sec():
    sleep(10)
    return 'ABC'


threads_pool_manager = ThreadsPoolManager()

try:
    threads_pool_manager.start()

    mt = MethodTask(sleep_10_sec)

    threads_pool_manager.add_task(mt)

    sleep(11)

    result = mt.result

    print(f'Result: {result}')
finally:
    threads_pool_manager.shutdown()
    threads_pool_manager.join()