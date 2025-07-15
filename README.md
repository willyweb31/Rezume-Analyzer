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


## Notes
- Ensure your `.env` file is not committed to version control.
- The app uses Flask's secure file upload methods.
- Placeholder functions are provided for easy expansion.
# Rezume-Analyzer
