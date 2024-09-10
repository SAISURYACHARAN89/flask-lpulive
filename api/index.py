from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allows all origins by default

@app.route('/', methods=['GET'])
def get_data():
    """
    API endpoint to get user details from LPU Live.
    """
    id = request.args.get('id')
    token = "9daacfb1e97a628660431de6c9442481"
    url = f"https://lpulive.lpu.in/fugu-api/api/chat/groupChatSearch?en_user_id={token}&search_text={id}&user_role=USER"
    
    try:
        response = requests.get(url, headers={"app_version": "1.0.0", "device_type": "WEB"})
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        users = data.get("data", {}).get("users", [])
        if not users:
            return jsonify({"detail": "No user found."}), 404
        
        return jsonify({"users": users}), 200
    
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": "HTTP error occurred", "message": str(http_err)}), 500
    except Exception as err:
        return jsonify({"error": "An error occurred", "message": str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
