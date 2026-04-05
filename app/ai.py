import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_suggestions(resume_text, job_description, missing_keywords):

    prompt = f"""
You are an ATS resume expert.

Resume:
{resume_text}

Job Description:
{job_description}

Missing Keywords:
{missing_keywords}

Give 3-5 short, actionable suggestions to improve the resume.
Return ONLY bullet points.
Keep it concise and professional.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )

    text = response.choices[0].message.content.strip()

    # convert bullet text → list
    suggestions = [
    s.strip("- ").strip().replace('"', '')
    for s in text.split("\n")
    if s.strip()
    ]

    return suggestions