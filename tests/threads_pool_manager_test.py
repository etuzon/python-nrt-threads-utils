from threading import Thread

import pytest
from time import sleep

from nrt_threads_utils.threads_pool_manager import ThreadsPoolManager, ThreadTask, \
    MethodTask, QueuePlacementEnum, TaskStateEnum, FullQueueException
from nrt_time_utils.time_utils import TimeUtil, MINUTE_MS, SECOND_MS

SLEEP_10 = 10


def sleep_x_and_y_sec(x: int, y: int):
    sleep(x)
    sleep(y)


def sleep_10_sec():
    sleep(SLEEP_10)


def sleep_11_sec():
    sleep(11)


class SleepSecPriorityThreadBase(Thread):
    __sleep_sec: int
    __priority: int

    def __init__(self, sleep_sec: int, priority: int):
        super().__init__()

        self.__sleep_sec = sleep_sec
        self.__priority = priority

    def run(self):
        sleep(self.__sleep_sec)

    @property
    def priority(self):
        return self.__priority


class Sleep30SecPriority1Thread(SleepSecPriorityThreadBase):

    def __init__(self):
        super().__init__(3 * SLEEP_10, 1)


class Sleep10SecPriority1Thread(SleepSecPriorityThreadBase):

    def __init__(self):
        super().__init__(SLEEP_10, 1)


class Sleep10SecPriority2Thread(SleepSecPriorityThreadBase):

    def __init__(self):
        super().__init__(SLEEP_10, 2)


class Sleep10SecPriority3Thread(SleepSecPriorityThreadBase):

    def __init__(self):
        super().__init__(SLEEP_10, 3)


def test_name():
    threads_pool_manager = ThreadsPoolManager()

    assert threads_pool_manager.name is None

    threads_pool_manager.name = 'test'
    assert threads_pool_manager.name == 'test'


