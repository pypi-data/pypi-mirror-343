from __future__ import annotations
from typing import Literal

from .parser import parse_interval, sum_units
from asyncio import sleep
from typing_extensions import (
    cast,
    NotRequired,
    Self,
    TypedDict,
    Unpack,
)


class Scheduler:
    """
    The main module entrypoint.

    Example usage:

    ```py
    from asyncio import run
    from runevery import Scheduler

    scheduler = Scheduler()

    @scheduler.every(seconds=5)
    async def mytask():
        print("yay!")

    run(scheduler.loop())
    ```
    """

    def __init__(self) -> None:
        self.tasks: dict[str, SchedulingTask] = {}
        self.name_counters: dict[str, int] = {}

    async def tick(self, sleep_duration: float = 1e-5) -> None:
        """send ticks to every task, releasing control on every iteration"""
        for task in self:
            task.tick(self)
            await sleep(sleep_duration)

    async def loop(self, sleep_duration: float = 1e-5) -> None:
        """run scheduler indefinitely"""
        while True:
            await self.tick(sleep_duration)

    async def tick_nowait(self) -> None:
        """send ticks to every task, but do not release control at all"""
        for task in self:
            task.tick(self)

    def add_task(self, task: SchedulingTask) -> None:
        key: str = task.final_name
        callback_name: str = key

        if key not in self.name_counters:
            self.name_counters[key] = 0
        else:
            callback_name = f"{key} #{self.name_counters[key]}"

        self.name_counters[key] += 1

        self.tasks[callback_name] = task

    def remove_task(self, task: SchedulingTask) -> SchedulingTask | None:
        for key in self.tasks:
            if self.tasks[key] is task:
                return self.tasks.pop(key)

    def __iter__(self):
        """This method iterates over scheduled tasks, adapting to all the changes in the task set (e.g. if tasks are added or removed in the middle of scheduling)"""
        visited: set[str] = set()

        while True:
            keys = self.tasks.keys()

            # here we get all unvisited tasks by filtering existing & visited tasks, and XORing those with existing tasks
            # we can't just use `keys ^ visited` since some tasks are visited but are not present in keys (removed between iterations)
            unvisited = keys ^ (keys & visited)

            # ...for the same reason as in previous comment, we cannot just check if `len(keys) == len(visited)` (visited is not always a subset of keys)
            if not unvisited:
                break

            # get a random-ish task
            key = unvisited.pop()
            task = self.tasks[key]
            visited.add(key)

            yield task

    def plan(self, **kwargs: Unpack[SchedulerPolicyKwargs]) -> SchedulerPolicy:
        return SchedulerPolicy(scheduler=self).derive(**kwargs)

    def once(self, **kwargs: Unpack[SchedulerPolicyKwargs]) -> SchedulerPolicy:
        """Although this may seem useless, this is a convenient way to do some stuff on startup or launch a long-running task along other tasks"""
        return self.after(ts=1, **kwargs)

    def __call__(self, **kwargs: Unpack[SchedulerPolicyKwargs]):
        return self.plan(**kwargs)

    def every(self, **kwargs: Unpack[SchedulerPolicyKwargs]) -> EverySchedulerPolicy:
        return EverySchedulerPolicy(scheduler=self).derive(**kwargs)

    def after(
        self, ts: float, **kwargs: Unpack[SchedulerPolicyKwargs]
    ) -> AtSchedulerPolicy:
        """This task will run after the specified unix timestamp"""
        kwargs["offset"] = ts
        return AtSchedulerPolicy(scheduler=self).derive(**kwargs)

    def at(
        self, *, interval: float, **kwargs: Unpack[SchedulerPolicyKwargs]
    ) -> AtSchedulerPolicy:
        """

        Runs the task at some fixed offset from Unixtime 0. The usual interval arguments (like hours, seconds, etc.) are used for the offset here, and `interval` is used for the interval itself.

        For example, run a task at 3PM UTC every day:

        ```py
        @scheduler.at(
            hours=15,
            interval=86400
        )
        async def its3pm():
            print("yeah!")
        ```
        """

        offset = sum_units(dict(kwargs)) + kwargs.get("offset", 0)

        kwargs = cast(
            SchedulerPolicyKwargs, {k: v for k, v in kwargs.items() if k not in units}
        )

        kwargs["offset"] = offset
        kwargs["seconds"] = interval

        return AtSchedulerPolicy(
            scheduler=self,
        ).derive(**kwargs)


