# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import uuid
import time
from datetime import datetime
from pdf_processor import analyze_french_history, load_prompt, ManagerAgent

# Configure logging system
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_filename = os.path.join(log_folder, f"backend_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler(log_filename, encoding='utf-8')  # Also save to log file
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload file size to 16MB

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logger.info(f"Created upload folder: {UPLOAD_FOLDER}")

# In-memory task storage (in production, use a database)
tasks = {}

# Load prompt
try:
    prompt = load_prompt()
    logger.info("Analysis prompt loaded successfully")
except Exception as e:
    logger.error(f"Failed to load prompt: {str(e)}")
    prompt = None

# Default reference text for validation
REFERENCE_TEXT = """The development of French history can be traced back to the ancient Roman period, 
when it was called Gaul. It then went through important historical stages such as the Frankish Kingdom 
in the Middle Ages, religious wars during the Renaissance, and the Enlightenment and the French Revolution."""

# 測試用
@app.route('/')
def index():
    logger.info("Root path request received")
    return jsonify({
        "status": "success",
        "message": "Backend API is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

# 上傳PDF檔案
@app.route('/api/upload', methods=['POST'])
def upload_file():
    logger.info("File upload request received")
    
    # Check if request contains file
    if 'file' not in request.files:
        logger.warning("Upload request does not contain file")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.warning("Uploaded file name is empty")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        try:
            # Generate a UUID for the task
            task_id = str(uuid.uuid4())
            
            # Save the file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            logger.info(f"PDF file received and saved successfully: {file.filename}")
            
            # Create task entry
            tasks[task_id] = {
                "id": task_id,
                "status": "processing",
                "progress": 0,
                "filename": file.filename,
                "filepath": filepath,
                "created_at": int(time.time()),
                "result": None
            }
            
            # Start processing in a background thread (in production use Celery/Redis)
            import threading
            thread = threading.Thread(
                target=process_pdf_task,
                args=(task_id, filepath, file.filename)
            )
            thread.daemon = True
            thread.start()
            
            return jsonify({
                "message": "file upload successfully",
                "taskid": task_id
            }), 200
            
        except Exception as e:
            logger.error(f"PDF upload failed: {str(e)}", exc_info=True)
            return jsonify({'error': f'Failed to process PDF: {str(e)}'}), 500
    else:
        logger.warning(f"Invalid file format received: {file.filename}")
        return jsonify({'error': 'Invalid file format. Please upload a PDF'}), 400

def process_pdf_task(task_id, filepath, filename):
    """Process PDF file in background thread"""
    try:
        logger.info(f"Starting background task {task_id} for file {filename}")
        
        # Update task progress
        tasks[task_id]["progress"] = 20
        
        # Process the PDF file
        pdf_files = [filepath]
        response_text, prompt_token, output_token = analyze_french_history(pdf_files, prompt)
        
        # Update task progress
        tasks[task_id]["progress"] = 60
        
        # Initialize the Manager Agent with max 3 attempts
        logger.info("Starting multi-agent validation process")
        manager_agent = ManagerAgent(max_attempts=3)
        validation_result, final_text = manager_agent.process(response_text, REFERENCE_TEXT, pdf_files, prompt)
        
        # Extract validation details
        semantic_result = validation_result['detailed_results']['semantic']
        factual_result = validation_result['detailed_results']['factual']
        qa_result = validation_result['detailed_results']['qa']
        
        # Update task with results
        tasks[task_id].update({
            "status": "completed",
            "progress": 100,
            "result": {
                "text": final_text,
                "validation_result": {
                    "attempts": validation_result["attempts"],
                    "final_status": validation_result["final_status"],
                    "average_score": round(validation_result["average_score"], 2),
                    "detailed_results": {
                        "semantic_result": round(semantic_result["score"], 2),
                        "factual_result": round(factual_result["score"], 2),
                        "qa_result": round(qa_result["score"], 2),
                        "semantic_isPassed": semantic_result["passed"],
                        "factual_isPassed": factual_result["passed"],
                        "qa_isPassed": qa_result["passed"]
                    }
                },
                "tokens": {
                    "prompt": prompt_token,
                    "output": output_token
                }
            }
        })
        
        logger.info(f"Task {task_id} completed successfully")
    
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}", exc_info=True)
        tasks[task_id].update({
            "status": "failed",
            "progress": 100,
            "error": str(e)
        })

# 取得任務狀態
@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    logger.info(f"Task status request received for task ID: {task_id}")
    
    if task_id not in tasks:
        logger.warning(f"Task ID not found: {task_id}")
        return jsonify({'error': 'Task not found'}), 404
    
    task = tasks[task_id]
    
    # Return different response formats based on task status
    if task["status"] in ["processing", "failed"]:
        return jsonify({
            "id": task["id"],
            "status": task["status"],
            "progress": task["progress"],
            "filename": task["filename"],
            "created_at": task["created_at"]
        })
    else:  # completed
        return jsonify({
            "id": task["id"],
            "status": task["status"],
            "progress": task["progress"],
            "filename": task["filename"],
            "created_at": task["created_at"],
            "result": task["result"]
        })


if __name__ == '__main__':
    logger.info("Starting Flask application server...")
    app.run(host='127.0.0.1', port=5000, debug=True)