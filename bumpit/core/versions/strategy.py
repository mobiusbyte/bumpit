from dataclasses import dataclass
from typing import Any


@dataclass
class StrategySettings:
    target_strategy: str
    current_version: str
    version_format: Any


@dataclass
class Strategy:
    name: str
    increment_transform: Any
    static_transform: Any
    version_parser: Any
