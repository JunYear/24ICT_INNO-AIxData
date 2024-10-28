from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from .speech_processing import speech_to_text, analyze_text
from .models import save_analysis_result

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
UPLOAD_FOLDER = 'data/uploads/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 음성 인식 및 분석
        text = speech_to_text(filepath)
        feedback = analyze_text(text)

        # 결과 저장
        result_id = save_analysis_result(text, feedback)

        return jsonify({'result_id': str(result_id), 'text': text, 'feedback': feedback}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400
