import os
from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS


app = Flask(__name__)

# Enable CORS for all domains
CORS(app)

# Upload folder setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg'}



@app.route('/', methods=['GET',])
def success():
    return "HELLO WORLD"


@app.route('/api/test', methods=['GET',])
def test():
    return jsonify({"status":"success"})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/upload_file', methods=['POST',])
def upload_file():

    print(request)

    if 'audioFile' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['audioFile']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    print(file.filename)

    if file and allowed_file(file.filename):
        # Save the file to the upload folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # You can add additional processing logic here (e.g., audio analysis)
        return jsonify({"message": "File uploaded successfully", "file": filename}), 200
    else:
        return jsonify({"message": "Invalid file format"}), 400



if __name__ == '__main__':
    app.run(debug=True)
  