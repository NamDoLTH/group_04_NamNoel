from __future__ import annotations

# python built-in imports
from dataclasses import dataclass


@dataclass
class Game:
    title: str
    score: float
    score_phrase: str
    platform: str
    genre: str
    release_year: int
    release_month: int
    release_day: int
