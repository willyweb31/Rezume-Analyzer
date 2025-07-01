# Resume Analyzer

Resume Analyzer is a web application built with Flask that helps users optimize their resumes for specific job descriptions. Users can upload a PDF resume and paste a job description. The app will:

- Extract text from the uploaded PDF resume
- Compare keywords between the resume and the job description
- Use the OpenAI API (ChatGPT) to provide:
  - A match score (0–100)
  - Strengths
  - Weaknesses
  - Suggested bullet points to improve the resume

## Features
- PDF resume upload
- Job description input
- Keyword comparison
- AI-powered feedback
- Clean Bootstrap-styled UI

## Project Structure
```
Resume-Analyzer/
├── app.py
├── requirements.txt
├── .env
├── README.md
├── utils/
│   ├── pdf_parser.py
│   ├── keyword_matcher.py
│   └── openai_api.py
├── templates/
│   ├── index.html
│   └── result.html
└── static/
    └── style.css
```

## Setup Instructions
1. **Clone the repository**
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your OpenAI API key**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
5. **Run the app**
   ```bash
   flask run
   ```

## Notes
- Ensure your `.env` file is not committed to version control.
- The app uses Flask's secure file upload methods.
- Placeholder functions are provided for easy expansion.
# Rezume-Analyzer
