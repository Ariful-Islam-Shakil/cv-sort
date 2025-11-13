from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional, List
import pandas as pd
import os
import json
import time
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# model = "meta-llama/Llama-4-Scout-17B-16E-Instruct"
model = "llama-3.1-8b-instant"

# -------- Define structured output schema --------
class CVScore(BaseModel):
    Name: Optional[str] = Field(None, description="Candidate full name")
    Strength: Optional[str] = Field(None, description="Key strengths based on JD and CV match")
    Weakness: Optional[str] = Field(None, description="Weak points or missing skills based on JD and CV")
    Score: Optional[float] = Field(None, description="Relevance score between 0 and 10 (2 decimal precision)")

class CVBatchResult(BaseModel):
    results: List[CVScore] = Field(..., description="List of candidate evaluations")

# -------- Initialize LLM --------
llm = ChatGroq(model=model, api_key=GROQ_API_KEY)

# -------- Prompt Template --------
prompt = ChatPromptTemplate.from_template("""
You are an expert HR recruiter.
You will receive:
1️⃣ A Job Description (JD)
2️⃣ Multiple candidate CVs in the format: "filename: CV text"

Your task:
- Analyze ALL CVs **together** relative to the JD.
- For each candidate, extract:
  - Name
  - Strengths (skills aligning with JD)
  - Weaknesses (missing or weak areas)
  - A numeric Score (0–10, 2 decimal precision)
- Return **a list** of JSON objects strictly matching this schema:

[
  {{"Name": "John Doe", "Strength": "...", "Weakness": "...", "Score": 8.75}},
  {{"Name": "Jane Smith", "Strength": "...", "Weakness": "...", "Score": 6.50}}
]

Job Description:
{job_description}

Candidate CVs:
{cv_batch}
""")


# -------- Single-call batch analysis --------
def analyze_cv_batch_single_call(jd: str, cv_batch: str, max_retries: int = 3, retry_delay: int = 2):
    """
    jd: Job Description (string)
    cv_batch: Combined CVs (filename: cv text \n\n filename: cv text ...)
    Returns: List[Dict] -> [{Name, Strength, Weakness, Score}, ...]
    """
    for attempt in range(1, max_retries + 1):
        try:
            chain = prompt | llm
            response = chain.invoke({
                "job_description": jd,
                "cv_batch": cv_batch
            })
            
            # Try to parse JSON from model output
            raw_text = response.content if hasattr(response, "content") else str(response)
            try:
                parsed = json.loads(raw_text)
                return parsed
            except json.JSONDecodeError:
                print("⚠️ Model output not valid JSON, trying to fix...")
                import re
                json_text = re.search(r'\[.*\]', raw_text, re.DOTALL)
                if json_text:
                    parsed = json.loads(json_text.group(0))
                    return parsed
                else:
                    raise ValueError("No valid JSON array found in output.")

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                print("❌ Max retries reached.")
                return []

def format_batch(batch):
    batch = "\n\n".join(batch)
    # print(batch)
    return batch

# -------- Example usage --------
if __name__ == "__main__":

    jd = """We are hiring an AI/ML Engineer skilled in Python, TensorFlow or PyTorch,
    experience with NLP or computer vision, and familiarity with data preprocessing, model deployment, and Git."""

    cv_batch = [
    "john_doe_cv.txt: John Doe is an AI engineer experienced in Python, TensorFlow, and NLP projects like sentiment analysis. He has some basic deployment experience.",

    "jane_smith_cv.txt: Jane Smith is a web developer skilled in React, Node.js, and MongoDB. No prior AI or ML experience mentioned.",

    "alex_khan_cv.txt: Alex Khan worked on image classification using PyTorch, OpenCV, and deployed models on AWS using Docker."
    ]
    with open("/Users/mdarifulislamshakil/ztrios/cv-sort/cv_batches.json", "r") as f:
        batches = json.load(f)
    total_df = pd.DataFrame()
    for i, cv_batch in enumerate(batches):
        print(f"\n\n=== Analyzing CV Batch {i+1} ===")
        # cv_batch = format_batch(cv_batch)
        results = analyze_cv_batch_single_call(jd, cv_batch)
        print(json.dumps(results, indent=2))

        if results:
            df = pd.DataFrame(results)
            total_df = pd.concat([total_df, df], ignore_index=True)
    total_df.to_csv("jd_cv_analysis_single_call.csv", index=False)
    logger.info("✅ Batch analysis complete. Results saved to jd_cv_analysis_single_call.csv")
