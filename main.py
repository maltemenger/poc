from flask import Flask, request, jsonify

from models.expecations import TestcaseService, Testresult
from services.vectorservice import VectorService

app = Flask(__name__)


@app.route("/testExpectation", methods=["POST"])
def execute_test():
    payload = request.get_json()
    testcase = TestcaseService.create_testcase_from_dict(payload)
    similarity_chunks = VectorService.get_chunks(testcase.question, 15)
    expectations_met = TestcaseService.are_all_expectations_met(similarity_chunks, testcase.expectations)
    response_data = TestcaseService.build_expecation_test_response(similarity_chunks, expectations_met)
    return jsonify(response_data), 200


@app.route("/testExpectations", methods=["POST"])
def execute_tests():
    payload = request.get_json()
    testcases = [TestcaseService.create_testcase_from_dict(data) for data in payload]
    test_result: Testresult = Testresult(successful=[], unsuccessful=[], successCount=0, failCount=0)
    testcase_service = TestcaseService()

    for testcase in testcases:
        similarity_chunks = VectorService.get_chunks(testcase.question, 5000)
        expectations_for_testcase_met = testcase_service.are_all_expectations_met(similarity_chunks, testcase.expectations)

        if expectations_for_testcase_met:
            test_result.successful.append(testcase.question)
            test_result.successCount += 1
        else:
            test_result.unsuccessful.append(testcase.question)
            test_result.failCount += 1

    return jsonify(test_result), 200



