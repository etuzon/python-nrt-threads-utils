# Threads Utilities

### Threads utilities in Python.

![PyPI](https://img.shields.io/pypi/v/nrt-threads-utils?color=blueviolet&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nrt-threads-utils?color=greens&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/nrt-threads-utils?color=blue&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dd/nrt-threads-utils?style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nrt-threads-utils?color=yellow&style=plastic)
[![Coverage Status](https://coveralls.io/repos/github/etuzon/python-nrt-threads-utils/badge.svg)](https://coveralls.io/github/etuzon/pytohn-nrt-threads-utils)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/etuzon/python-nrt-threads-utils?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/etuzon/python-nrt-threads-utils?style=plastic)
[![DeepSource](https://app.deepsource.com/gh/etuzon/python-nrt-threads-utils.svg/?label=active+issues&show_trend=false&token=O1IXaeoboX7tPARnOfzNNvBp)](https://app.deepsource.com/gh/etuzon/python-nrt-threads-utils/)

## Threads pool manager

### Description

Threads pool manager is a threads pool manager that manages a pool of task executors that execute tasks.

### Queue Placement Algorithms

| **Algorithm**               | **Description**                                                                                                                                                                                                                                                                                                                                                                                                   |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `STRICT_PRIORITY`           | Higher priority tasks are added to the queue before lower priority tasks.                                                                                                                                                                                                                                                                                                                                         |
| `AVOID_STARVATION_PRIORITY` | Tasks are added to the queue in `STRICT_PRIORITY`,<br>and if tasks are not added to the last place in the queue in `avoid_starvation_amount` times,<br>the next task is added to the last place in the queue and will be flagged with `avoid_starvation` flag.<br>Other tasks will be added to the queue in `AVOID_STARVATION_PRIORITY` order after that flagged task, so this task will be executed before them. |

### Executors extension pool

The threads pool manager has an executors extension pool that extends the pool of task executors<br>
when the pool is full and at least one task executor run more than `executors_timeout_ms`.


## ThreadsPoolManager class

### Methods

| **Method**                          | **Description**                                                                   | **Parameters**                                                                                                                                                                                                                                                                            | **Returns**                                                                             |
|-------------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `add_task`                          | Adds a task to the threads pool.                                                  | `task (ThreadTask \| MethodTask)` The task to add to the threads pool.<br>`task_id (Optional[str], Default: None)` Task identifier.<br>`priority (int, Default: 1)` Task Priority. Higher number is higher priority.<br>`queue_placement (QueuePlacementEnum)` Queue placement algorithm. | `None`                                                                                  |
| `get_task`                          | Gets a task from the threads pool.                                                | `task_id (str)` Task identifier.                                                                                                                                                                                                                                                          | `ThreadTask \| MethodTask \| None` Return task if task is found, otherwise return None. |
| `is_task_exists`                    | Checks if task exists in the threads pool.                                        | `task_id (str)` Task identifier.                                                                                                                                                                                                                                                          | `bool` True if task exists, otherwise False.                                            |
| `reset_metrics`                     | Resets Metrics.                                                                   | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |
| `start`                             | Starts the threads pool.                                                          | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |
| `shutdown`                          | Shuts down the threads pool.                                                      | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |
| `active_tasks_amount`               | Returns the amount of active tasks in the threads pool.                           | `@propery`                                                                                                                                                                                                                                                                                | `int` Active tasks amount.                                                              |
| `avoid_starvation_amount`           | Returns Avoid Starvation Amount                                                   | `@propery`                                                                                                                                                                                                                                                                                | `int` Avoid Starvation Amount.                                                          |
| `executors_extension_pool_size`     | Returns Executors Extension Pool Size.                                            | `@propery`                                                                                                                                                                                                                                                                                | `int` Executors Extension Pool Size.                                                    |
| `executors_timeout_ms`              | Returns Executors Timeout in milliseconds.                                        | `@propery`                                                                                                                                                                                                                                                                                | `int` Executors Timeout in milliseconds.                                                |
| `executors_timeout_ms`              | Sets Executors Timeout in milliseconds.                                           | `@setter` Executors Timeout in milliseconds.                                                                                                                                                                                                                                              | `None`                                                                                  |
| `finished_tasks`                    | Returns finished tasks.<br>Finished tasks list will be truncated after each call. | `@propery`                                                                                                                                                                                                                                                                                | `List[ThreadTask \| MethodTask]` Finished tasks.                                        |
| `is_all_executed`                   | Returns True if all tasks are executed.                                           | `@propery`                                                                                                                                                                                                                                                                                | `bool` True if all tasks are executed, otherwise False.                                 | 
| `is_executors_shutdown`             | Returns True if executors pool is shutdown.                                       | `@propery`                                                                                                                                                                                                                                                                                | `bool`                                                                                  |
| `max_executors_extension_pool_size` | Returns Max Executors Extension Pool Size.                                        | `@propery`                                                                                                                                                                                                                                                                                | `int` Max Executors Extension Pool Size.                                                |
| `max_executors_extension_pool_size` | Sets Max Executors Extension Pool Size.                                           | `@setter` Max Executors Extension Pool Size.                                                                                                                                                                                                                                              | `None`                                                                                  |
| `max_executors_pool_size`           | Returns Max Executors Pool Size.                                                  | `@propery`                                                                                                                                                                                                                                                                                | `int` Max Executors Pool Size.                                                          |
| `max_executors_pool_size`           | Sets Max Executors Pool Size.                                                     | `@setter` Max Executors Pool Size.                                                                                                                                                                                                                                                        | `None`                                                                                  |
| `max_queue_size`                    | Returns Queue Size limitation.                                                    | `@propery`                                                                                                                                                                                                                                                                                | `int` Max Queue Size.                                                                   |
| `max_queue_size`                    | Sets Max Queue Size.                                                              | `@setter` Max Queue Size.                                                                                                                                                                                                                                                                 | `None`                                                                                  |
| `metrics`                           | Returns Metrics.                                                                  | `@propery`                                                                                                                                                                                                                                                                                | `ThreadsPoolManagerMetrics` Metrics.                                                    |
| `name`                              | Returns Threads Pool Name.                                                        | `@propery`                                                                                                                                                                                                                                                                                | `str` Threads Pool Name.                                                                |
| `name`                              | Sets Threads Pool Name.                                                           | `@setter` Threads Pool Name.                                                                                                                                                                                                                                                              | `None`                                                                                  |
| `queue`                             | Returns Queue.                                                                    | `@propery`                                                                                                                                                                                                                                                                                | `Queue` Queue.                                                                          |
| `queue_size`                        | Returns Queue Size.                                                               | `@propery`                                                                                                                                                                                                                                                                                | `int` Queue Size.                                                                       |
| `shutdown`                          | Shuts down the threads pool.                                                      | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |
| `shutdown_executors`                | Shuts down executors pool.                                                        | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |
| `start_executors`                   | Starts executors pool.                                                            | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |

## TaskExecutor class

### Methods

| **Method**              | **Description**                                                                       | **Parameters** | **Returns**                  |
|-------------------------|---------------------------------------------------------------------------------------|----------------|------------------------------|
| `start`                 | Starts the task executor.                                                             | `None`         | `None`                       |
| `avoid_starvation_flag` | Returns Avoid Starvation Flag.                                                        | `@propery`     | `bool`                       |
| `avoid_starvation_flag` | Sets Avoid Starvation Flag.                                                           | `@setter`      | `None`                       |
| `exception`             | Returns Exception, if it happened in method that was executed in MethodTask.          | `@propery`     | `Exception`                  |
| `stack_trace`           | Returns stack trace, if exception happened in method that was executed in MethodTask. | `@propery`     | `str` Exception stack trace. |
| `priority`              | Returns priority.                                                                     | `@propery`     | `int`                        |
| `task`                  | Returns task.                                                                         | `@propery`     | `ThreadTask \| MethodTask`   |
| `task_id`               | Returns task id.                                                                      | `@propery`     | `str`                        |

## ThreadTask class

Task that runs a thread.

### Methods

| **Method**      | **Description**             | **Parameters** | **Returns**                    |
|-----------------|-----------------------------|----------------|--------------------------------|
| `execute`       | Executes the task.          | `None`         | `None`                         |
| `task_instance` | Returns task instance.      | `@propery`     | `Thread` Task Thread instance. |
| `alive_date_ms` | Returns task alive date ms. | `@propery`     | `int` Alive date in ms.        |
| `start_date_ms` | Returns task start date ms. | `@propery`     | `int` Start date in ms.        |
| `start_date_ms` | Sets task start date ms.    | `@setter`      | `None`                         |
| `task_state`    | Returns task state.         | `@propery`     | `TaskStateEnum` Task state.    |
| `task_state`    | Sets task state.            | `@setter`      | `None`                         |

## MethodTask class

Task that runs a method.

### Methods

| **Method**      | **Description**                             | **Parameters** | **Returns**                  |
|-----------------|---------------------------------------------|----------------|------------------------------|
| `execute`       | Executes the task.                          | `None`         | `None`                       |
| `alive_date_ms` | Returns task alive date ms.                 | `@propery`     | `int` Alive date in ms.      |
| `exception`     | Returns Exception, if it happened.          | `@propery`     | `Exception`                  |
| `result`        | Returns task result.                        | `@propery`     | `Any` Task result.           |
| `stack_trace`   | Returns stack trace, if exception happened. | `@propery`     | `str` Exception stack trace. |
| `start_date_ms` | Returns task start date ms.                 | `@propery`     | `int` Start date in ms.      |
| `start_date_ms` | Sets task start date ms.                    | `@setter`      | `None`                       |
| `task_state`    | Returns task state.                         | `@propery`     | `TaskStateEnum` Task state.  |
| `task_state`    | Sets task state.                            | `@setter`      | `None`                       |


## ThreadsPoolManagerMetrics class

dataclass that holds threads pool manager metrics.

### Properties

| **Property**                  | **Description**                                                                                      | **Type**         |
|-------------------------------|------------------------------------------------------------------------------------------------------|------------------|
| `avoid_starvation_counter`    | Count the times that `AVOID_STARVATION_PRORITY` flag has been raised.                                | `int`            |
| `executed_method_counter`     | Count the times that `MethodTask` has been executed.                                                 | `int`            |
| `executed_task_counter`       | Count the times that `ThreadTask\|MethodTask` has been executed.                                     | `int`            |
| `executed_thread_counter`     | Count the times that `ThreadTask` has been executed.                                                 | `int`            |
| `max_execution_date_ms`       | Max execution date in ms.                                                                            | `int`            |
| `max_queue_size`              | Max size that the queue has reached.                                                                 | `int`            |
| `method_tasks_counter_dict`   | Count the times that `MethodTask` has been executed by task id.<br>key is task priority.             | `dict[int, int]` |
| `tasks_priority_counter_dict` | Count the times that `ThreadTask\|MethodTask` has been executed by task id.<br>key is task priority. | `dict[int, int]` |
| `thread_tasks_counter_dict`   | Count the times that `ThreadTask` has been executed by task id.<br>key is task priority.             | `dict[int, int]` |


## TaskStateEnum Enum

Task state enum.

| **Enum**         | **Description**            |
|------------------|----------------------------|
| `QUEUE`          | Task is in queue.          |
| `EXECUTORS_POOL` | Task is in executors pool. |
| `EXECUTED`       | Task is finished.          |

## QueuePlacementEnum Enum

Queue placement enum.

| **Enum**                    | **Description**            |
|-----------------------------|----------------------------|
| `STRICT_PRIORITY`           | Strict Priority.           |
| `AVOID_STARVATION_PRIORITY` | Avoid Starvation Priority. |

## Examples:

- ### Add tasks with `STRICT_PRIORITY` queue placement.

    Create a threads pool manager with 2 executors pool size.
    
    ```python
    from nrt_threads_utils.threads_pool_manager.threads_pool_manager import ThreadsPoolManager
    
    threads_pool_manager = ThreadsPoolManager(executors_pool_size=2)
    threads_pool_manager.start()
    ```
    ![init-threads-pool-manager-2-executors.png.png](information/pictures/init-threads-pool-manager-2-executors.png)
    
    Add two tasks to the threads pool manager.<br>
    The tasks will be executed as the two executors are empty.
    
    ```python
    from nrt_threads_utils.threads_pool_manager.tasks import ThreadTask
    
    t_1 = CustomThread()
    t_2 = CustomThread()
    
    threads_pool_manager.add_task(ThreadTask(t_1), priority=1)
    threads_pool_manager.add_task(ThreadTask(t_1), priority=1)
    ```
    
    ![threads-pool-manager-2-threads-2-executors.png](information/pictures/threads-pool-manager-2-threads-2-executors.png)
    
    Add 2 tasks in priority 1.<br>
    Default queue placement is `STRICT_PRIORITY`.
    
    ```python
    t_3 = CustomThread()
    t_4 = CustomThread()
    
    threads_pool_manager.add_task(ThreadTask(t_3), priority=1)
    threads_pool_manager.add_task(ThreadTask(t_4), priority=1)
    ```
    
    ![threads-pool-manager-add-3-and-4-threads-2-executors.png](information/pictures/threads-pool-manager-add-3-and-4-threads-2-executors.png)
    
    Add task in priority 2 (Higher priority)
    Default queue placement is `STRICT_PRIORITY`.
    
    ```python
    t_5 = CustomThread()
    
    threads_pool_manager.add_task(ThreadTask(t_3), priority=2)
    ```
    
    Task in priority 2 is executed before tasks in priority 1.
    
    ![threads-pool-manager-thread-strict-priority-2.png](information/pictures/threads-pool-manager-thread-strict-priority-2.png)

- ### Add tasks with `AVOID_STARVATION_PRIORITY` queue placement.

    Create a threads pool manager with 2 executors pool size.
    `avoid_starvation_amount` is set to 1.
    
    ```python
    from nrt_threads_utils.threads_pool_manager.threads_pool_manager import ThreadsPoolManager
    
    threads_pool_manager = ThreadsPoolManager(executors_pool_size=2)
    threads_pool_manager.avoid_starvation_amount = 1
    threads_pool_manager.start()
    ```
    ![init-threads-pool-manager-2-executors.png](information/pictures/init-threads-pool-manager-2-executors.png)
    
    Add 2 tasks in priority 1.<br>
    
    ```python
    from nrt_threads_utils.threads_pool_manager.tasks import ThreadTask
    from nrt_threads_utils.threads_pool_manager.enums import QueuePlacementEnum
    
    t_1 = CustomThread()
    t_2 = CustomThread()
    
    threads_pool_manager.add_task(
        ThreadTask(t_1),
        priority=1,
        queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
    threads_pool_manager.add_task(
        ThreadTask(t_2),
        priority=1,
        queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
    ```
    ![threads-pool-manager-2-threads-2-executors.png](information/pictures/threads-pool-manager-2-threads-2-executors.png)
    
    Add task in priority 2 (Higher priority)
    
    ```python
    t_5 = CustomThread()
    
    threads_pool_manager.add_task(
        ThreadTask(t_3), 
        priority=2,
        queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
    ```
    
    Task in priority 2 is executed before tasks in priority 1.<br>
    Avoid starvation counter is increased by 1 because the task is not appended to the end of the queue.
    
    ![threads-pool-manager-add-3-and-4-threads-2-executors.png](information/pictures/threads-pool-manager-add-3-and-4-threads-2-executors.png)
    
    Add another task in priority 2 (Higher priority)
    
    ```python
    t_5 = CustomThread()
    
    threads_pool_manager.add_task(
        ThreadTask(t_3), 
        priority=2,
        queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
    ```
    
    The task will flag with `avoid_starvation_flag` and will be added to the end of the queue.

    ![threads-pool-manager-avoid-starvation-flag.png](information/pictures/threads-pool-manager-avoid-starvation-flag.png)
    
    Add the next tasks will be added in **Avoid Starvation Priority** after the flagged task.
    
    ![threads-pool-manager-avoid-starvation-next-tasks.png](information/pictures/threads-pool-manager-avoid-starvation-next-tasks.png)


- ### Metrics.

    Create method that sleep for 10 seconds.<br><br>
    
    **Code**
    
    ```python
    from nrt_threads_utils.threads_pool_manager.threads_pool_manager import ThreadsPoolManager
    from nrt_threads_utils.threads_pool_manager.tasks import MethodTask
    from time import sleep
    
    
    def sleep_10_sec():
        sleep(10)
        return 'a', 'b'
    
    
    threads_pool_manager = \
            ThreadsPoolManager(executors_pool_size=1)
    
        try:
            threads_pool_manager.start()
            
            mt_1 = MethodTask(sleep_10_sec)
            mt_2 = MethodTask(sleep_10_sec)
            mt_3 = MethodTask(sleep_10_sec)
  
            threads_pool_manager.add_task(mt_1, priority=1)
            sleep(0.2)
            threads_pool_manager.add_task(mt_2, priority=2)
            threads_pool_manager.add_task(mt_3, priority=2)
    
            metrics = threads_pool_manager.metrics
            print(f'Max queue size: {metrics.max_queue_size}')
            print(f'Max execution date ms {metrics.max_execution_date_ms}')
            print(f'Executed tasks counter: {metrics.executed_tasks_counter}')
            print(f'Executed threads counter: {metrics.executed_threads_counter}')
            print(f'Executed methods counter: {metrics.executed_methods_counter}')
            print(f'Avoid starvation counter: {metrics.avoid_starvation_counter}')
            print(f'Tasks priority counter dict {metrics.tasks_priority_counter_dict}')
            
            sleep(12)
  
            a, b = mt_1.result
  
            print('Result 1: ' + a)
            print('Result 2: ' + b)
        finally:
            threads_pool_manager.shutdown()
            threads_pool_manager.join()
    ```
    
    **Output**
        
    ```
    Max queue size: 2
    Max execution date ms 10000
    Executed tasks counter: 3
    Executed threads counter: 0
    Executed methods counter: 3
    Avoid starvation counter: 0
    Tasks priority counter dict {1: 1, 2: 2}
    Result 1: a
    Result 2: b
    ```