import os
from dotenv import load_dotenv
from openai import OpenAI

from prompts import (
    RECRUITER_PROMPT,
    TECHNICAL_PROMPT,
    CULTURE_PROMPT,
    COUNCIL_PROMPT
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def run_agent(prompt):

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def recruiter_agent(jd, resume, notes):

    prompt = f"""
    {RECRUITER_PROMPT}

    JOB DESCRIPTION:
    {jd}

    RESUME:
    {resume}

    INTERVIEW NOTES:
    {notes}
    """

    return run_agent(prompt)


def technical_agent(jd, resume, notes):

    prompt = f"""
    {TECHNICAL_PROMPT}

    JOB DESCRIPTION:
    {jd}

    RESUME:
    {resume}

    INTERVIEW NOTES:
    {notes}
    """

    return run_agent(prompt)


def culture_agent(jd, resume, notes):

    prompt = f"""
    {CULTURE_PROMPT}

    JOB DESCRIPTION:
    {jd}

    RESUME:
    {resume}

    INTERVIEW NOTES:
    {notes}
    """

    return run_agent(prompt)


def council_agent(recruiter_result, technical_result, culture_result):

    prompt = f"""
    {COUNCIL_PROMPT}

    RECRUITER EVALUATION:
    {recruiter_result}

    TECHNICAL EVALUATION:
    {technical_result}

    CULTURE EVALUATION:
    {culture_result}
    """

    return run_agent(prompt)