from flask import Flask, redirect, url_for, request, jsonify
from io import BytesIO
import os
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


# Upload folder setup
UPLOAD_FOLDER = 'src/analysis/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET',])
def success():
    return "HELLO WORLD"



# Route for file upload
@app.route('/api/upload_file', methods=['POST'])
def upload_file():

    if 'audio_file' not in request.files:
        return {'error': 'No file part'}, 400
    
    audio_file = request.files['audio_file']

    if audio_file.filename == '':
        return {'error': 'No selected file'}, 400
        
    filename = ''
    if audio_file and allowed_file(audio_file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)

        print(filename)
        audio_file.save(filename)

        # Process the file with your model here
        return ({'message': 'File uploaded successfully', 'filename': audio_file.filename})
    else:
        return {'error': 'Invalid file type'}, 400




if __name__ == '__main__':
    app.run(debug=True, port=5000)
  