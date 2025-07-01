import openai
import json

def get_resume_feedback(resume_text, job_description, api_key):
    """
    Sends resume and job description to OpenAI API and returns feedback.
    Args:
        resume_text (str): Extracted resume text.
        job_description (str): Job description text.
        api_key (str): OpenAI API key.
    Returns:
        dict: Feedback with match score, strengths, weaknesses, suggestions.
    """
    
    max_resume_chars = 3000  # Limit resume text
    max_job_chars = 2500     # Limit job description
    
    if len(resume_text) > max_resume_chars:
        resume_text = resume_text[:max_resume_chars] + "..."
        print(f"Resume text truncated to {max_resume_chars} characters")
    
    if len(job_description) > max_job_chars:
        job_description = job_description[:max_job_chars] + "..."
        print(f"Job description truncated to {max_job_chars} characters")
    
    openai.api_key = api_key

    prompt = (
        "You are a professional resume reviewer. You MUST respond with valid JSON only.\n"
        "Given the following resume and job description, provide a detailed analysis and feedback on the resume.\n"
        "\n"
        "SCORING CRITERIA:\n"
        "- 90-100: Excellent match - resume perfectly aligns with job requirements\n"
        "- 80-89: Very good match - resume strongly matches job requirements\n"
        "- 70-79: Good match - resume generally matches job requirements\n"
        "- 60-69: Fair match - resume partially matches job requirements\n"
        "- 50-59: Poor match - resume has limited alignment with job requirements\n"
        "- 0-49: Very poor match - resume does not align with job requirements\n"
        "\n"
        "Your response must be a valid JSON object with exactly these keys:\n"
        "- match_score (number 0-100, based on alignment between resume and job description)\n"
        "- strengths (array of 3-5 specific strengths from the resume)\n"
        "- weaknesses (array of 3-5 specific weaknesses or gaps)\n"
        "- suggestions (array of exactly 3 specific improvement suggestions)\n"
        "\n"
        "CRITICAL: Your response must be valid JSON. Do not include any text before or after the JSON object.\n"
        "Do not use markdown formatting, code blocks, or any other formatting.\n"
        "Start your response with {{ and end with }} only.\n"
        "\n"
        "Example response format (copy this exact structure):\n"
        '{{\n'
        '  "match_score": 75,\n'
        '  "strengths": ["Strong Python programming skills", "Relevant Flask framework experience", "Database management expertise"],\n'
        '  "weaknesses": ["Missing cloud platform experience", "Limited team leadership examples", "No mention of API development"],\n'
        '  "suggestions": ["Add AWS or Azure cloud experience", "Include leadership and team collaboration examples", "Highlight API development and integration work"]\n'
        '}}\n'
        "\n"
        "Resume:\n{resume_text}\n\n"
        "Job Description:\n{job_description}\n"
        "\n"
        "IMPORTANT: Respond with ONLY the JSON object, no additional text, explanations, or markdown formatting."
    )
    
    # Format the prompt with actual data
    formatted_prompt = prompt.format(resume_text=resume_text, job_description=job_description)
    
    print(f"=== PROMPT DEBUG ===")
    print(f"Formatted prompt length: {len(formatted_prompt)}")
    print(f"Prompt preview (first 500 chars): {formatted_prompt[:500]}...")
    print(f"Prompt preview (last 200 chars): ...{formatted_prompt[-200:]}")
    print(f"=== END PROMPT DEBUG ===")
    
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model='gpt-4',  # Try GPT-4 for better JSON compliance
        messages=[
            {"role": 'system', "content": "You are a JSON-only response assistant. You must respond with valid JSON only, no other text."},
            {"role": 'user', "content": formatted_prompt}
        ],
        max_tokens=2000,
        temperature=0.1,  # Lower temperature for more consistent formatting
    )

    try:
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI response content is None")
        
        # Debug: print what we received
        print(f"OpenAI Response: {content}")
        print(f"Response length: {len(content)}")
        print(f"Response starts with: {content[:100]}")
        
        # Try to clean the response if it has extra text
        content = content.strip()
        
        # Remove markdown code blocks
        if content.startswith('```json'):
            content = content[7:]
        elif content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        print(f"Cleaned content: {content}")
        
        # Try to parse JSON with better error handling
        try:
            feedback = json.loads(content)
        except json.JSONDecodeError as json_error:
            print(f"JSON parsing failed: {json_error}")
            print(f"Attempting to fix malformed JSON...")
            
            # Try to extract JSON from the response
            import re
            
            # Method 1: Look for JSON-like structure with braces
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
            if json_match:
                try:
                    feedback = json.loads(json_match.group())
                    print("Successfully extracted JSON from response using method 1")
                except:
                    pass
            
            # Method 2: If method 1 failed, try to find the last JSON-like structure
            if 'feedback' not in locals() or not isinstance(feedback, dict):
                json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
                if json_matches:
                    for match in reversed(json_matches):  # Try the last match first
                        try:
                            feedback = json.loads(match)
                            print("Successfully extracted JSON from response using method 2")
                            break
                        except:
                            continue
            
            # Method 3: Try to manually construct JSON from common patterns
            if 'feedback' not in locals() or not isinstance(feedback, dict):
                print("Attempting manual JSON construction...")
                try:
                    # Look for match_score pattern
                    score_match = re.search(r'"match_score":\s*(\d+)', content)
                    score = int(score_match.group(1)) if score_match else 50
                    
                    # Look for strengths pattern
                    strengths_match = re.search(r'"strengths":\s*\[(.*?)\]', content, re.DOTALL)
                    strengths = []
                    if strengths_match:
                        strengths_text = strengths_match.group(1)
                        strengths = [s.strip().strip('"') for s in strengths_text.split(',') if s.strip()]
                    
                    # Look for weaknesses pattern
                    weaknesses_match = re.search(r'"weaknesses":\s*\[(.*?)\]', content, re.DOTALL)
                    weaknesses = []
                    if weaknesses_match:
                        weaknesses_text = weaknesses_match.group(1)
                        weaknesses = [s.strip().strip('"') for s in weaknesses_text.split(',') if s.strip()]
                    
                    # Look for suggestions pattern
                    suggestions_match = re.search(r'"suggestions":\s*\[(.*?)\]', content, re.DOTALL)
                    suggestions = []
                    if suggestions_match:
                        suggestions_text = suggestions_match.group(1)
                        suggestions = [s.strip().strip('"') for s in suggestions_text.split(',') if s.strip()]
                    
                    feedback = {
                        "match_score": score,
                        "strengths": strengths if strengths else ["Unable to parse strengths"],
                        "weaknesses": weaknesses if weaknesses else ["Unable to parse weaknesses"],
                        "suggestions": suggestions if suggestions else ["Unable to parse suggestions"]
                    }
                    print("Successfully constructed JSON manually")
                except Exception as manual_error:
                    print(f"Manual construction failed: {manual_error}")
            
            # If all methods failed, create a fallback response
            if 'feedback' not in locals() or not isinstance(feedback, dict):
                print("Creating fallback response due to JSON parsing failure")
                feedback = {
                    "match_score": 50,
                    "strengths": ["Unable to parse AI response"],
                    "weaknesses": ["Response format error"],
                    "suggestions": ["Please try again with different input"]
                }
        
        print(f"Parsed feedback: {feedback}")
        print(f"Match score: {feedback.get('match_score', 'NOT FOUND')}")
        
        return feedback
    except Exception as e:
        print(f"Error parsing OpenAI response: {e}")
        print(f"Raw response: {response.choices[0].message.content if response.choices[0].message.content else 'None'}")
        return {
            "match_score": 0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [f"Error parsing OpenAI response: {e}"]
        }
