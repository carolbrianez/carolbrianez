import re
from datetime import date

BIRTHDATE = date(1998, 2, 7)
README_PATH = "README.md"

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def calculate_uptime(birthdate: date, today: date) -> str:
    years = today.year - birthdate.year
    months = today.month - birthdate.month
    days = today.day - birthdate.day

    if days < 0:
        months -= 1
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month > 1 else today.year - 1
        days_in_prev_month = DAYS_IN_MONTH[prev_month - 1]
        if prev_month == 2 and is_leap(prev_year):
            days_in_prev_month = 29
        days += days_in_prev_month

    if months < 0:
        years -= 1
        months += 12

    def plural(n: int, word: str) -> str:
        return f"{n} {word}{'s' if n != 1 else ''}"

    return ", ".join([
        plural(years, "year"),
        plural(months, "month"),
        plural(days, "day"),
    ])


def main() -> None:
    today = date.today()
    uptime_str = calculate_uptime(BIRTHDATE, today)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, count = re.subn(
        r"(<!--UPTIME:START-->)(.*?)(<!--UPTIME:END-->)",
        lambda m: f"{m.group(1)}{uptime_str}{m.group(3)}",
        content,
        flags=re.DOTALL,
    )

    if count == 0:
        print("No <!--UPTIME:START-->...<!--UPTIME:END--> markers found in README.md.")
        return

    if new_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated uptime to: {uptime_str}")
    else:
        print("Uptime already up to date.")


if __name__ == "__main__":
    main()
