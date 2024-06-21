from abc import abstractmethod
from enum import Enum
from threading import Lock, Thread
from typing import Optional

from time import sleep
from nrt_collections_utils.list_utils import ListUtil
from nrt_time_utils.time_utils import TimeUtil


class FullQueueException(Exception):
    pass


class QueuePlacementEnum(Enum):
    STRICT_PRIORITY = 1
    AVOID_STARVATION_PRIORITY = 2


class TaskStateEnum(Enum):
    QUEUE = 1
    EXECUTORS_POOL = 2
    EXECUTED = 3


class TaskBase:
    _start_date_ms: int
    _task_state: TaskStateEnum

    def __init__(self):
        self._start_date_ms = 0
        self._task_state = TaskStateEnum.QUEUE

    @property
    def alive_date_ms(self) -> int:
        if self.start_date_ms:
            return TimeUtil.get_current_date_ms() - self.start_date_ms

        return 0

    @property
    def start_date_ms(self) -> int:
        return self._start_date_ms

    @start_date_ms.setter
    def start_date_ms(self, date_ms: int):
        self._start_date_ms = date_ms

    @property
    def task_state(self) -> TaskStateEnum:
        return self._task_state

    @task_state.setter
    def task_state(self, task_state: TaskStateEnum):
        self._task_state = task_state

    @abstractmethod
    def execute(self):
        pass


class ThreadTask(TaskBase):
    __task: Thread

    def __init__(self, task: Thread):
        super().__init__()

        self.__task = task

    def execute(self):
        self.__task.start()
        self.__task.join()

    @property
    def task_instance(self) -> Thread:
        return self.__task


class MethodTask(TaskBase):
    __task: callable
    __args: tuple
    __kwargs: dict

    def __init__(self, task: callable, *args, **kwargs):
        super().__init__()

        self.__task = task
        self.__args = args
        self.__kwargs = kwargs

    def execute(self):
        self.__task(*self.__args, **self.__kwargs)


class TaskExecutor(Thread):
    __task: TaskBase
    __priority: int
    __avoid_starvation_flag: bool = False
    __task_id: Optional[str] = None

    def __init__(
            self,
            task: TaskBase,
            task_id: Optional[str] = None,
            priority: int = 1):

        super().__init__()

        self.__task = task
        self.__task_id = task_id
        self.__priority = priority

    def run(self):
        self.__task.start_date_ms = TimeUtil.get_current_date_ms()
        self.__task.execute()

    @property
    def avoid_starvation_flag(self) -> bool:
        return self.__avoid_starvation_flag

    @avoid_starvation_flag.setter
    def avoid_starvation_flag(self, flag: bool):
        self.__avoid_starvation_flag = flag

    @property
    def priority(self) -> int:
        return self.__priority

    @property
    def task(self) -> TaskBase:
        return self.__task

    @property
    def task_id(self) -> Optional[str]:
        return self.__task_id


