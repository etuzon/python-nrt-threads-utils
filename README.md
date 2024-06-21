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

| **Method**                          | **Description**                                         | **Parameters**                                                                                                                                                                                                                                                                            | **Returns**                                                                             |
|-------------------------------------|---------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `add_task`                          | Adds a task to the threads pool.                        | `task (ThreadTask \| MethodTask)` The task to add to the threads pool.<br>`task_id (Optional[str], Default: None)` Task identifier.<br>`priority (int, Default: 1)` Task Priority. Higher number is higher priority.<br>`queue_placement (QueuePlacementEnum)` Queue placement algorithm. | `None`                                                                                  |
| `get_task`                          | Gets a task from the threads pool.                      | `task_id (str)` Task identifier.                                                                                                                                                                                                                                                          | `ThreadTask \| MethodTask \| None` Return task if task is found, otherwise return None  |
| `start`                             | Starts the threads pool.                                | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |
| `shutdown`                          | Shuts down the threads pool.                            | `None`                                                                                                                                                                                                                                                                                    | `None`                                                                                  |
| `active_tasks_amount`               | Returns the amount of active tasks in the threads pool. | `@propery`                                                                                                                                                                                                                                                                                | `int` Active tasks amount.                                                              |
| `avoid_starvation_amount`           | Returns Avoid Starvation Amount                         | `@propery`                                                                                                                                                                                                                                                                                | `int` Avoid Starvation Amount.                                                          |
| `executors_extension_pool_size`     | Returns Executors Extension Pool Size.                  | `@propery`                                                                                                                                                                                                                                                                                | `int` Executors Extension Pool Size.                                                    |
| `executors_timeout_ms`              | Returns Executors Timeout in milliseconds.              | `@propery`                                                                                                                                                                                                                                                                                | `int` Executors Timeout in milliseconds.                                                |
| `executors_timeout_ms`              | Sets Executors Timeout in milliseconds.                 | `@setter` Executors Timeout in milliseconds.                                                                                                                                                                                                                                              | `None`                                                                                  |
| `max_executors_extension_pool_size` | Returns Max Executors Extension Pool Size.              | `@propery`                                                                                                                                                                                                                                                                                | `int` Max Executors Extension Pool Size.                                                |
| `max_executors_extension_pool_size` | Sets Max Executors Extension Pool Size.                 | `@setter` Max Executors Extension Pool Size.                                                                                                                                                                                                                                              | `None`                                                                                  |
| `max_executors_pool_size`           | Returns Max Executors Pool Size.                        | `@propery`                                                                                                                                                                                                                                                                                | `int` Max Executors Pool Size.                                                          |
| `max_executors_pool_size`           | Sets Max Executors Pool Size.                           | `@setter` Max Executors Pool Size.                                                                                                                                                                                                                                                        | `None`                                                                                  |
| `max_queue_size`                    | Returns Max Queue Size.                                 | `@propery`                                                                                                                                                                                                                                                                                | `int` Max Queue Size.                                                                   |
| `max_queue_size`                    | Sets Max Queue Size.                                    | `@setter` Max Queue Size.                                                                                                                                                                                                                                                                 | `None`                                                                                  |
| `name`                              | Returns Threads Pool Name.                              | `@propery`                                                                                                                                                                                                                                                                                | `str` Threads Pool Name.                                                                |
| `name`                              | Sets Threads Pool Name.                                 | `@setter` Threads Pool Name.                                                                                                                                                                                                                                                              | `None`                                                                                  |
| `queue`                             | Returns Queue.                                          | `@propery`                                                                                                                                                                                                                                                                                | `Queue` Queue.                                                                          |
| `queue_size`                        | Returns Queue Size.                                     | `@propery`                                                                                                                                                                                                                                                                                | `int` Queue Size.                                                                       |

## TaskExecutor class

### Methods

| **Method**              | **Description**                | **Parameters**  | **Returns**                |
|-------------------------|--------------------------------|-----------------|----------------------------|
| `start`                 | Starts the task executor.      | `None`          | `None`                     |
| `avoid_starvation_flag` | Returns Avoid Starvation Flag. | `@propery`      | `bool`                     |
| `avoid_starvation_flag` | Sets Avoid Starvation Flag.    | `@setter`       | `None`                     |
| `priority`              | Returns priority.              | `@propery`      | `int`                      |
| `task`                  | Returns task.                  | `@propery`      | `ThreadTask \| MethodTask` |
| `task_id`               | Returns task id.               | `@propery`      | `str`                      |

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

| **Method**      | **Description**             | **Parameters** | **Returns**                 |
|-----------------|-----------------------------|----------------|-----------------------------|
| `execute`       | Executes the task.          | `None`         | `None`                      |
| `alive_date_ms` | Returns task alive date ms. | `@propery`     | `int` Alive date in ms.     |
| `start_date_ms` | Returns task start date ms. | `@propery`     | `int` Start date in ms.     |
| `start_date_ms` | Sets task start date ms.    | `@setter`      | `None`                      |
| `task_state`    | Returns task state.         | `@propery`     | `TaskStateEnum` Task state. |
| `task_state`    | Sets task state.            | `@setter`      | `None`                      |


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

### Example 1: Add tasks with `STRICT_PRIORITY` queue placement.

Create a threads pool manager with 2 executors pool size.

```python
from nrt_threads_utils.threads_pool_manager import ThreadsPoolManager

threads_pool_manager = ThreadsPoolManager(executors_pool_size=2)
threads_pool_manager.start()
```
![init-threads-pool-manager-2-executors.png.png](information/pictures/init-threads-pool-manager-2-executors.png)

Add two tasks to the threads pool manager.<br>
The tasks will be executed as the two executors are empty.

```python
from nrt_threads_utils.threads_pool_manager import ThreadTask

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

### Example 2: Add tasks with `AVOID_STARVATION_PRIORITY` queue placement.

Create a threads pool manager with 2 executors pool size.
`avoid_starvation_amount` is set to 1.

```python
from nrt_threads_utils.threads_pool_manager import ThreadsPoolManager

threads_pool_manager = ThreadsPoolManager(executors_pool_size=2)
threads_pool_manager.avoid_starvation_amount = 1
threads_pool_manager.start()
```
![init-threads-pool-manager-2-executors.png](information/pictures/init-threads-pool-manager-2-executors.png)

Add 2 tasks in priority 1.<br>

```python
from nrt_threads_utils.threads_pool_manager import ThreadTask, QueuePlacementEnum

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