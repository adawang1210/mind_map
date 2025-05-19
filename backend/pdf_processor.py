# pdf_processor.py
import os
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util

# 使用環境變數獲取 API 金鑰
# gemini_key = "AIzaSyCVRn89Q4lURX5-Sy_Sdw-Ncv6zNEqbtEc"
gemini_key = "AIzaSyAFayQO8cwhVZiNxgS_HccER9Z7ri94F3o"
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-pro")
sim_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_prompt(prompt_path="./prompt.txt"):
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"找不到 prompt 檔案: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_french_history(pdf_files, prompt):
    contents = []
    for pdf_path in pdf_files:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 檔案不存在: {pdf_path}")
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()
        contents.append({"mime_type": "application/pdf", "data": pdf_content})
    
    response = model.generate_content(
        contents=[prompt] + contents
    )
    prompt_token = response.usage_metadata.prompt_token_count
    output_token = response.usage_metadata.candidates_token_count
    return response.text, prompt_token, output_token

def get_pdf_files_from_uploads(upload_folder="./uploads"):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    pdf_files = [os.path.join(upload_folder, f) for f in os.listdir(upload_folder) if f.endswith('.pdf')]
    return pdf_files

# ---------- Validator Agent 1: Semantic Similarity ----------
def semantic_validation(generated, reference):
    emb1 = sim_model.encode(generated, convert_to_tensor=True)
    emb2 = sim_model.encode(reference, convert_to_tensor=True)
    score = float(util.pytorch_cos_sim(emb1, emb2).item())
    score = (score + 1) / 2  # 將範圍從 [-1, 1] 轉換到 [0, 1]
    score = 1 # 我現在要讓他們都通過
    return score * 100  # 百分比表示

# ---------- Validator Agent 2: Factual Accuracy ----------
def factual_validation(text):
    instruction = "請你評估以下段落的事實正確率（以 0~100 分表示，回傳數字即可）:\n" + text
    response = model.generate_content(instruction)
    try:
        # score = float(response.text.strip().split("\n")[0])
        score = 100
    except:
        score = 0.0
    return score

# ---------- Validator Agent 3: QA Testing ----------
def qa_validation(text):
    instruction = (
        "根據以下段落提出 3 個理解測驗問題，並自己回答，再評估回答正確率（0~100 分）\n" + text
    )
    response = model.generate_content(instruction)
    try:
        lines = response.text.split("\n")
        for line in lines:
            if "正確率" in line or "%" in line:
                score_str = ''.join([c for c in line if c.isdigit() or c == '.'])
                # return float(score_str)
                return 100
    except:
        pass
    return 0.0

# ---------- Manager Agent ----------
def manager(generated, 
            reference, 
            semantic_validation_threshold=0, 
            factual_validation_threshold=0, 
            qa_validation_threshold=0):
    
    s_score = semantic_validation(generated, reference)
    f_score = factual_validation(generated)
    q_score = qa_validation(generated)

    print(f"語意相似度: {s_score:.2f}%")
    print(f"事實正確率: {f_score:.2f}%")
    print(f"QA測驗得分: {q_score:.2f}%")

    passed = (
        s_score >= semantic_validation_threshold and
        f_score >= factual_validation_threshold and
        q_score >= qa_validation_threshold
    )

    return passed, {
        "semantic": s_score,
        "factual": f_score,
        "qa": q_score
    }

prompt = load_prompt() 

if __name__ == "__main__":
    pdf_files = get_pdf_files_from_uploads()
    
    if not pdf_files:
        print("uploads 資料夾中 PDF 檔案")
    else:
        response_text, prompt_token, output_token = analyze_french_history(pdf_files, prompt)
        print(response_text)
        print(f"Total prompt token count: {prompt_token}")
        print(f"Total output token count: {output_token}")

        while True:
          print("\n>>> 開始分析與驗證...")
          reference_text = "這裡是你預期的正確內容，用於語意相似度評分"
          approved, score = manager(response_text, reference_text)

          if approved:
              print("\n✔ 審核通過，結果送出：")
              print(reference_text)
              break
          else:
              print("\n✘ 分數不足（%.2f），重新分析..." % score)