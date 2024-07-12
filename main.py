from flask import Flask, request, jsonify

from internal_gpt import InternalGPT
from models.expecations import are_all_expectations_met, build_expecation_test_response, create_testcase_from_dict, \
    Testresult
from vectorizer import Vectorizer

app = Flask(__name__)


@app.route("/testExpectation", methods=["POST"])
def execute_test():
    payload = request.get_json()
    testcase = create_testcase_from_dict(payload)

    vectorizer = Vectorizer()
    similarity_chunks = vectorizer.get_chunks(testcase.question, 15)
    expectations_met = are_all_expectations_met(similarity_chunks, testcase.expectations)
    response_data = build_expecation_test_response(similarity_chunks, expectations_met)
    return jsonify(response_data), 200


@app.route("/testExpectations", methods=["POST"])
def execute_tests():
    payload = request.get_json()

    testcases = [create_testcase_from_dict(data) for data in payload]
    vectorizer = Vectorizer()

    test_result: Testresult = Testresult(successful=[], unsuccessful=[], successCount=0, failCount=0)

    for testcase in testcases:
        similarity_chunks = vectorizer.get_chunks(testcase.question, 15)
        expectations_for_testcase_met = are_all_expectations_met(similarity_chunks, testcase.expectations)

        if expectations_for_testcase_met:
            test_result.successful.append(testcase.question)
            test_result.successCount += 1
        else:
            test_result.unsuccessful.append(testcase.question)
            test_result.failCount += 1

    return jsonify(test_result), 200


@app.route("/")
def answer_question():
    internal_gpt = InternalGPT()
    response = internal_gpt.answer_question(query='query')
    return response


@app.route("/process_question", methods=["POST"])
def process_question():
    payload = request.get_json()
    question = payload['data']
    internal_gpt = InternalGPT()
    print("!!!!")
    print(question)
    return internal_gpt.answer_question(query=question)
