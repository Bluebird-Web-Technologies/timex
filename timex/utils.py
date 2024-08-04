def time_dict(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = int(seconds)

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
    }


def str_format_duration(td):
    duration = time_dict(td)

    duration_arr = []

    for key, value in duration.items():
        if value is not None and value > 0:
            duration_arr.append(f"{value} {key}")

    return ", ".join(duration_arr)
