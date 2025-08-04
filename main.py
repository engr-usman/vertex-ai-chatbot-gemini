from flask import Request, jsonify, make_response, request as flask_request
import vertexai
from vertexai.preview.generative_models import GenerativeModel


def chatbot(request: Request):
    try:
        # Handle CORS preflight
        if request.method == "OPTIONS":
            response = make_response()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            return response

        # Healthcheck endpoint
        if flask_request.path == "/healthcheck":
            response = make_response("Chatbot function is healthy ✅", 200)
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

        # Handle GET requests for testing
        if request.method == "GET":
            prompt = request.args.get("prompt", "")
            if not prompt:
                response = make_response(jsonify({"error": "Prompt query param missing"}), 400)
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response
            return _generate_response(prompt)

        # Handle POST with JSON payload
        data = request.get_json(silent=True)
        prompt = data.get("prompt", "") if data else ""

        if not prompt:
            response = make_response(jsonify({"error": "Prompt is missing"}), 400)
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

        return _generate_response(prompt)

    except Exception as e:
        result = make_response(jsonify({"error": str(e)}), 500)
        result.headers["Access-Control-Allow-Origin"] = "*"
        return result


def _generate_response(prompt: str):
    vertexai.init(project="gcp-learning-01-463711", location="us-central1")
    model = GenerativeModel("gemini-2.5-flash")  # Use a supported model
    response = model.generate_content(prompt)
    result = make_response(jsonify({"response": response.text}))
    result.headers["Access-Control-Allow-Origin"] = "*"
    return result
