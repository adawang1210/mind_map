# pdf_processor.py
import os
import google.generativeai as genai

# 使用環境變數獲取 API 金鑰
gemini_key = "AIzaSyCVRn89Q4lURX5-Sy_Sdw-Ncv6zNEqbtEc"
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# 完整的 prompt
prompt = '''
你是一個法國歷史專家，我將提供一段關於法國歷史的文獻（可能是文本、摘要或 PDF 內容），你的任務是根據以下規範性框架分析並概括其內容，並將分析結果以指定的 JSON 格式輸出。如果文獻是法文，請直接根據法文分析並用中文回覆。以下是分析框架：

1. **主題和論點**
    - (1) 主題：文獻探討的主要主題是什麼？（例如：文明與文化、政治變革）
    - (2) 論點：作者的核心主張或觀點是什麼？（註明是否具爭議性）
    - (3) 事件：文獻提到的重大歷史事件有哪些？（包括名稱、時間點、類型）
2. **背景與時期**
    - (1) 背景：文獻涉及的歷史背景是什麼？（例如：社會環境、國際局勢）
    - (2) 時期：文獻涵蓋的具體歷史時期或年代是什麼？（例如：公元前58年至公元472年）
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
- 你的回答**必須**符合以下 格式：

const nodeData = {
  topic: '法國歷史分析',
  id: 'history_root_001',
  style: { fontSize: '32', color: '#2c3e50', background: '#ecf0f1' },
  expanded: true,
  parent: null,
  tags: ['歷史', '法國'],
  icons: ['📜'],
  children: [
    {
      topic: '主題與論點',
      id: 'themes_arguments_001',
      expanded: true,
      parent: 'history_root_001',
      children: [
        { topic: '主題', id: 'themes_001', parent: 'themes_arguments_001', children: [], tags: ['文明', '政治'] },
        { topic: '論點', id: 'arguments_001', parent: 'themes_arguments_001', children: [], hyperLink: '' },
        { topic: '事件', id: 'events_001', parent: 'themes_arguments_001', children: [], tags: ['革命', '戰爭'] }
      ]
    },
    {
      topic: '背景與時期',
      id: 'context_period_001',
      expanded: true,
      parent: 'history_root_001',
      children: [
        { topic: '背景', id: 'context_001', parent: 'context_period_001', children: [] },
        { topic: '時期', id: 'period_001', parent: 'context_period_001', children: [] }
      ]
    },
    {
      topic: '地點',
      id: 'location_001',
      expanded: true,
      parent: 'history_root_001',
      children: [
        { topic: '地理範圍', id: 'geography_001', parent: 'location_001', children: [], tags: ['高盧', '巴黎'] }
      ]
    },
    {
      topic: '人物',
      id: 'characters_001',
      expanded: true,
      parent: 'history_root_001',
      children: [
        {
          topic: '人物1',
          id: 'character_001',
          parent: 'characters_001',
          children: [
            { topic: '評價', id: 'eval_001', parent: 'character_001', children: [] },
            { topic: '姓名', id: 'name_001', parent: 'character_001', children: [] },
            { topic: '地位', id: 'status_001', parent: 'character_001', children: [] }
          ]
        }
      ]
    },
    {
      topic: '組織',
      id: 'organizations_001',
      expanded: true,
      parent: 'history_root_001',
      children: [], // 可動態添加具體組織
      tags: ['軍團', '政府']
    },
    {
      topic: '核心概念',
      id: 'concepts_001',
      expanded: true,
      parent: 'history_root_001',
      children: [], // 可動態添加概念
      tags: ['自由', '君主制']
    },
    {
      topic: '影響與意義',
      id: 'impact_significance_001',
      expanded: true,
      parent: 'history_root_001',
      children: [
        { topic: '短期影響', id: 'short_term_001', parent: 'impact_significance_001', children: [] },
        { topic: '長期意義', id: 'long_term_001', parent: 'impact_significance_001', children: [] }
      ]
    },
    {
      topic: '思維導圖建議',
      id: 'mind_map_suggestion_001',
      expanded: true,
      parent: 'history_root_001',
      children: [
        { topic: '主軸概念', id: 'theme_suggestion_001', parent: 'mind_map_suggestion_001', children: [] },
        { topic: '理由', id: 'reason_001', parent: 'mind_map_suggestion_001', children: [] }
      ]
    }
  ]
};

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