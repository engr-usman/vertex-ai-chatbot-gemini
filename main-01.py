from flask import Request, jsonify, make_response
import vertexai
from vertexai.preview.generative_models import GenerativeModel


def chatbot(request: Request):
    try:
        if request.method == "OPTIONS":
            # Handle CORS preflight
            response = make_response()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "POST"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            return response

        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return make_response(jsonify({"error": "Prompt is missing"}), 400)

        vertexai.init(project="gcp-learning-01-463711", location="us-central1")
        model = GenerativeModel("gemini-2.5-flash")  # Or any supported one
        response = model.generate_content(prompt)

        result = make_response(jsonify({"response": response.text}))
        result.headers["Access-Control-Allow-Origin"] = "*"
        return result

    except Exception as e:
        result = make_response(jsonify({"error": str(e)}), 500)
        result.headers["Access-Control-Allow-Origin"] = "*"
        return result
