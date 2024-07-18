from flask import Flask, request, jsonify

from models.testcase import Testresult
from services.chroma_service import ChromaService
from services.testcase_service import TestcaseService

app = Flask(__name__)


@app.route("/testExpectation", methods=["POST"])
def execute_test():
    payload = request.get_json()
    testcase = TestcaseService.create_testcase_from_dict(payload)
    similarity_chunks = ChromaService.get_chunks(testcase.question, 15)
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
        similarity_chunks = ChromaService.get_chunks(testcase.question, 15, {"tag": "g1"})
        print(similarity_chunks)
        expectations_for_testcase_met = testcase_service.are_all_expectations_met(similarity_chunks=similarity_chunks,
                                                                                  expectations=testcase.expectations)

        if expectations_for_testcase_met:
            test_result.successful.append(testcase.question)
            test_result.successCount += 1
        else:
            test_result.unsuccessful.append(testcase.question)
            test_result.failCount += 1

    return jsonify(test_result), 200

@app.route("/initialize_data", methods=["POST"])
def load_data():
    new_chroma = ChromaService()
    new_chroma.add_document('./data/g1.pdf', 'g1')
    new_chroma.add_document('./data/netznutzungsvertrag.pdf', 'netz')

    return "success", 200
