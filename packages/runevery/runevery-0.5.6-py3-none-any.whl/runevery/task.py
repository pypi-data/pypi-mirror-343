from __future__ import annotations

import inspect
from time import time
from asyncio import Task, AbstractEventLoop, get_event_loop
from time import time
from typing_extensions import Coroutine, Callable
from heapq import heapify
from random import randint


TaskCallback = Callable[..., Coroutine[None, None, None]]


class SchedulingTask:
    def __init__(
        self,
        callback: TaskCallback,
        planner: SchedulingPlanner,
        on_error: TaskCallback | None = None,
        name: str | None = None,
    ):
        self.callback = callback
        self.callback_kwargs = self.inspect_callback(callback)
        self.on_error = on_error

        self.planner = planner
        self.runs: dict[float, Task[None]] = {}
        self.scheduled: list[float] = [self.time]
        self.name = name

        self.last_run_start: float = 0
        self.last_run_end: float = 0

    def get_last_run(self, strategy: IntervalStrategy):
        if strategy == "start":
            return self.last_run_start

        if self.last_run_start > self.last_run_end:
            # runs now
            return self.time

        return self.last_run_end

    @property
    def time(self):
        return time()

    @staticmethod
    def inspect_callback(callback: TaskCallback) -> set[str]:
        signature = inspect.signature(callback)
        return set(signature.parameters)

    def run_callback(
        self,
        callback: TaskCallback,
        scheduler: Scheduler,
        event_loop: AbstractEventLoop | None,
    ):
        if not event_loop:
            event_loop = get_event_loop()

        kwargs = {
            "task": self,
            "scheduler": scheduler,
        }

        task = event_loop.create_task(
            callback(
                **{k: v for k, v in kwargs.items() if k in self.callback_kwargs},
            )
        )

        # save a reference to callback run so GC will not delete the task
        random_id = randint(0, int(10e9))
        self.runs[random_id] = task
        task.add_done_callback(lambda _: self.runs.pop(random_id, None))

    def tick(self, scheduler: Scheduler, event_loop: AbstractEventLoop | None = None):
        if self.planner.check(self):
            self.last_run_start = self.time
            self.run(self.callback, scheduler, event_loop)
            self.planner.on_run(self)
            self.last_run = self.time

    def run(self, callback: TaskCallback, scheduler: Scheduler, event_loop):
        async def callback_wrapper(**kwargs):
            try:
                await callback(**kwargs)
            except Exception as e:
                if self.on_error:
                    self.run_callback(self.on_error, scheduler, event_loop)
                else:
                    raise e

        self.run_callback(callback_wrapper, scheduler, event_loop)

    def discard(self):
        self.planner = NeverPlanner(interval_strategy="start")

    def pause_until(self, ts: float):
        def reinstate_switch(task: SchedulingTask):
            new_planner.planners.pop(new_planner.planner_index)
            self.planner = new_planner.planners[0]
            return 0

        paused = FixedOffsetPlanner(offset=ts, interval=0)

        new_planner = SwitchPlanner(
            planners=[self.planner, paused],
            switch_callback=reinstate_switch,
        )

        self.planner = new_planner

    def pause_for(self, duration: float):
        return self.pause_until(self.time + duration)

    @property
    def default_name(self):
        return self.callback.__name__

    @property
    def final_name(self):
        return self.name or self.default_name

    def __repr__(self):
        return f"Task['run {self.final_name} {self.planner}']"


from .scheduler import IntervalStrategy, Scheduler
from .planners import FixedOffsetPlanner, NeverPlanner, SchedulingPlanner, SwitchPlanner
