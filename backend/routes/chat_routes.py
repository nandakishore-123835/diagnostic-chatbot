from flask import Blueprint, request, jsonify

from services.diagnostic_service import (
    find_dtc,
    extract_dtc_code
)

from services.prompt_service import create_prompt
from services.model_service import generate_answer


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is missing."
        }), 400

    query = data.get("query", "").strip()

    if not query:
        return jsonify({
            "success": False,
            "message": "Please enter a car problem."
        }), 400


    # Extract DTC code
    dtc_code = extract_dtc_code(query)


    # Search DTC database
    diagnostic_data = None

    if dtc_code:
        diagnostic_data = find_dtc(dtc_code)


    # Create prompt
    prompt = create_prompt(
        query,
        diagnostic_data
    )


    # Generate response
    response = generate_answer(prompt)


    return jsonify({
        "success": True,
        "query": query,
        "dtc_code": dtc_code,
        "response": response
    })