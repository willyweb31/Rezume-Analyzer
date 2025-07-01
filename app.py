import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from utils.pdf_parser import extract_text_from_pdf
from utils.keyword_matcher import compare_keywords
from utils.openai_api import get_resume_feedback

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey' 

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get resume text from either PDF or text input
        resume_text = ""
        
        # Check if PDF file was uploaded
        if 'resume' in request.files and request.files['resume'].filename != '':
            file = request.files['resume']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                resume_text = extract_text_from_pdf(filepath)
            else:
                flash('Allowed file type is PDF')
                return redirect(request.url)
        
        # Check if resume text was pasted
        elif 'resume_text' in request.form and request.form['resume_text'].strip():
            resume_text = request.form['resume_text'].strip()
        
        # If neither PDF nor text provided
        if not resume_text:
            flash('Please either upload a PDF or paste your resume text')
            return redirect(request.url)
        
        # Get job description
        job_description = request.form.get('job_description', '')
        if not job_description.strip():
            flash('Please provide a job description')
            return redirect(request.url)
        
        print(f"=== RESUME TEXT DEBUG ===")
        print(f"Resume text extracted: {len(resume_text) if resume_text else 0} characters")
        print(f"Resume text preview: {resume_text[:300] if resume_text else 'EMPTY'}")
        print(f"Job description: {job_description[:200] if job_description else 'EMPTY'}")
        print(f"=== END DEBUG ===")
        
        # Compare keywords
        keyword_result = compare_keywords(resume_text, job_description)
        
        # Get AI feedback
        print(f"=== CALLING OPENAI API ===")
        print(f"About to call get_resume_feedback with:")
        print(f"  - Resume text length: {len(resume_text)}")
        print(f"  - Job description length: {len(job_description)}")
        print(f"  - API key present: {'Yes' if OPENAI_API_KEY else 'No'}")
        
        feedback = get_resume_feedback(resume_text, job_description, OPENAI_API_KEY)
        
        print(f"=== OPENAI API CALL COMPLETED ===")
        print(f"Feedback received: {feedback}")
        return render_template('result.html',
                               keyword_result=keyword_result,
                               feedback=feedback)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 