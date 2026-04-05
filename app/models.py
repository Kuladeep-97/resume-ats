from pydantic import BaseModel

class ResumeInput(BaseModel):
    resume_text: str
    job_description: str
    role: str="Software Engineer"
