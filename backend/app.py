# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
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

@app.route('/')
def index():
    logger.info("Root path request received")
    return jsonify({
        "status": "success",
        "message": "Backend API is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/upload', methods=['POST'])
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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            logger.info(f"PDF file received and saved successfully: {file.filename}")
            
            pdf_files = [filepath]
            logger.info(f"Starting analysis of PDF file: {file.filename}")
            
            # Initial AI analysis
            response_text, prompt_token, output_token = analyze_french_history(pdf_files, prompt)
            logger.info(f"PDF initial analysis completed - Prompt tokens: {prompt_token}, Output tokens: {output_token}")
            
            # Initialize the Manager Agent with max 3 attempts
            logger.info("Starting multi-agent validation process")
            manager_agent = ManagerAgent(max_attempts=3)
            validation_result, final_text = manager_agent.process(response_text, REFERENCE_TEXT, pdf_files, prompt)
            
            # Log and return the comprehensive results
            logger.info(f"Validation process completed - Status: {validation_result['final_status']}")
            logger.info(f"Total validation attempts: {validation_result['attempts']}")
            logger.info(f"Final average validation score: {validation_result['average_score']:.2f}%")
            
            # Collect the individual agent scores for the response
            semantic_score = validation_result['detailed_results']['semantic']['score']
            factual_score = validation_result['detailed_results']['factual']['score']
            qa_score = validation_result['detailed_results']['qa']['score']
            
            return jsonify({
                'message': 'PDF uploaded and analyzed successfully',
                'filename': file.filename,
                'analysis_result': final_text,
                'prompt_token': prompt_token,
                'output_token': output_token,
                'validation': {
                    'status': validation_result['final_status'],
                    'attempts': validation_result['attempts'],
                    'average_score': validation_result['average_score'],
                    'agent_scores': {
                        'semantic_validation': semantic_score,
                        'factual_validation': factual_score,
                        'qa_validation': qa_score
                    }
                }
            }), 200
            
        except Exception as e:
            logger.error(f"PDF processing failed: {str(e)}", exc_info=True)
            return jsonify({'error': f'Failed to process PDF: {str(e)}'}), 500
    else:
        logger.warning(f"Invalid file format received: {file.filename}")
        return jsonify({'error': 'Invalid file format. Please upload a PDF'}), 400

if __name__ == '__main__':
    logger.info("Starting Flask application server...")
    app.run(host='127.0.0.1', port=5000, debug=True)