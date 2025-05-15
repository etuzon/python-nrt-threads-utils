from threading import Thread
from time import sleep

from nrt_threads_utils.threads_pool_manager.enums import TaskTypeEnum
from nrt_threads_utils.threads_pool_manager.tasks import MethodTask, ThreadTask
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


def sleep_1_sec():
    sleep(1)
    return 'ABC'


threads_pool_manager = ThreadsPoolManager()

try:
    threads_pool_manager.start()

    mt = MethodTask(sleep_1_sec)
    thread_task = ThreadTask(SleepSecPriorityThread(2))
    print('Adding tasks to the pool manager')
    threads_pool_manager.add_task(mt, task_id='mt')
    threads_pool_manager.add_task(thread_task, task_id='thread_task')

    while not threads_pool_manager.is_all_executed:
        sleep(1)

    finished_tasks = threads_pool_manager.finished_tasks

    for te in finished_tasks:
        print(f'Task ID: {te.task_id}')
        print(f'Task Type: {te.task_type}')

        if te.task_type == TaskTypeEnum.METHOD:
            print(f'MethodTask result: {te.task.result}')
        elif te.task_type == TaskTypeEnum.THREAD:
            print(f'ThreadTask state: {te.task.task_state}')
finally:
    threads_pool_manager.shutdown()
    threads_pool_manager.join()
