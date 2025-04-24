from datetime import datetime

duration_sizes = {86400000: "d", 3600000: "h", 60000: "m", 1000: "s", 1: "ms"}


def format_duration(duration: float) -> str:
    parts: list[str] = []

    duration *= 1000

    for size, suffix in duration_sizes.items():
        amount = int(duration // size)

        if amount:
            parts.append(f"{amount}{suffix} ")

        duration %= size

    return "".join(parts).strip()


def format_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("[%d.%m.%Y, %H:%M:%S, %:::z]")