class ThreadsPoolManager(Thread):
    AVOID_STARVATION_AMOUNT = 10

    __lock: Lock
    __queue: list
    __max_executors_pool_size: int
    __max_queue_size: int = 0
    __max_executors_extension_pool_size: int = 0
    __name: Optional[str] = None
    __executors_timeout_ms: int = 0

    __executors_extension_pool_size = 0

    __avoid_starvation_amount: int = AVOID_STARVATION_AMOUNT
    __avoid_starvation_counter: int = 0

    __is_shutdown: bool = False

    __executors_pool: list

    def __init__(self, executors_pool_size: int = 1):
        super().__init__()

        self.__lock = Lock()
        self.__queue = []
        self.__max_executors_pool_size = executors_pool_size
        self.__executors_pool = []

    def add_task(
            self,
            task: TaskBase,
            task_id: Optional[str] = None,
            priority: int = 1,
            queue_placement: QueuePlacementEnum = QueuePlacementEnum.STRICT_PRIORITY):

        task_executor = \
            TaskExecutor(
                task=task,
                task_id=task_id,
                priority=priority)

        with self.__lock:
            self.__verify_queue_size()

            if queue_placement == QueuePlacementEnum.STRICT_PRIORITY:
                self.__add_task_strict_queue_placement(task_executor)
            elif queue_placement == QueuePlacementEnum.AVOID_STARVATION_PRIORITY:
                self.__add_task_avoid_starvation_queue_placement(task_executor)
            else:
                raise NotImplementedError('Queue placement not implemented')

    def get_task(self, task_id: str) -> Optional[TaskBase]:
        with self.__lock:
            for task_executor in self.__executors_pool:
                if task_executor.task_id == task_id:
                    return task_executor.task

            for task_executor in self.__queue:
                if task_executor.task_id == task_id:
                    return task_executor.task

        return None

    def run(self):
        while not self.__is_shutdown:
            is_execute = self.__get_next_task_from_queue_to_executors_pool()
            is_remove = self.__remove_dead_tasks_from_executors_pool()

            if not is_execute and not is_remove:
                sleep(.05)

    def shutdown(self):
        self.__is_shutdown = True

    @property
    def active_tasks_amount(self) -> int:
        return len(self.__executors_pool)

    @property
    def avoid_starvation_amount(self) -> int:
        return self.__avoid_starvation_amount

    @property
    def avoid_starvation_task_index(self):
        for i, te in enumerate(reversed(self.__queue)):
            if te.avoid_starvation_flag:
                return len(self.__queue) - 1 - i

        return -1

    @avoid_starvation_amount.setter
    def avoid_starvation_amount(self, amount: int):
        self.__avoid_starvation_amount = amount

    @property
    def executors_extension_pool_size(self) -> int:
        return self.__executors_extension_pool_size

    @property
    def executors_timeout_ms(self) -> int:
        return self.__executors_timeout_ms

    @executors_timeout_ms.setter
    def executors_timeout_ms(self, timeout_ms: int):
        self.__executors_timeout_ms = timeout_ms

    @property
    def max_executors_extension_pool_size(self) -> int:
        return self.__max_executors_extension_pool_size

    @max_executors_extension_pool_size.setter
    def max_executors_extension_pool_size(self, size: int):
        self.__max_executors_extension_pool_size = size

    @property
    def max_executors_pool_size(self) -> int:
        return self.__max_executors_pool_size

    @max_executors_pool_size.setter
    def max_executors_pool_size(self, size: int):
        self.__max_executors_pool_size = size

    @property
    def max_queue_size(self) -> int:
        return self.__max_queue_size

    @max_queue_size.setter
    def max_queue_size(self, size: int):
        self.__max_queue_size = size

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def queue(self) -> list:
        with self.__lock:
            return self.__queue.copy()

    @property
    def queue_size(self) -> int:
        with self.__lock:
            return len(self.__queue)

    def __verify_queue_size(self):
        if self.__max_queue_size > 0:
            if len(self.__queue) >= self.__max_queue_size:
                raise FullQueueException(f'Queue size: {len(self.__queue)}')

    def __get_next_task_from_queue_to_executors_pool(self) -> bool:
        if len(self.__executors_pool) < self.max_executors_pool_size \
                or self.__increase_executors_extension_pool_size():

            task_executor = self.__get_next_task_executor()

            if task_executor is not None:
                task_executor.task.task_state = TaskStateEnum.EXECUTORS_POOL
                task_executor.start()
                self.__executors_pool.append(task_executor)
                return True

        return False

    def __increase_executors_extension_pool_size(self):
        if self.executors_extension_pool_size < self.max_executors_extension_pool_size \
                and len(self.__executors_pool) >= self.max_executors_pool_size \
                and self.__is_executor_timeout() and self.queue_size:

            self.__executors_extension_pool_size += 1
            return True

        return False

    def __is_executor_timeout(self):
        for task_executor in self.__executors_pool:
            if task_executor.task.alive_date_ms > self.executors_timeout_ms:
                return True

        return False

    def __remove_dead_tasks_from_executors_pool(self):
        is_removed = False

        for i in range(len(self.__executors_pool)):
            if not self.__executors_pool[i].is_alive():
                self.__executors_pool[i].task.task_state = TaskStateEnum.EXECUTED
                self.__executors_pool[i] = None

                if self.__executors_extension_pool_size > 0:
                    self.__executors_extension_pool_size -= 1

                is_removed = True

        self.__executors_pool = ListUtil.remove_none(self.__executors_pool)

        return is_removed

    def __get_next_task_executor(self):
        with self.__lock:
            if len(self.__queue) > 0:
                task_executor = self.__queue.pop(0)
                return task_executor

        return None

    def __add_task_strict_queue_placement(
            self, task: TaskExecutor, start_index: int = 0) -> int:

        for i, te in enumerate(self.__queue[start_index:], start=start_index):
            if te.priority < task.priority:
                self.__queue.insert(i, task)
                return i

        self.__queue.append(task)

        return -1

    def __add_task_avoid_starvation_queue_placement(self, task_executor: TaskExecutor):
        if self.__avoid_starvation_counter >= self.__avoid_starvation_amount:
            self.__add_task_avoid_starvation_counter_equal_to_amount(task_executor)
        else:
            self.__add_task_avoid_starvation_counter_gt_than_amount(task_executor)

    def __add_task_avoid_starvation_counter_gt_than_amount(
            self, task_executor: TaskExecutor):

        avoid_starvation_task_index = self.avoid_starvation_task_index

        if avoid_starvation_task_index >= 0:
            index = \
                self.__add_task_strict_queue_placement(
                    task_executor, avoid_starvation_task_index + 1)
        else:
            index = self.__add_task_strict_queue_placement(task_executor)

        if index != -1:
            self.__avoid_starvation_counter += 1

    def __add_task_avoid_starvation_counter_equal_to_amount(
            self, task_executor: TaskExecutor):

        task_executor.avoid_starvation_flag = True
        self.__avoid_starvation_counter = 0
        self.__queue.append(task_executor)
