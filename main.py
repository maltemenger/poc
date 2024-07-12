import json
from typing import TypedDict, List

from internal_gpt import InternalGPT

from flask import Flask, request, jsonify

from vectorizer import Vectorizer
from models.expecations import are_all_expectations_met, build_expecation_test_response

app = Flask(__name__)

@app.route("/")
def answer_question():
    internal_gpt = InternalGPT()
    response = internal_gpt.answer_question(query='query')
    return response

@app.route("/testExpectation", methods=["POST"])
def check_vectors():
    payload = request.get_json()
    question = payload['question']
    expectations = payload['expectations']

    vectorizer = Vectorizer()
    similarity_chunks = vectorizer.get_chunks(question, 15)
    expectations_met = are_all_expectations_met(similarity_chunks, expectations)
    response_data = build_expecation_test_response(similarity_chunks, expectations_met)
    return jsonify(response_data), 200


@app.route("/process_question", methods=["POST"])
def process_question():
    payload = request.get_json()
    question = payload['data']
    internal_gpt = InternalGPT()
    print("!!!!")
    print(question)
    return internal_gpt.answer_question(query=question)


