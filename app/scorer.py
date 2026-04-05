from app.utils import extract_keywords
from app.constants import ROLE_SKILLS, DOMAIN_KEYWORDS


def keyword_score(role, job_desc, resume):

    role_keywords = set(ROLE_SKILLS.get(role, []))
    domain_keywords = set(DOMAIN_KEYWORDS.get(role, []))

    allowed_keywords = role_keywords.union(domain_keywords)

    job_keywords = extract_keywords(job_desc, role) & allowed_keywords
    resume_keywords = extract_keywords(resume, role) & allowed_keywords

    matched = job_keywords & resume_keywords

    if len(job_keywords) == 0:
        return 0, [], []

    score = (len(matched) / len(job_keywords)) * 100

    missing = job_keywords - resume_keywords

    return score, list(matched), list(missing)


def skills_score(role, resume):
    required_skills = ROLE_SKILLS.get(role, [])
    resume_keywords = extract_keywords(resume, role)

    if not required_skills:
        return 50

    matched = set(required_skills) & set(resume_keywords)

    return (len(matched) / len(required_skills)) * 100


def experience_score(resume):
    resume = resume.lower()

    if "3 years" in resume or "4 years" in resume or "5 years" in resume:
        return 100
    elif "1 year" in resume or "2 years" in resume:
        return 70
    else:
        return 40


def format_score(resume):
    score = 0
    resume = resume.lower()

    if "education" in resume:
        score += 25
    if "experience" in resume:
        score += 25
    if "skills" in resume:
        score += 25
    if "project" in resume:
        score += 25

    return score


def final_score(K, S, E, F):
    raw_score = 0.5*K + 0.2*S + 0.2*E + 0.1*F

    score = raw_score

    if score > 92:
        score = 92 + (score - 92) * 0.3  # soft cap

    return int(round(raw_score)), int(round(score))