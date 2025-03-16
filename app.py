from flask import Flask, request, jsonify, send_from_directory
from document_processor import DocumentProcessor
import os
import logging
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
processor = DocumentProcessor()

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    """Create upload folder if it doesn't exist"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    try:
        return app.send_static_file('index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_documents():
    try:
        ensure_upload_folder()

        # Check if files are present in request
        if 'resume' not in request.files or 'requirements' not in request.files:
            return jsonify({'error': 'Both resume and requirements files are required'}), 400

        resume_file = request.files['resume']
        requirements_file = request.files['requirements']

        # Validate file names
        if resume_file.filename == '' or requirements_file.filename == '':
            return jsonify({'error': 'No selected files'}), 400

        # Validate file extensions
        if not (allowed_file(resume_file.filename) and allowed_file(requirements_file.filename)):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed'}), 400

        # Secure the filenames
        resume_filename = secure_filename(resume_file.filename)
        requirements_filename = secure_filename(requirements_file.filename)

        # Create temporary file paths
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_resume_{resume_filename}')
        requirements_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_requirements_{requirements_filename}')

        try:
            # Save files
            resume_file.save(resume_path)
            requirements_file.save(requirements_path)

            logger.info(f"Processing resume: {resume_filename}")
            logger.info(f"Processing requirements: {requirements_filename}")

            # Process files based on their extension
            resume_text = (processor.read_pdf(resume_path) 
                         if resume_path.lower().endswith('.pdf') 
                         else processor.read_docx(resume_path))

            requirements_text = (processor.read_pdf(requirements_path) 
                              if requirements_path.lower().endswith('.pdf') 
                              else processor.read_docx(requirements_path))

            if not resume_text or not requirements_text:
                return jsonify({'error': 'Failed to extract text from files'}), 400

            # Calculate match
            results = processor.calculate_match(resume_text, requirements_text)
            
            # Add file names to results
            results['resume_filename'] = resume_filename
            results['requirements_filename'] = requirements_filename

            return jsonify(results)

        except Exception as e:
            logger.error(f"Error processing files: {str(e)}")
            return jsonify({'error': f'Error processing files: {str(e)}'}), 500

        finally:
            # Clean up temporary files
            for file_path in [resume_path, requirements_path]:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    logger.error(f"Error removing temporary file {file_path}: {str(e)}")

    except Exception as e:
        logger.error(f"Error in analyze_documents: {str(e)}")
        return jsonify({'error': str(e)}), 500

def create_static_folder():
    """Create static folder if it doesn't exist"""
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
        # Move index.html to static folder if it's in the root
        root_index = os.path.join(os.path.dirname(__file__), 'index.html')
        if os.path.exists(root_index):
            static_index = os.path.join(static_folder, 'index.html')
            os.rename(root_index, static_index)

if __name__ == '__main__':
    try:
        create_static_folder()
        ensure_upload_folder()
        logger.info("Starting server on port 8000...")
        from waitress import serve
        serve(app, host='localhost', port=8000)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")