from fastapi import FastAPI, Request, HTTPException
from app.models import ResumeInput
from app.scorer import (
    keyword_score,
    skills_score,
    experience_score,
    format_score,
    final_score
)
from app.ai import generate_ai_suggestions
import os
from fastapi.responses import JSONResponse


app = FastAPI(title="ATS Resume Scoring API",docs_url=None,
    redoc_url=None)




@app.middleware("http")
async def check_rapidapi(request: Request, call_next):

    # allow root
    if request.url.path == "/":
        return await call_next(request)

    # block non-RapidAPI requests
    if not request.headers.get("x-rapidapi-host"):
        return JSONResponse(
            status_code=403,
            content={"detail": "Direct access forbidden"}
        )

    return await call_next(request)


@app.get("/")
def home():
    return {"message": "ATS Resume API is running"}


@app.post("/ats-score")
def ats_score(data: ResumeInput):
    K, matched, missing = keyword_score(
    data.role,
    data.job_description,
    data.resume_text
)

    S = skills_score(data.role, data.resume_text)
    E = experience_score(data.resume_text)
    F = format_score(data.resume_text)

    raw_score, score = final_score(K, S, E, F)
    suggestions = generate_ai_suggestions(
    data.resume_text,
    data.job_description,
    missing
)

    return {
         "raw_score": int(round(raw_score)),
    "ats_score": int(round(score)),
    "suggestions": suggestions,
    "note": "Score is normalized to reflect real-world ATS behavior",
    "breakdown": {
        "keyword_match": int(round(K)),
        "skills_match": int(round(S)),
        "experience_match": int(round(E)),
        "format_score": int(round(F))
    },
    "matched_keywords": sorted([k for k in matched if len(k) > 3])[:15],
    "missing_keywords": sorted([k for k in missing if len(k) > 3])[:15]
    }