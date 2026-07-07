def pace_to_seconds(pace):
    if not pace or ":" not in pace:
        return None

    minutes, seconds = pace.split(":")
    return int(minutes) * 60 + int(seconds)


def seconds_to_pace(seconds):
    minutes = seconds // 60
    rest_seconds = seconds % 60
    return f"{minutes}:{rest_seconds:02d}"


def average_runs(runs):
    count = len(runs)

    valid_paces = [
        pace_to_seconds(run[3])
        for run in runs
        if pace_to_seconds(run[3]) is not None
    ]

    avg_pace_seconds = sum(valid_paces) / len(valid_paces) if valid_paces else 0

    return {
        "kilometer": sum(run[1] for run in runs) / count,
        "dauer": sum(run[2] for run in runs) / count,
        "pace_seconds": avg_pace_seconds,
        "pace": seconds_to_pace(int(avg_pace_seconds)) if avg_pace_seconds else "Keine gültige Pace",
        "puls": sum(run[4] for run in runs) / count,
        "hoehenmeter": sum(run[5] for run in runs) / count,
        "kalorien": sum(run[6] for run in runs) / count,
    }


def compare_current_run(current_run, averages):
    current_pace_seconds = pace_to_seconds(current_run[3])

    pace_diff = None
    if current_pace_seconds is not None:
        pace_diff = current_pace_seconds - averages["pace_seconds"]

    return {
        "kilometer_diff": current_run[1] - averages["kilometer"],
        "dauer_diff": current_run[2] - averages["dauer"],
        "pace_diff": pace_diff,
        "puls_diff": current_run[4] - averages["puls"],
        "hoehenmeter_diff": current_run[5] - averages["hoehenmeter"],
        "kalorien_diff": current_run[6] - averages["kalorien"],
    }


def generate_summary(comparison):
    pace_diff = comparison["pace_diff"]
    puls_diff = comparison["puls_diff"]
    hoehenmeter_diff = comparison["hoehenmeter_diff"]

    if pace_diff is not None and pace_diff < -3 and puls_diff <= 2:
        return "🟢 Starker Lauf: Du warst schneller als dein Durchschnitt und dein Puls blieb nahezu gleich. Das spricht für eine gute Entwicklung."

    if pace_diff is not None and pace_diff < -3 and puls_diff > 2:
        return "🟡 Du warst schneller als dein Durchschnitt, hattest aber auch einen höheren Puls. Das spricht eher für eine intensivere Einheit."

    if pace_diff is not None and pace_diff > 3 and hoehenmeter_diff > 5:
        return "🟡 Die Pace war etwas langsamer, allerdings hattest du mehr Höhenmeter. Der Lauf war dadurch vermutlich anspruchsvoller."

    if pace_diff is not None and pace_diff > 3 and puls_diff > 2:
        return "🔴 Der Lauf war langsamer und dein Puls lag höher. Das könnte auf Müdigkeit, Hitze oder schlechtere Regeneration hindeuten."

    return "🔵 Dein Lauf liegt insgesamt ungefähr im Bereich deines Durchschnitts der letzten drei Einheiten."