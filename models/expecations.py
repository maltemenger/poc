from dataclasses import dataclass
from typing import List

from models.chunk import Chunk


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


class TestcaseService:
    @staticmethod
    def create_testcase_from_dict(data: dict) -> Testcase:
        expectations = [Expectation(**exp) for exp in data['expectations']]
        return Testcase(question=data['question'], expectations=expectations)

    @staticmethod
    def is_expectation_met(similarity_chunks: list[Chunk], expectation: Expectation) -> bool:
        expected_source_doc = expectation.source_doc
        expected_pages = expectation.pages

        filtered_chunks_by_expected_document = list(
            filter(lambda chunk: chunk.source_doc == "data/" + expected_source_doc, similarity_chunks))
        return all(page in [doc.page for doc in filtered_chunks_by_expected_document] for page in expected_pages)

    def are_all_expectations_met(self, similarity_chunks: list[Chunk], expectations: list[Expectation]) -> bool:
        return not any(not self.is_expectation_met(similarity_chunks, exp) for exp in expectations)

    @staticmethod
    def build_expecation_test_response(similariy_chunks: list[Chunk], all_expectations_met: bool):
        docs_with_test_result = []
        for doc in similariy_chunks:
            obj_dict = doc.__dict__
            docs_with_test_result.append(obj_dict)

        return {
            'allExpectationsMet': all_expectations_met,
            'objects': docs_with_test_result
        }
