from flask import Flask
from flask_cors import CORS

from routes.chat_routes import chat_bp

app = Flask(__name__)

# Allow React frontend to communicate with Flask
CORS(app)

# Register chat routes
app.register_blueprint(chat_bp, url_prefix="/api")


@app.route("/")
def home():
    return {
        "message": "Diagnostics Chatbot API is running"
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000)