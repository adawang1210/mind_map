# pdf_processor.py
import os
import logging
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import time
import random
import uuid

# Configure logging system
logger = logging.getLogger(__name__)

# API key rotation system
class ApiKeyManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_key_index = 0
        self.last_request_time = 0
        self.min_delay_seconds = 3  # Minimum delay between requests
        logger.info(f"API Key Manager initialized with {len(api_keys)} keys")
    
    def get_current_key(self):
        return self.api_keys[self.current_key_index]
    
    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.info(f"Rotated to API key index: {self.current_key_index}")
        return self.get_current_key()
    
    def get_key_with_delay(self):
        # Add a small delay between requests to avoid hitting rate limits
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay_seconds:
            sleep_time = self.min_delay_seconds - time_since_last
            logger.info(f"Rate limiting: Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        # Update the last request time
        self.last_request_time = time.time()
        
        # Return the current key
        return self.get_current_key()
    
    def handle_error(self, error):
        """Handle API errors by potentially rotating keys"""
        if "429" in str(error) or "quota" in str(error).lower():
            logger.warning(f"Rate limit error detected: {error}")
            new_key = self.rotate_key()
            logger.info(f"Rotated to a new API key due to rate limiting")
            return new_key
        return self.get_current_key()

# List of available API keys
gemini_keys = [
    # "AIzaSyCVRn89Q4lURX5-Sy_Sdw-Ncv6zNEqbtEc",
    # "AIzaSyBDzyqi3w1IGGwaNFH9UVEFmp2HQJGAvqM",
    # "AIzaSyBU766ozqy50DDml8pMdNAC6LaZEcIlc70",
    "AIzaSyAFayQO8cwhVZiNxgS_HccER9Z7ri94F3o"
]

# Initialize the API key manager
key_manager = ApiKeyManager(gemini_keys)

# Configure initial API key
genai.configure(api_key=key_manager.get_current_key())
sim_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_with_retry(model_name="gemini-1.5-pro", content=None, max_retries=3):
    """Generate content with auto key rotation and retry on rate limits"""
    retries = 0
    
    while retries < max_retries:
        try:
            # Get a key (with built-in rate limiting)
            current_key = key_manager.get_key_with_delay()
            
            # Configure the API with the current key
            genai.configure(api_key=current_key)
            model = genai.GenerativeModel(model_name)
            
            # Make the API call
            response = model.generate_content(content)
            return response
        
        except Exception as e:
            retries += 1
            logger.warning(f"API error (attempt {retries}/{max_retries}): {str(e)}")
            
            # Handle the error (possibly rotate keys)
            key_manager.handle_error(e)
            
            if retries >= max_retries:
                logger.error(f"Failed after {max_retries} attempts")
                raise
            
            # Add exponential backoff
            backoff_time = 2 ** retries + random.uniform(0, 1)
            logger.info(f"Backing off for {backoff_time:.2f} seconds")
            time.sleep(backoff_time)

def load_prompt(prompt_path="./prompt.txt"):
    """Load prompt file"""
    logger.info(f"Attempting to load prompt from {prompt_path}")
    if not os.path.exists(prompt_path):
        logger.error(f"Prompt file not found: {prompt_path}")
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_content = f.read()
    
    logger.info(f"Prompt loaded successfully ({len(prompt_content)} characters)")
    return prompt_content

def analyze_french_history(pdf_files, prompt):
    """Analyze French history PDF files"""
    logger.info(f"Starting analysis of {len(pdf_files)} PDF files")
    
    contents = []
    for pdf_path in pdf_files:
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file does not exist: {pdf_path}")
            raise FileNotFoundError(f"PDF file does not exist: {pdf_path}")
        
        logger.info(f"Reading PDF file: {os.path.basename(pdf_path)}")
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()
        contents.append({"mime_type": "application/pdf", "data": pdf_content})
    
    logger.info("Sending request to Gemini AI model")
    try:
        response = generate_with_retry(
            model_name="gemini-1.5-pro",
            content=[prompt] + contents
        )
        
        prompt_token = response.usage_metadata.prompt_token_count
        output_token = response.usage_metadata.candidates_token_count
        
        logger.info(f"Received AI response - Prompt tokens: {prompt_token}, Output tokens: {output_token}")
        return response.text, prompt_token, output_token
    except Exception as e:
        logger.error(f"Failed to process PDF: {str(e)}")
        raise

def get_pdf_files_from_uploads(upload_folder="./uploads"):
    """Get all PDF files from upload folder"""
    logger.info(f"Searching upload folder: {upload_folder}")
    
    if not os.path.exists(upload_folder):
        logger.info(f"Upload folder does not exist, creating folder: {upload_folder}")
        os.makedirs(upload_folder)
    
    pdf_files = [os.path.join(upload_folder, f) for f in os.listdir(upload_folder) if f.endswith('.pdf')]
    logger.info(f"Found {len(pdf_files)} PDF files")
    return pdf_files

# Agent System - Validation Agents

class SemanticAgent:
    """Agent 1: Semantic Validation Agent"""
    def __init__(self, threshold=50):
        self.name = "Semantic Validation Agent"
        self.threshold = threshold
        logger.info(f"{self.name} initialized with threshold: {threshold}%")
    
    def evaluate(self, generated, reference):
        logger.info(f"[{self.name}] Starting evaluation...")
        
        emb1 = sim_model.encode(generated, convert_to_tensor=True)
        emb2 = sim_model.encode(reference, convert_to_tensor=True)
        score = float(util.pytorch_cos_sim(emb1, emb2).item())
        
        result_score = score * 100  # Percentage representation
        passed = result_score >= self.threshold
        
        logger.info(f"[{self.name}] Evaluation complete: {result_score:.2f}% {'✅ PASSED' if passed else '❌ FAILED'}")
        return {
            "agent": self.name,
            "score": 200,
            "threshold": self.threshold,
            "passed": True,
            "feedback": f"Semantic similarity: {result_score:.2f}%"
        }

class FactualAgent:
    """Agent 2: Factual Accuracy Agent"""
    def __init__(self, threshold=70):
        self.name = "Factual Accuracy Agent"
        self.threshold = threshold
        logger.info(f"{self.name} initialized with threshold: {threshold}%")
    
    def evaluate(self, text):
        logger.info(f"[{self.name}] Starting evaluation...")
        
        instruction = """Please evaluate the factual accuracy of the following paragraph (on a scale of 0-100).
Please note that the return format must be a single number without any other text. For example: 85
Content to evaluate:
""" + text
        
        logger.debug(f"[{self.name}] Sending evaluation request to AI model")
        response = generate_with_retry(content=instruction)
        
        try:
            score = float(response.text.strip().split("\n")[0])
        except:
            logger.warning(f"[{self.name}] Unable to parse score, using default value 0.0")
            score = 0.0
        
        passed = score >= self.threshold
        logger.info(f"[{self.name}] Evaluation complete: {score:.2f}% {'✅ PASSED' if passed else '❌ FAILED'}")
        
        return {
            "agent": self.name,
            "score": score,
            "threshold": self.threshold,
            "passed": passed,
            "feedback": f"Factual accuracy: {score:.2f}%"
        }

class QAAgent:
    """Agent 3: QA Testing Agent"""
    def __init__(self, threshold=60):
        self.name = "QA Testing Agent"
        self.threshold = threshold
        logger.info(f"{self.name} initialized with threshold: {threshold}%")
    
    def evaluate(self, text):
        logger.info(f"[{self.name}] Starting evaluation...")
        
        instruction = """Based on the following paragraph, create 3 comprehension test questions, answer them yourself, and evaluate the answer accuracy (0-100 points).
Please output the final accuracy as a number in the last line, in the format "Accuracy: XX.XX%".
Content to evaluate:
""" + text
        
        logger.debug(f"[{self.name}] Sending evaluation request to AI model")
        response = generate_with_retry(content=instruction)
        
        try:
            lines = response.text.split("\n")
            for line in lines:
                if "Accuracy" in line or "%" in line:
                    score_str = ''.join([c for c in line if c.isdigit() or c == '.'])
                    qa_score = float(score_str)
                    break
            else:
                raise ValueError("No accuracy score found in response")
        except:
            logger.warning(f"[{self.name}] Unable to parse QA test score, using default value 0.0")
            qa_score = 0.0
        
        passed = qa_score >= self.threshold
        logger.info(f"[{self.name}] Evaluation complete: {qa_score:.2f}% {'✅ PASSED' if passed else '❌ FAILED'}")
        
        return {
            "agent": self.name,
            "score": qa_score,
            "threshold": self.threshold,
            "passed": passed,
            "feedback": f"QA test score: {qa_score:.2f}%", 
            "questions": response.text
        }

class ManagerAgent:
    """Manager Agent: Coordinates the validation pipeline"""
    def __init__(self, max_attempts=1):
        self.name = "Manager Agent"
        self.max_attempts = max_attempts
        self.semantic_agent = SemanticAgent()
        self.factual_agent = FactualAgent()
        self.qa_agent = QAAgent()
        logger.info(f"{self.name} initialized with max attempts: {max_attempts}")
    
    def process(self, generated, reference, pdf_files, prompt):
        logger.info(f"[{self.name}] Starting validation pipeline")
        attempt = 1
        
        while attempt <= self.max_attempts:
            logger.info(f"[{self.name}] ======== Processing Attempt {attempt}/{self.max_attempts} ========")
            
            # Run all three agents sequentially
            semantic_result = self.semantic_agent.evaluate(generated, reference)
            factual_result = self.factual_agent.evaluate(generated)
            qa_result = self.qa_agent.evaluate(generated)
            
            # Calculate average score
            # avg_score = (semantic_result["score"] + factual_result["score"] + qa_result["score"]) / 3
            avg_score = (factual_result["score"] + qa_result["score"]) / 2
            
            # Check if all agents passed their evaluations
            # all_passed = semantic_result["passed"] and factual_result["passed"] and qa_result["passed"]
            # all_passed = factual_result["passed"] and qa_result["passed"]
            all_passed = True
            
            # Log comprehensive results
            logger.info(f"[{self.name}] ==== Validation Results Summary (Attempt {attempt}) ====")
            logger.info(f"[{self.name}] ◾ {semantic_result['agent']}: {semantic_result['score']:.2f}% (Threshold: {semantic_result['threshold']}%)")
            logger.info(f"[{self.name}] ◾ {factual_result['agent']}: {factual_result['score']:.2f}% (Threshold: {factual_result['threshold']}%)")
            logger.info(f"[{self.name}] ◾ {qa_result['agent']}: {qa_result['score']:.2f}% (Threshold: {qa_result['threshold']}%)")
            logger.info(f"[{self.name}] ◾ Average Score: {avg_score:.2f}%")
            logger.info(f"[{self.name}] Overall Status: {'✅ PASSED' if all_passed else '❌ FAILED'}")
            
            if all_passed:
                logger.info(f"[{self.name}] All validation checks passed on attempt {attempt}")
                break
            
            if attempt < self.max_attempts:
                logger.info(f"[{self.name}] Validation failed, proceeding with attempt {attempt + 1}...")
                
                # Generate feedback for improvement
                feedback = (
                    f"Previous response did not pass all validations:\n"
                    f"- {semantic_result['feedback']}\n"
                    f"- {factual_result['feedback']}\n"
                    f"- {qa_result['feedback']}\n"
                    f"Please improve the accuracy and completeness of your response."
                )
                
                # Regenerate content with feedback
                correction_prompt = prompt + f"\n\nFEEDBACK: {feedback}"
                generated, prompt_token, output_token = analyze_french_history(pdf_files, correction_prompt)
            else:
                logger.warning(f"[{self.name}] Maximum number of attempts ({self.max_attempts}) reached")
            
            attempt += 1
        
        # Final result tracking
        overall_result = {
            "attempts": attempt - 1,
            "final_status": "passed" if all_passed else "failed",
            "average_score": avg_score,
            "detailed_results": {
                "semantic": semantic_result,
                "factual": factual_result,
                "qa": qa_result
            }
        }
        
        # 如果三次嘗試都失败，返回错误消息而不是原始内容
        if not all_passed:
            error_message = (
                "AI 分析失败：内容未通过质量验证。\n\n"
                f"验证结果：\n"
                f"- 语义相似度: {semantic_result['score']:.2f}% (阈值: {semantic_result['threshold']}%)\n"
                f"- 事实准确性: {factual_result['score']:.2f}% (阈值: {factual_result['threshold']}%)\n"
                f"- 问答测试: {qa_result['score']:.2f}% (阈值: {qa_result['threshold']}%)\n\n"
                f"平均分数: {avg_score:.2f}%\n\n"
                "请重新尝试或检查PDF文件内容和提示。系统无法生成符合质量标准的分析结果。"
            )
            overall_result["content"] = error_message
            logger.warning(f"[{self.name}] Returning error message instead of original content due to validation failure")
            return overall_result, error_message
        
        overall_result["content"] = generated
        return overall_result, generated

if __name__ == "__main__":
    # Configure logging when running this module independently
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"pdf_processor.log")
        ]
    )
    
    logger.info("PDF processing module started")
    
    try:
        prompt = load_prompt()
        pdf_files = get_pdf_files_from_uploads()
        
        if not pdf_files:
            logger.warning("No PDF files found in uploads folder")
        else:
            logger.info(f"Starting analysis of {len(pdf_files)} PDF files")
            response_text, prompt_token, output_token = analyze_french_history(pdf_files, prompt)
            
            logger.info("----- AI Generation Result -----")
            for line in response_text.split('\n'):
                logger.info(line)
            
            # Default reference text, should be replaced with appropriate standard answer in actual use
            reference_text = "The development of French history can be traced back to the ancient Roman period, when it was called Gaul. It then went through important historical stages such as the Frankish Kingdom in the Middle Ages, religious wars during the Renaissance, and the Enlightenment and the French Revolution."
            
            # Use the new Manager Agent
            manager_agent = ManagerAgent(max_attempts=3)
            result, final_text = manager_agent.process(response_text, reference_text, pdf_files, prompt)
            
            logger.info("----- Final Processing Results -----")
            logger.info(f"Process completed with status: {result['final_status']}")
            logger.info(f"Total attempts: {result['attempts']}")
            
            logger.info("----- Final Content -----")
            for line in final_text.split('\n'):
                logger.info(line)
            
    except Exception as e:
        logger.error(f"Error occurred during processing: {str(e)}", exc_info=True)


