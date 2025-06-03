# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from pdf_processor import analyze_french_history, prompt
from quiz_generator import quiz_bp

app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")

# 配置 CORS
CORS(app, 
     resources={
         r"/*": {  # 允許所有路由
             "origins": ["http://localhost:8080", "http://localhost:8081"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type"],
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "X-CSRFToken"],
             "max_age": 600
         }
     })

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 註冊 quiz blueprint
app.register_blueprint(quiz_bp)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

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

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        # 獲取上傳的文件
        if 'file' not in request.files:
            return jsonify({'error': '沒有上傳文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '沒有選擇文件'}), 400
        
        # 保存文件
        file_path = f"uploads/{file.filename}"
        file.save(file_path)
        
        # 分析文件
        result, prompt_token, output_token = analyze_french_history([file_path], prompt)
        
        return jsonify({
            'success': True,
            'result': result,
            'token_usage': {
                'prompt_tokens': prompt_token,
                'output_tokens': output_token
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)