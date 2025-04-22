# pdf_processor.py
import os
import google.generativeai as genai

# 使用環境變數獲取 API 金鑰
gemini_key = "AIzaSyCVRn89Q4lURX5-Sy_Sdw-Ncv6zNEqbtEc"
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# 完整的 prompt
prompt = '''
你是一個法國歷史專家，我將提供一段關於法國歷史的文獻（可能是文本、摘要或 PDF 內容），你的任務是根據以下規範性框架分析並概括其內容，並將分析結果以指定的格式輸出。如果文獻是法文，請直接根據法文分析並用中文回覆。以下是分析框架：

1. **主題和論點**
    - (1) 主題：文獻探討的主要主題是什麼？（例如：文明與文化、政治變革）
    - (2) 論點：作者的核心主張或觀點是什麼？（註明是否具爭議性）
    - (3) 事件：文獻提到的重大歷史事件有哪些？（包括名稱、時間點、類型）
2. **背景與時期**
    - (1) 背景：文獻涉及的歷史背景是什麼？（例如：社會環境、國際局勢）
    - (2) 時期：文獻涵蓋的具體歷史時期或年代是什麼?（例如:公元前58年至公元472年）
3. **地點**
    - (1) 地理：文獻涉及的具體地點或地理範圍是什麼？（例如：高盧、萊茵河）
4. **人物**
    - (1) 情緒：僅根據文獻內容提取人物的情感、動機或歷史評價，不進行額外推測或主觀解讀，確保資訊直接來自文本。
    - (2) 名字：涉及哪些重要人物？（提供全名或稱號）
    - (3) 地位：這些人物的角色或權力地位是什麼？（例如：軍事領袖）
5. **組織（政治、軍事或社會團體）**
    - 文獻中提到的關鍵組織是什麼？（例如：羅馬軍團，註明類型與功能）
6. **涉及的核心概念（抽象名詞）**
    - 僅從文獻中提取最多三個原文提及的抽象概念（例如：自由、君主制），不額外推測或創造新概念，確保概念準確反映文獻內容。
7. **影響和意義**
    - 文獻描述的歷史發展對法國有什麼影響和意義？（分為短期影響、長期意義)

**請務必只回傳要求格式的內容，不要包含額外的文字描述。**

**輸出要求：**
- 你的回答**必須**符合以下 JSON 結構格式。
- 所有節點（包括根節點與所有子節點）**必須包含 `text` 欄位**，其內容需與節點功能或分類相對應，並用中文簡潔表達該節點的主題或內容（例如："歷史背景"、"核心論點"、"拿破崙的改革" 等）。

{
  "id": "history_root_001",
  "topic": "",
  "children": [
    {
      "id": "themes_arguments_001",
      "topic": "主題與論點",
      "children": [
        { "id": "themes_001", "topic": "主題" },
        { "id": "arguments_001", "topic": "論點" },
        { "id": "events_001", "topic": "重大事件" }
      ]
    },
    {
      "id": "context_period_001",
      "topic": "背景與時期",
      "children": [
        { "id": "context_001", "topic": "歷史背景" },
        { "id": "period_001", "topic": "歷史時期" }
      ]
    },
    {
      "id": "location_001",
      "topic": "地理位置",
      "children": [
        { "id": "geography_001", "topic": "具體地點" }
      ]
    },
    {
      "id": "characters_001",
      "topic": "重要人物",
      "children": [
        {
          "id": "character_001",
          "topic": "人物A",
          "children": [
            { "id": "eval_001", "topic": "情緒與評價" },
            { "id": "name_001", "topic": "姓名" },
            { "id": "status_001", "topic": "角色地位" }
          ]
        }
      ]
    },
    {
      "id": "organizations_001",
      "topic": "關鍵組織",
      "children": [
        {
          "id": "organization_001",
          "topic": "組織A",
          "children": [
            { "id": "eval_001", "topic": "歷史評價" },
            { "id": "name_001", "topic": "名稱" },
            { "id": "status_001", "topic": "功能或類型" }
          ]
        }
      ]
    },
    {
      "id": "concepts_001",
      "topic": "核心概念",
      "children": [
        { "id": "concept_001", "topic": "自由" },
        { "id": "concept_002", "topic": "君主制" },
        { "id": "concept_003", "topic": "民族認同" }
      ]
    },
    {
      "id": "impact_significance_001",
      "topic": "影響與意義",
      "children": [
        { "id": "short_term_001", "topic": "短期影響" },
        { "id": "long_term_001", "topic": "長期意義" }
      ]
    },
    {
      "id": "mind_map_suggestion_001",
      "topic": "心智圖建議",
      "children": [
        { "id": "theme_suggestion_001", "topic": "推薦主題" },
        { "id": "reason_001", "topic": "推薦理由" }
      ]
    }
  ]
}
'''

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

def get_pdf_files_from_uploads(upload_folder="uploads"):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    pdf_files = [os.path.join(upload_folder, f) for f in os.listdir(upload_folder) if f.endswith('.pdf')]
    return pdf_files

if __name__ == "__main__":
    pdf_files = get_pdf_files_from_uploads()
    if not pdf_files:
        print("uploads 資料夾中 PDF 檔案")
    else:
        response_text, prompt_token, output_token = analyze_french_history(pdf_files, prompt)
        print(response_text)
        print(f"Total prompt token count: {prompt_token}")
        print(f"Total output token count: {output_token}")