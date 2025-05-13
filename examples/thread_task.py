from threading import Thread
from time import sleep

from nrt_threads_utils.threads_pool_manager.tasks import ThreadTask
from nrt_threads_utils.threads_pool_manager.threads_pool_manager import ThreadsPoolManager


class SleepSecPriorityThread(Thread):
    __sleep_sec: int

    def __init__(self, sleep_sec: int):
        super().__init__()

        self.__sleep_sec = sleep_sec

    def run(self):
        print('Before sleep')
        sleep(self.__sleep_sec)
        print('After sleep')


threads_pool_manager = ThreadsPoolManager(executors_pool_size=2)

try:
    threads_pool_manager.start()

    t_1 = SleepSecPriorityThread(10)
    t_2 = SleepSecPriorityThread(10)
    t_3 = SleepSecPriorityThread(10)
    t_4 = SleepSecPriorityThread(10)
    t_5 = SleepSecPriorityThread(10)

    threads_pool_manager.add_task(ThreadTask(t_1), task_id='t_1')
    threads_pool_manager.add_task(ThreadTask(t_2), task_id='t_2')
    threads_pool_manager.add_task(ThreadTask(t_3), task_id='t_3')
    threads_pool_manager.add_task(ThreadTask(t_4), task_id='t_4')
    threads_pool_manager.add_task(ThreadTask(t_5), task_id='t_5')

    while not threads_pool_manager.is_all_executed:
        sleep(1)
finally:
    threads_pool_manager.shutdown()
    threads_pool_manager.join()
