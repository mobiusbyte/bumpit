from dataclasses import dataclass
from typing import Any


@dataclass
class Strategy:
    name: str
    increment_transform: Any
    static_transform: Any
    version_parser: Any