def test_threads_and_pool_size_is_1():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=1)

    try:
        threads_pool_manager.start()

        t_1 = Sleep10SecPriority1Thread()
        t_2 = Sleep10SecPriority1Thread()

        threads_pool_manager.add_task(ThreadTask(t_1))
        threads_pool_manager.add_task(ThreadTask(t_2))

        __verify_pool_size_is_1(threads_pool_manager)

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_threads_and_pool_size_is_2():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=2)

    try:
        threads_pool_manager.start()

        t_1 = Sleep10SecPriority1Thread()
        t_2 = Sleep10SecPriority1Thread()
        t_3 = Sleep10SecPriority1Thread()

        threads_pool_manager.add_task(ThreadTask(t_1))
        threads_pool_manager.add_task(ThreadTask(t_2))
        threads_pool_manager.add_task(ThreadTask(t_3))

        __verify_pool_size_is_2(threads_pool_manager)

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_method_without_args_and_pool_size_is_1():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=1)

    try:
        threads_pool_manager.start()

        threads_pool_manager.add_task(MethodTask(sleep_10_sec))
        threads_pool_manager.add_task(MethodTask(sleep_10_sec))

        __verify_pool_size_is_1(threads_pool_manager)

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_method_without_args_and_pool_size_is_2():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=2)

    try:
        threads_pool_manager.start()

        threads_pool_manager.add_task(MethodTask(sleep_10_sec))
        threads_pool_manager.add_task(MethodTask(sleep_10_sec))
        threads_pool_manager.add_task(MethodTask(sleep_10_sec))

        __verify_pool_size_is_2(threads_pool_manager)

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_method_with_args_and_pool_size_is_1():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=1)

    try:
        threads_pool_manager.start()

        threads_pool_manager.add_task(MethodTask(sleep_x_and_y_sec, 6, 4))
        threads_pool_manager.add_task(MethodTask(sleep_x_and_y_sec, x=7, y=3))

        __verify_pool_size_is_1(threads_pool_manager)

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_strict_priority():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=1)

    try:
        threads_pool_manager.start()

        t_1 = Sleep10SecPriority1Thread()
        t_2 = Sleep10SecPriority2Thread()

        threads_pool_manager.add_task(ThreadTask(t_1), priority=1)
        threads_pool_manager.add_task(ThreadTask(t_2), priority=2)

        sleep(5)

        assert threads_pool_manager.queue_size == 1, \
            f'Queue size: {threads_pool_manager.queue_size}'

        queue = threads_pool_manager.queue

        assert len(queue) == 1, f'Queue: {queue}'
        assert queue[0].task.task_instance.priority == 1

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_avoid_starvation_priority():
    """
    Tasks order:

    Queue start:
        t_6 (priority 2),
        t_7 (priority 3),
        t_5 (priority 2), - Get avoid starvation flag
        t_2 (priority 1) ,
        t_1 (priority 1),
        t_4 (priority 2),
        t_3 (priority 2) - In executor pool

    :return:
    """

    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=1)

    threads_pool_manager.avoid_starvation_amount = 2

    assert threads_pool_manager.avoid_starvation_amount == 2

    try:
        threads_pool_manager.start()

        t_1 = Sleep10SecPriority1Thread()
        t_2 = Sleep10SecPriority1Thread()
        t_3 = Sleep10SecPriority2Thread()
        t_4 = Sleep10SecPriority2Thread()
        t_5 = Sleep10SecPriority2Thread()
        t_6 = Sleep10SecPriority2Thread()
        t_7 = Sleep10SecPriority3Thread()

        threads_pool_manager.add_task(
            ThreadTask(t_1),
            task_id='t_1',
            priority=1,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
        threads_pool_manager.add_task(
            ThreadTask(t_2),
            task_id='t_2',
            priority=1,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
        threads_pool_manager.add_task(
            ThreadTask(t_3),
            task_id='t_3',
            priority=2,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
        threads_pool_manager.add_task(
            ThreadTask(t_4),
            task_id='t_4',
            priority=2,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
        threads_pool_manager.add_task(
            ThreadTask(t_5),
            task_id='t_5',
            priority=2,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
        threads_pool_manager.add_task(
            ThreadTask(t_6),
            task_id='t_6',
            priority=2,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
        threads_pool_manager.add_task(
            ThreadTask(t_7),
            task_id='t_7',
            priority=3,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)

        sleep(5)

        assert threads_pool_manager.queue_size == 6, \
            f'Queue size: {threads_pool_manager.queue_size}'

        queue = threads_pool_manager.queue

        assert len(queue) == 6, f'Queue: {queue}'
        assert queue[-1].task_id == 't_6', __get_queue_order(queue)
        assert queue[-2].task_id == 't_7', __get_queue_order(queue)
        assert queue[-3].task_id == 't_5', __get_queue_order(queue)
        assert queue[-4].task_id == 't_2', __get_queue_order(queue)
        assert queue[-5].task_id == 't_1', __get_queue_order(queue)
        assert queue[-6].task_id == 't_4', __get_queue_order(queue)

        start_date_ms = TimeUtil.get_current_date_ms()

        while threads_pool_manager.queue_size > 1 \
                and not TimeUtil.is_timeout_ms(start_date_ms, 2 * MINUTE_MS):
            sleep(1)

        assert threads_pool_manager.queue_size == 1

        t_8 = Sleep10SecPriority3Thread()

        threads_pool_manager.add_task(
            ThreadTask(t_8),
            task_id='t_8',
            priority=3,
            queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)

        queue = threads_pool_manager.queue

        assert queue[0].task_id == 't_8'

        while threads_pool_manager.queue_size > 0 \
                and not TimeUtil.is_timeout_ms(start_date_ms, 2 * MINUTE_MS):
            sleep(1)

        assert threads_pool_manager.queue_size == 0

        sleep(2 * SLEEP_10)

        assert threads_pool_manager.active_tasks_amount == 0

        assert threads_pool_manager.get_task('t_1') is None

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_task_base_properties():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=1)

    try:
        threads_pool_manager.start()

        t_1 = Sleep10SecPriority1Thread()
        t_2 = Sleep10SecPriority1Thread()

        threads_pool_manager.add_task(ThreadTask(t_1), task_id='t_1')
        threads_pool_manager.add_task(ThreadTask(t_2), task_id='t_2')

        sleep(5)

        t_1 = threads_pool_manager.get_task('t_1')
        t_2 = threads_pool_manager.get_task('t_2')

        assert t_1.start_date_ms > 0
        assert t_2.start_date_ms == 0

        assert t_1.alive_date_ms > 0
        assert t_2.alive_date_ms == 0

        assert t_1.task_state == TaskStateEnum.EXECUTORS_POOL
        assert t_2.task_state == TaskStateEnum.QUEUE

        sleep(SLEEP_10)

        assert t_2.start_date_ms > 0
        assert t_2.alive_date_ms > 0

        assert t_1.task_state == TaskStateEnum.EXECUTED
        assert t_2.task_state == TaskStateEnum.EXECUTORS_POOL

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_max_queue_size():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=1)

    try:
        threads_pool_manager.start()

        threads_pool_manager.max_queue_size = 1

        t_1 = Sleep10SecPriority1Thread()
        t_2 = Sleep10SecPriority1Thread()
        t_3 = Sleep10SecPriority1Thread()

        threads_pool_manager.add_task(ThreadTask(t_1), task_id='t_1')

        sleep(2)

        threads_pool_manager.add_task(ThreadTask(t_2), task_id='t_2')

        with pytest.raises(FullQueueException):
            threads_pool_manager.add_task(ThreadTask(t_3), task_id='t_3')

        sleep(5)

        assert threads_pool_manager.queue_size == 1, \
            f'Queue size: {threads_pool_manager.queue_size}'

        queue = threads_pool_manager.queue

        assert len(queue) == 1, f'Queue: {queue}'
        assert queue[0].task_id == 't_2'

        sleep(SLEEP_10)

        assert threads_pool_manager.queue_size == 0

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def test_executors_extension():
    threads_pool_manager = \
        ThreadsPoolManager(executors_pool_size=2)

    threads_pool_manager.max_executors_extension_pool_size = 2
    threads_pool_manager.executors_timeout_ms = 10 * SECOND_MS

    try:
        threads_pool_manager.start()

        t_1 = Sleep30SecPriority1Thread()
        t_2 = Sleep30SecPriority1Thread()
        t_3 = Sleep10SecPriority1Thread()
        t_4 = Sleep10SecPriority1Thread()
        t_5 = Sleep10SecPriority1Thread()

        threads_pool_manager.add_task(ThreadTask(t_1), task_id='t_1')
        threads_pool_manager.add_task(ThreadTask(t_2), task_id='t_2')
        threads_pool_manager.add_task(ThreadTask(t_3), task_id='t_3')
        threads_pool_manager.add_task(ThreadTask(t_4), task_id='t_4')
        threads_pool_manager.add_task(ThreadTask(t_5), task_id='t_5')

        sleep(5)

        assert threads_pool_manager.queue_size == 3, \
            f'Queue size: {threads_pool_manager.queue_size}'

        assert threads_pool_manager.max_executors_pool_size == 2
        assert threads_pool_manager.executors_extension_pool_size == 0
        assert threads_pool_manager.active_tasks_amount == 2

        sleep_10_sec()

        assert threads_pool_manager.queue_size == 1, \
            f'Queue size: {threads_pool_manager.queue_size}'

        assert threads_pool_manager.max_executors_pool_size == 2
        assert threads_pool_manager.executors_extension_pool_size == 2
        assert threads_pool_manager.active_tasks_amount == 4

        sleep_11_sec()

        assert threads_pool_manager.queue_size == 0, \
            f'Queue size: {threads_pool_manager.queue_size}'

        assert threads_pool_manager.max_executors_pool_size == 2
        assert threads_pool_manager.executors_extension_pool_size == 1
        assert threads_pool_manager.active_tasks_amount == 3

        sleep_11_sec()

        assert threads_pool_manager.queue_size == 0, \
            f'Queue size: {threads_pool_manager.queue_size}'

        assert threads_pool_manager.executors_extension_pool_size == 0
        assert threads_pool_manager.active_tasks_amount == 0

    finally:
        threads_pool_manager.shutdown()
        threads_pool_manager.join()


def __verify_pool_size_is_1(threads_pool_manager: ThreadsPoolManager):

    threads_pool_manager.max_executors_pool_size = 1

    sleep(5)

    assert threads_pool_manager.queue_size == 1, \
           f'Queue size: {threads_pool_manager.queue_size}'
    assert threads_pool_manager.max_executors_pool_size == 1, \
           f'Executors pool size: {threads_pool_manager.max_executors_pool_size}'
    assert threads_pool_manager.active_tasks_amount == 1, \
           f'Active tasks amount: {threads_pool_manager.active_tasks_amount}'
    sleep(SLEEP_10)

    assert threads_pool_manager.queue_size == 0, \
           f'Queue size: {threads_pool_manager.queue_size}'
    assert threads_pool_manager.max_executors_pool_size == 1, \
           f'Executors pool size: {threads_pool_manager.max_executors_pool_size}'
    assert threads_pool_manager.active_tasks_amount == 1, \
           f'Active tasks amount: {threads_pool_manager.active_tasks_amount}'

    sleep(SLEEP_10)

    assert threads_pool_manager.queue_size == 0, \
           f'Queue size: {threads_pool_manager.queue_size}'
    assert threads_pool_manager.max_executors_pool_size == 1, \
           f'Executors pool size: {threads_pool_manager.max_executors_pool_size}'
    assert threads_pool_manager.active_tasks_amount == 0, \
           f'Active tasks amount: {threads_pool_manager.active_tasks_amount}'


def __verify_pool_size_is_2(threads_pool_manager: ThreadsPoolManager):

    threads_pool_manager.max_executors_pool_size = 2

    sleep(5)

    assert threads_pool_manager.queue_size == 1, \
           f'Queue size: {threads_pool_manager.queue_size}'
    assert threads_pool_manager.max_executors_pool_size == 2, \
           f'Executors pool size: {threads_pool_manager.max_executors_pool_size}'
    assert threads_pool_manager.active_tasks_amount == 2, \
           f'Active tasks amount: {threads_pool_manager.active_tasks_amount}'

    sleep(SLEEP_10)

    assert threads_pool_manager.queue_size == 0, \
           f'Queue size: {threads_pool_manager.queue_size}'
    assert threads_pool_manager.max_executors_pool_size == 2, \
           f'Executors pool size: {threads_pool_manager.max_executors_pool_size}'
    assert threads_pool_manager.active_tasks_amount == 1, \
           f'Active tasks amount: {threads_pool_manager.active_tasks_amount}'

    sleep(SLEEP_10)

    assert threads_pool_manager.queue_size == 0, \
           f'Queue size: {threads_pool_manager.queue_size}'
    assert threads_pool_manager.max_executors_pool_size == 2, \
           f'Executors pool size: {threads_pool_manager.max_executors_pool_size}'
    assert threads_pool_manager.active_tasks_amount == 0, \
           f'Active tasks amount: {threads_pool_manager.active_tasks_amount}'


def __get_queue_order(queue: list):
    order_str = ', '.join([task_executor.task_id for task_executor in queue])
    return f'Queue order: {order_str}'
