from flask import Blueprint, jsonify
from pdf_processor import analyze_french_history, prompt
import random
import google.generativeai as genai
import os
import json

# 配置Gemini API
GOOGLE_API_KEY = "AIzaSyCVRn89Q4lURX5-Sy_Sdw-Ncv6zNEqbtEc"  # 请替换为你的实际API key
genai.configure(api_key=GOOGLE_API_KEY)

# 使用正確的模型名稱
model = genai.GenerativeModel("gemini-1.5-pro")

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
        
        return questions
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        # 如果生成失败，返回一些默认问题
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

@quiz_bp.route('/api/quiz/questions', methods=['GET'])
def get_quiz_questions():
    try:
        # 获取最新的PDF分析内容
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
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500 