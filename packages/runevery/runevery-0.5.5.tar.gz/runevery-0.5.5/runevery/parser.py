units: dict[str, int] = {}

units["millisecond"] = 1
units["second"] = 1000
units["minute"] = 60 * units["second"]
units["hour"] = 60 * units["minute"]
units["day"] = 24 * units["hour"]
units["week"] = 7 * units["day"]


for unit in list(units):
    units[unit + "s"] = units[unit]


units["ms"] = units["millisecond"]
units["s"] = units["second"]
units["m"] = units["minute"]
units["h"] = units["hour"]
units["d"] = units["day"]
units["w"] = units["week"]


base_numbers = {
    k: i
    for i, k in enumerate(
        [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fiveteen",
            "sixteen",
            "seventeen",
            "eightteen",
            "nineteen",
        ]
    )
}

dozens = {
    k: (i + 2) * 10
    for i, k in enumerate(
        ["twenty", "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    )
}

multipliers = {
    "hundred": 100,
    "hundreds": 100,
    "thousand": 1000,
    "thousands": 1000,
    "million": 1_000_000,
    "millions": 1_000_000,
    "billion": 1_000_000_000,
    "billions": 1_000_000_000,
}


def parse_interval(interval_string: str) -> float:
    parts = [part for part in interval_string.split("_") if part != "and"]
    result = 0

    number_buf: list[int] = []
    last_multiplier = False

    for part in parts:
        if part in units:
            amount = sum(number_buf) if number_buf else 1
            result += amount * units[part]
            number_buf.clear()

        elif part in multipliers:
            amount = multipliers[part]

            if number_buf:
                number_buf[-1] *= amount
            else:
                number_buf.append(amount)

        elif part in dozens:
            number_buf.append(dozens[part])

        elif part in base_numbers:
            amount = base_numbers[part]

            if number_buf and not last_multiplier:
                number_buf[-1] += amount
            else:
                number_buf.append(amount)

        else:
            continue

        last_multiplier = part in multipliers

    if number_buf:
        result += sum(number_buf)

    return result / 1000


def sum_units(data: dict[str, object]):
    result: float = 0

    for unit, value in data.items():
        if not isinstance(value, (float, int)):
            if unit in units:
                raise TypeError(
                    f"Value '{value}' (in '{unit}={value}') is not numeric. Pass a float or int to the scheduler policy"
                )
            else:
                continue

        if unit in units:
            result += units[unit] * value

    return result / 1000
