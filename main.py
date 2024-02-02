from internal_gpt import InternalGPT

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def answer_question():
    internal_gpt = InternalGPT()
    response = internal_gpt.answer_question()
    return response

@app.route("/process_question", methods=["POST"])
def process_question():
    payload = request.get_json()
    question = payload['data']
    internal_gpt = InternalGPT()
    return internal_gpt.answer_question(query = question)

