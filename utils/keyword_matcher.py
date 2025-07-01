import re
from collections import Counter

def extract_keywords(text, min_length=3):
    """
    Extract meaningful keywords from text using basic Python.
    Args:
        text (str): Input text to extract keywords from.
        min_length (int): Minimum length for keywords.
    Returns:
        list: List of keywords.
    """
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Remove stopwords and short words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
        'mine', 'yours', 'hers', 'ours', 'theirs', 'am', 'is', 'are', 'was', 'were',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'cannot', 'cant'
    }
    
    # Remove common words that aren't useful for job matching
    common_words = {
        'experience', 'work', 'job', 'position', 'role', 'team', 'company', 'business',
        'project', 'development', 'management', 'support', 'service', 'system',
        'technology', 'software', 'application', 'data', 'information', 'process',
        'analysis', 'design', 'implementation', 'testing', 'deployment', 'maintenance',
        'documentation', 'training', 'communication', 'collaboration', 'leadership',
        'problem', 'solution', 'improvement', 'optimization', 'efficiency', 'quality',
        'performance', 'security', 'reliability', 'scalability', 'integration',
        'responsibility', 'duties', 'requirements', 'skills', 'knowledge', 'ability',
        'experience', 'years', 'month', 'day', 'time', 'period', 'duration', 'level',
        'senior', 'junior', 'entry', 'mid', 'advanced', 'expert', 'beginner', 'intermediate'
    }
    
    keywords = []
    for word in words:
        if (len(word) >= min_length and 
            word not in stop_words and 
            word not in common_words and
            not word.isdigit()):
            keywords.append(word)
    
    return keywords

def get_keyword_frequency(keywords):
    """
    Get frequency of keywords.
    Args:
        keywords (list): List of keywords.
    Returns:
        Counter: Frequency counter of keywords.
    """
    return Counter(keywords)

def compare_keywords(resume_text, job_description):
    """
    Compares keywords between resume text and job description.
    Args:
        resume_text (str): Extracted resume text.
        job_description (str): Job description text.
    Returns:
        dict: Analysis with matched and missing keywords, scores, and recommendations.
    """
    # Extract keywords from both texts
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Get keyword frequencies
    resume_freq = get_keyword_frequency(resume_keywords)
    job_freq = get_keyword_frequency(job_keywords)
    
    # Find matched keywords (keywords that appear in both)
    matched_keywords = list(set(resume_keywords) & set(job_keywords))
    
    # Find missing keywords (keywords in job description but not in resume)
    missing_keywords = list(set(job_keywords) - set(resume_keywords))
    
    # Find extra keywords (keywords in resume but not in job description)
    extra_keywords = list(set(resume_keywords) - set(job_keywords))
    
    # Calculate match score
    total_job_keywords = len(set(job_keywords))
    if total_job_keywords > 0:
        match_score = (len(matched_keywords) / total_job_keywords) * 100
    else:
        match_score = 0
    
    # Get top missing keywords (most frequent in job description)
    top_missing = sorted(
        [(word, job_freq[word]) for word in missing_keywords],
        key=lambda x: x[1],
        reverse=True
    )[:10]  # Top 10 missing keywords
    
    # Get top matched keywords (most frequent in both)
    top_matched = sorted(
        [(word, min(resume_freq[word], job_freq[word])) for word in matched_keywords],
        key=lambda x: x[1],
        reverse=True
    )[:10]  # Top 10 matched keywords
    
    return {
        'match_score': round(match_score, 1),
        'matched_keywords': [word for word, _ in top_matched],
        'missing_keywords': [word for word, _ in top_missing],
        'extra_keywords': extra_keywords[:10],  # Top 10 extra keywords
        'total_job_keywords': total_job_keywords,
        'total_resume_keywords': len(set(resume_keywords)),
        'matched_count': len(matched_keywords),
        'missing_count': len(missing_keywords),
        'recommendations': generate_recommendations(match_score, missing_keywords[:5])
    }

def generate_recommendations(match_score, top_missing_keywords):
    """
    Generate recommendations based on match score and missing keywords.
    Args:
        match_score (float): Keyword match score.
        top_missing_keywords (list): Top missing keywords.
    Returns:
        list: List of recommendations.
    """
    recommendations = []
    
    if match_score < 30:
        recommendations.append("Your resume has very few keywords matching the job description. Consider adding more relevant skills and experiences.")
    elif match_score < 60:
        recommendations.append("Your resume has some matching keywords but could be improved. Focus on adding the most important missing keywords.")
    else:
        recommendations.append("Good keyword match! Your resume aligns well with the job requirements.")
    
    if top_missing_keywords:
        missing_str = ", ".join(top_missing_keywords[:3])
        recommendations.append(f"Consider adding these important keywords: {missing_str}")
    
    if match_score > 0:
        recommendations.append("Review your resume to ensure keywords are used naturally in context, not just listed.")
    
    return recommendations 