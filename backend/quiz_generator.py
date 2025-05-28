from flask import Blueprint, jsonify, request
from pdf_processor import analyze_french_history, prompt
import random
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# API 金鑰列表，預設為空，將從環境變數載入
API_KEYS = [
    os.getenv('GEMINI_API_KEY_1', ''),  # 主要金鑰
    os.getenv('GEMINI_API_KEY_2', ''),  # 備用金鑰1
    os.getenv('GEMINI_API_KEY_3', '')   # 備用金鑰2
]

# 移除空值
API_KEYS = [key for key in API_KEYS if key]

# 如果沒有設置任何金鑰，添加警告訊息
if not API_KEYS:
    print("警告: 未設置任何 API 金鑰，請在 .env 文件中配置 GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3")
    # 添加一個空的金鑰以防止程式崩潰，但這會導致 API 請求失敗
    API_KEYS = ['']

current_key_index = 0
genai.configure(api_key=API_KEYS[current_key_index])

# 使用正確的模型名稱
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def rotate_api_key():
    """
    輪換到下一個可用的 API 金鑰。
    返回：bool 是否成功切換到新金鑰
    """
    global current_key_index, model
    
    # 記錄原始索引，用於判斷是否已嘗試所有金鑰
    original_index = current_key_index
    
    while True:
        # 切換到下一個金鑰
        current_key_index = (current_key_index + 1) % len(API_KEYS)
        
        # 如果已經嘗試了所有金鑰，則返回失敗
        if current_key_index == original_index:
            print("所有 API 金鑰都已嘗試且皆無法使用")
            return False
            
        try:
            print(f"切換到 API 金鑰 {current_key_index + 1}/{len(API_KEYS)}")
            genai.configure(api_key=API_KEYS[current_key_index])
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            
            # 測試新金鑰是否有效（使用簡單查詢）
            test_response = model.generate_content("Say hello")
            test_response.text  # 確認能獲取響應
            return True
            
        except Exception as e:
            print(f"API 金鑰 {current_key_index + 1} 無效或已達到配額限制: {str(e)}")
            # 繼續嘗試下一個金鑰
            continue

quiz_bp = Blueprint('quiz', __name__)

def generate_questions_from_content(content):
    # 构建提示词
    prompt = """
    Generate 5 quiz questions based on the following content. The questions should be in JSON format as follows:
    1. Single choice question format:
    {
        "type": "single",
        "question": "Question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct": 0
    }
    
    2. True/False question format:
    {
        "type": "true-false",
        "question": "Question text",
        "correct": true
    }
    
    Requirements:
    1. Questions must be based on the provided content
    2. Options should be reasonable and challenging
    3. Return format must be a valid JSON array
    4. Questions should be diverse and not repetitive
    5. Use English punctuation marks only
    6. Return ONLY the JSON array, no other text
    """
    
    # 最多嘗試所有 API 金鑰
    max_retries = len(API_KEYS)
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 使用Gemini生成问题
            response = model.generate_content([prompt, content])
            
            # 清理回應文本，只保留 JSON 部分
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # 使用 json.loads 解析 JSON
            questions = json.loads(response_text)
            
            # 验证问题格式
            for q in questions:
                if q['type'] not in ['single', 'true-false']:
                    raise ValueError(f"Invalid question type: {q['type']}")
                if q['type'] == 'single':
                    if len(q['options']) != 4:
                        raise ValueError("Single choice questions must have 4 options")
                    if not isinstance(q['correct'], int) or q['correct'] not in range(4):
                        raise ValueError("Single choice correct answer must be an integer between 0-3")
                elif q['type'] == 'true-false':
                    if not isinstance(q['correct'], bool):
                        raise ValueError("True/False correct answer must be a boolean")
            
            # 成功生成問題
            return questions
            
        except Exception as e:
            print(f"使用 API 金鑰 {current_key_index + 1} 生成問題時出錯: {str(e)}")
            # 嘗試輪換 API 金鑰
            if rotate_api_key():
                print("已切換到新的 API 金鑰，重新嘗試生成問題...")
                retry_count += 1
                continue
            else:
                # 所有金鑰都已嘗試過且失敗
                break
    
    # 所有金鑰嘗試後仍失敗，返回默認問題
    print("所有 API 金鑰在生成測驗問題時均失敗，使用默認問題")
    return [
        {
            "type": "single",
            "question": "What was the iconic event that marked the beginning of the French Revolution?",
            "options": ["Storming of the Bastille", "Execution of Louis XVI", "Napoleon's Coup", "Meeting of the Estates General"],
            "correct": 0
        },
        {
            "type": "true-false",
            "question": "The French Revolution occurred in the late 18th century?",
            "correct": True
        }
    ]

@quiz_bp.route('/api/quiz/questions', methods=['POST', 'GET'])
def get_quiz_questions():
    try:
        content = ""
        prompt_token = 0
        output_token = 0
        
        # 檢查是否為POST請求並包含數據
        if request.method == 'POST':
            data = request.json
            filename = data.get('filename', '')
            mind_map_data = data.get('mindMapData', {})
            
            print(f"接收到的檔案名稱: {filename}")
            print(f"接收到的心智圖數據: {mind_map_data}")
            
            # 如果有心智圖數據，使用它來生成問題
            if mind_map_data:
                # 將心智圖數據轉換為文本形式以供生成問題使用
                content = json.dumps(mind_map_data, ensure_ascii=False)
            else:
                # 如果沒有心智圖數據，但有文件名，嘗試找到並使用該文件
                if filename:
                    pdf_path = os.path.join('uploads', filename)
                    if os.path.exists(pdf_path):
                        content, prompt_token, output_token = analyze_french_history([pdf_path], prompt)
                    else:
                        print(f"找不到檔案: {pdf_path}")
                        content, prompt_token, output_token = analyze_french_history([], prompt)
                else:
                    content, prompt_token, output_token = analyze_french_history([], prompt)
        else:  # GET請求 (向下兼容)
            content, prompt_token, output_token = analyze_french_history([], prompt)
        
        # 生成问题
        questions = generate_questions_from_content(content)
        
        # 随机打乱问题顺序
        random.shuffle(questions)
        
        return jsonify({
            "success": True,
            "questions": questions,
            "token_usage": {
                "prompt_tokens": prompt_token,
                "output_tokens": output_token
            }
        })
    except Exception as e:
        print(f"生成測驗問題失敗: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500