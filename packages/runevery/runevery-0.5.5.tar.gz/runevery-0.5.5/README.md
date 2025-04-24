# Runevery task when it's time

Runevery (one word, as in 'bakery') is a simple async scheduling library designed to schedule tasks in _no time_. With a simple and intuitive API, you can plan and manage tasks to run at specific intervals, times, or even based on custom conditions. No more writing complex loops and time checks!

> [!NOTE]
> It is highly recommended to use type-checking with runevery. Not only did I spent some time polishing it here, but also types are cool and nice. And I won't be covering some stuff that is obvious from the names.

> [!IMPORTANT]
> This package is fresh and both the readme and the API are not very stable and finished. Feel free to create issues and stuff, but be aware that this is at its early stages.

## Installation

You can install runevery from PyPI using pip. Just run:

```sh
pip install runevery
```

Or, if you prefer Poetry:

```sh
poetry add runevery
```

For more details, check out the [PyPI page](https://pypi.org/project/runevery/).

## Basic usage

Let's start with some basic usage examples to get you familiar with runevery.

### Example: Fetching emails every 10 minutes

Suppose you want to fetch your emails every 10 minutes. Here's how you can do it:

```python
from asyncio import run as asyncio_run
from runevery import run

@run.every(minutes=10)
async def fetch_emails():
    print("Very convincing code to fetch e-mails or something")

asyncio_run(run.loop())
```

### Example: Updating weather data every hour

Need to update your weather data every hour? No problem!

```python
from asyncio import run as asyncio_run
from runevery import run

@run.every(hours=1)
async def update_weather():
    print("Updating weather data...")

asyncio_run(run.loop())
```

### Example: Running a task once at startup

Sometimes, you might want to run a task just once at startup. Here's how:

```python
from asyncio import run as asyncio_run
from runevery import run

@run.once()
async def startup_task():
    print("Running startup task...")

asyncio_run(run.loop())
```

### Example: Running a task after a specific time

Want to run a task after a specific Unix timestamp, just for fun? We have a tool for that, it's called `scheduler.after`:

```python
from asyncio import run as asyncio_run
from runevery import run

@run.after(offset=1718567362)
async def run_after_timestamp():
    print("Running after specific timestamp...")

asyncio_run(run.loop())
```

## What's a scheduler, anyway?

### What is the scheduler task loop?

The scheduler and its task loop are the core of runevery. It continuously ticks through all scheduled tasks, checking if it's time to run them based on their planners.

But how does the scheduler know when to run a task? It doesn't. **CREDITS ROLL**
Okay, but actually, it just ticks every task, and each task's planner decides if it's time to run.

### What are the arguments to scheduler methods?

Let's break down the arguments you can pass to `scheduler.plan`, `scheduler.every`, `scheduler.once`, `scheduler.at`, and `scheduler.after`.

#### Example: Using `scheduler.every`

```python
from asyncio import run as asyncio_run
from runevery import run

@run.every(seconds=30)
async def every_30_seconds():
    print("Running every 30 seconds")

asyncio_run(run.loop())
```

#### Example: Using `scheduler.at`

```python
from asyncio import run as asyncio_run
from runevery import run

@run.at(interval=86400, hours=15)
async def daily_at_3pm():
    print("Running daily at 3 PM")

asyncio_run(run.loop())
```

## What's a planner?

Planners are the brains behind the scheduling. They decide if a task should run based on various conditions.

### Built-in planners

#### IntervalPlanner

Runs tasks at fixed intervals.

```python
from runevery import IntervalPlanner, run


@run.plan(planner=IntervalPlanner(interval=60))
async def every_minute():
    print("Running every minute")

asyncio_run(run.loop())
```

#### FixedOffsetPlanner

Runs tasks at a fixed timestamp, optionally repeating at intervals.

```python
from runevery import FixedOffsetPlanner, Scheduler

scheduler = Scheduler()

@scheduler.plan(planner=FixedOffsetPlanner(offset=1718567362, interval=3600))
async def hourly_after_timestamp():
    print("Running hourly after a specific timestamp")

asyncio_run(scheduler.loop())
```

#### CooldownPlanner

Runs tasks based on a cooldown period.

```python
from runevery import CooldownPlanner, run

class MyCooldownSource:
    def get_cooldown(self, interval: float):
        return 0  # Replace with actual cooldown logic

@run.plan(planner=CooldownPlanner(MyCooldownSource(), interval=300))
async def cooldown_task():
    print("Running with cooldown")

asyncio_run(run.loop())
```

## Interval strategy

The interval strategy defines if the interval is counted from the start or the end of the run.

-   Use `"start"` (default), when you want to count interval from the start of the previous task. The duration between callback starts doesn't drift, since it doesn't depend on the task duration.
-   Use `"end"`, when you care about interval _between_ tasks. This interval starts counting after the previous task has ended, so the pause between tasks doesn't drift.

```python
from runevery import run
from asyncio import sleep

@run.every(seconds=10, interval_strategy="end")
async def very_long_task():
    await sleep(3600)
    print("This task will run each ~3610 seconds, despite the interval beint 10 seconds")

asyncio_run(run.loop())
```

## Arguments to the task callback

Task callbacks can receive optional arguments like `task` and `scheduler`.

```python
from runevery import run, Scheduler, SchedulingTask

@run.every(minutes=5)
async def task_with_args(task: SchedulingTask, scheduler: Scheduler):
    print(f"Task {task.final_name} running with scheduler {scheduler}")

asyncio_run(run.loop())
```

## STOP RUNNING TASKS

Functions were not meant to be scheduled!!! Do this immediately:

```python
from runevery import run, Scheduler

@run.once()
async def stop_everything(scheduler: Scheduler):
    for task in scheduler:
        task.discard()

asyncio_run(run.loop())
```

## Pause a task

If you need to suspend (pause) the task execution `task.pause_for` and `task.pause_until` are for your service

```python
from runevery import run, SchedulingTask

@run.every(minutes=5)
async def pausable_task(task: SchedulingTask):
    print("Running pausable task")
    task.pause_for(600)  # Pause for 10 minutes

asyncio_run(run.loop())
```

## Run a task on a custom condition

Want to run a task based on a custom condition? Use a custom planner.

```python
from runevery import run, SchedulingPlanner, SchedulingTask

class CustomConditionPlanner(SchedulingPlanner):
    def check(self, task: SchedulingTask):
        return some_custom_condition()

@run.plan(planner=CustomConditionPlanner())
async def custom_task():
    print("Running custom task")

asyncio_run(scheduler.loop())
```

## Handle errors

Need to handle errors in your tasks? Provide an `on_error` callback.

```python
from runevery import run, SchedulingTask

@run.every(minutes=5, on_error=lambda task: print(f"Error in {task.final_name}"))
async def error_prone_task():
    raise Exception("Oops!")

asyncio_run(run.loop())
```

And that's it! You've now got a solid understanding of how to use runevery to schedule tasks in Python. Happy scheduling!
