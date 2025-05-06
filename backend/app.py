# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pdf_processor import analyze_french_history, prompt  # 導入 prompt

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return "I am backend i am running"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("控制台訊息: 後端未收到任何檔案")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        print("控制台訊息: 後端收到空檔案選擇")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        try:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            print(f"控制台訊息: 後端成功收到PDF檔案: {file.filename}")
            
            pdf_files = [filepath]
            print(f"控制台訊息: 正在分析 {file.filename} ...")  # 添加「正在分析」訊息
            response_text, prompt_token, output_token = analyze_french_history(pdf_files, prompt)
            print(f"控制台訊息: PDF分析完成，結果: {response_text}")
            
            return jsonify({
                'message': 'PDF uploaded and analyzed successfully',
                'filename': file.filename,
                'analysis_result': response_text,
                'prompt_token': prompt_token,
                'output_token': output_token
            }), 200
            
        except Exception as e:
            print(f"控制台訊息: PDF處理失敗，錯誤: {str(e)}")
            return jsonify({'error': f'Failed to process PDF: {str(e)}'}), 500
    else:
        print(f"控制台訊息: 收到無效檔案格式: {file.filename}")
        return jsonify({'error': 'Invalid file format. Please upload a PDF'}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)