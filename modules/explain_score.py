from openai import OpenAI

def explain_cv_score(
    full_text_similarity,
    skill_similarity,
    title_similarity,
    experience_similarity,
    cv_skills,
    jd_skills
):
    client = OpenAI(api_key="xxx")

    system_prompt = """You are a recruitment assistant. 
You receive a candidate CV and a job description.
Your task is to explain — in a clear and concise way — why the CV received a certain score compared to the job description.
You will be given several similarity scores (from 0 to 1) and extracted skills from both documents.
Structure your response in 2-3 paragraphs with professional language.
Do not return JSON or a list. Return a natural explanation."""

    user_prompt = f"""

Similarity Scores:
- Full Text Similarity: {full_text_similarity}
- Skill Similarity: {skill_similarity}
- Title Similarity: {title_similarity}
- Experience Similarity: {experience_similarity}

Extracted Skills:
- Job Description Skills: {", ".join(jd_skills)}
- CV Skills: {", ".join(cv_skills)}

Please explain why the CV received this score based on the job description and scores above.
"""

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"
def Explanationpdf(full_text_similarity,
    skill_similarity,
    title_similarity,
    experience_similarity,
    cv_skills,
    jd_skills):
    explanation=explain_cv_score(full_text_similarity,skill_similarity,title_similarity,experience_similarity,cv_skills,jd_skills)
    savetopdf(explanation,"explanation.txt")
    
    
