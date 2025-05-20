from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict_from_url", methods=["POST"])  # Ensure the method is POST
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # file.save(f"./uploads/{file.filename}")
    
    return jsonify({"message": f"File '{file.filename}' uploaded successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
