from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # To allow cross-origin requests

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    # Save the image to the uploads folder
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    return jsonify({'message': 'Image uploaded successfully!', 'file_path': image_path}), 200

if __name__ == '__main__':
    app.run(debug=True)