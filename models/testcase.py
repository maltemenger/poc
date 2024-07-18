from dataclasses import dataclass
from typing import List

@dataclass
class Expectation:
    source_doc: str
    pages: List[int]

@dataclass
class Testcase:
    question: str
    expectations: List[Expectation]


@dataclass
class Testclass:
    question: str


@dataclass
class Testresult:
    successful: list[str]
    successCount: int
    unsuccessful: list[str]
    failCount: int
