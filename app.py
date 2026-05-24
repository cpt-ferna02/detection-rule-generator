from flask import Flask, render_template, request, jsonify
from generator import generate_detection_rules
import traceback

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    threat = data.get("threat", "").strip()
    mitre_id = data.get("mitre_id", "").strip()

    if not threat:
        return jsonify({"error": "Please provide a threat description."}), 400

    try:
        result = generate_detection_rules(threat, mitre_id)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)