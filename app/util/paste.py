EXPIRY_TIMES_SECONDS = [0, 300, 600, 1800, 86400, 604800, 1209600, 18144000]
TIME_DURATION_UNITS = (
    ("month", 60 * 60 * 24 * 7 * 30),
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


def construct_expiry_values(forbid_infinite=False):
    options = []

    for time in EXPIRY_TIMES_SECONDS:
        if forbid_infinite and time == 0:
            continue
        options.append({"label": human_time_duration(time), "value": time})

    return options


# https://gist.github.com/borgstrom/936ca741e885a1438c374824efb038b3
def human_time_duration(seconds):
    if seconds == 0:
        return "Never"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)
