from dataclasses import dataclass
from datetime import date


@dataclass
class CalVer:
    version_format: str
    formatter: str
    calendar_date: date = date(2000, 1, 1)
    major: int = 0
    minor: int = 0
    micro: int = 0
    modifier: str = ""

    def __str__(self):
        return self.formatter.format(
            calendar_date=self.calendar_date,
            calendar_short_year=self.calendar_date.year % 100,
            major=self.major,
            minor=self.minor,
            micro=self.micro,
            modifier=self.modifier or "",
        )