units: set[str] = {
    "milliseconds",
    "seconds",
    "minutes",
    "hours",
    "days",
    "weeks",
    "ms",
    "s",
    "m",
    "h",
    "d",
    "w",
}

IntervalStrategy = Literal["start", "end"]


class SchedulerPolicyInternal(TypedDict):
    scheduler: Scheduler
    planner: NotRequired[SchedulingPlanner | None]
    on_error: NotRequired[TaskCallback | None]
    name: NotRequired[str | None]
    interval_strategy: NotRequired[IntervalStrategy]


class SchedulerPolicyKwargs(TypedDict):
    # basic policy fields
    on_error: NotRequired[TaskCallback | None]
    name: NotRequired[str | None]
    planner: NotRequired[SchedulingPlanner]

    # scheduler (why not)
    scheduler: NotRequired[Scheduler]

    # units
    milliseconds: NotRequired[float]
    seconds: NotRequired[float]
    minutes: NotRequired[float]
    hours: NotRequired[float]
    days: NotRequired[float]
    weeks: NotRequired[float]
    ms: NotRequired[float]
    s: NotRequired[float]
    m: NotRequired[float]
    h: NotRequired[float]
    d: NotRequired[float]
    w: NotRequired[float]

    offset: NotRequired[float]
    """Offset, used in `FixedOffsetPlanner`, as well as in `run.at` and `run.after`"""

    use_cooldown: NotRequired[CooldownSource | None]
    """If given, the policy will use CooldownPlanner, that checks if task is ready by retrieving its cooldown"""

    interval_strategy: NotRequired[IntervalStrategy]
    """
    The interval strategy defines if the interval is counted from the start of the run or from the end. 
    
    The "start" option (default) is suitable if you want to start tasks at fixed intervals, without drifting off.
    The "end" option is better when you want to wait some time between tasks.
    """


class SchedulerPolicy:
    def __init__(
        self,
        **kwargs: Unpack[SchedulerPolicyInternal],
    ):
        self.scheduler = kwargs["scheduler"]
        self.planner = kwargs.get("planner")
        self.on_error = kwargs.get("on_error")
        self.name = kwargs.get("name")
        self.interval_strategy: IntervalStrategy = kwargs.get(
            "interval_strategy",
            "start",
        )

    def derive(self, **kwargs: Unpack[SchedulerPolicyKwargs]) -> Self:
        interval = sum_units(dict(kwargs))

        offset = kwargs.get("offset")
        use_cooldown = kwargs.get("use_cooldown")

        if any([interval, offset, use_cooldown]):
            if offset is not None:
                planner = FixedOffsetPlanner(
                    offset,
                    interval=interval,
                    interval_strategy=self.interval_strategy,
                )
            elif use_cooldown is not None:
                planner = CooldownPlanner(
                    use_cooldown,
                    interval=interval,
                    interval_strategy=self.interval_strategy,
                )
            else:
                planner = IntervalPlanner(
                    interval=interval,
                    interval_strategy=self.interval_strategy,
                )

            kwargs["planner"] = planner

        data = {
            "scheduler": self.scheduler,
            "planner": self.planner,
            "on_error": self.on_error,
            "name": self.name,
        }

        data.update({k: v for k, v in kwargs.items() if k in data})

        return self.__class__(**data)

    def __call__(
        self,
        f: TaskCallback,
    ) -> TaskCallback:
        self.scheduler.add_task(
            SchedulingTask(
                callback=f,
                planner=self.planner
                or NeverPlanner(interval_strategy=self.interval_strategy),
                on_error=self.on_error,
            )
        )
        return f


class EverySchedulerPolicy(SchedulerPolicy):
    def __getattr__(self, attr: str) -> SchedulerPolicy:
        interval = parse_interval(attr)

        return self.derive(seconds=interval)


class AtSchedulerPolicy(SchedulerPolicy):
    def __init__(self, *, offset: float = 0, **kwargs: Unpack[SchedulerPolicyInternal]):
        self.offset = offset
        super().__init__(**kwargs)

    def derive(self, **kwargs) -> Self:
        kwargs["offset"] = kwargs.get("offset", self.offset)

        return super().derive(**kwargs)


run = Scheduler()


from .task import SchedulingTask, TaskCallback
from .planners import (
    CooldownSource,
    CooldownPlanner,
    FixedOffsetPlanner,
    IntervalPlanner,
    NeverPlanner,
    SchedulingPlanner,
)
