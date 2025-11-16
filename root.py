import pandas as pd
import os, json 
from loguru import logger
from read_cv import read_cv_info
from create_batch import tokenize_and_batch 
from llm import analyze_cv_batch_single_call

def pipeline(folder: str, JDI:str, jd: str, Department: str = "AI_ML", output_version: str = "v1"):
    cv_texts = read_cv_info(folder)
    batches = tokenize_and_batch(cv_texts, max_tokens=3000, model_name="gpt-3.5-turbo")

    total_df = pd.DataFrame()
    for i, cv_batch in enumerate(batches):
        print(f"\n\n=== Analyzing CV Batch {i+1} ===")
        # cv_batch = format_batch(cv_batch)
        results = analyze_cv_batch_single_call(jd, cv_batch)
        print(json.dumps(results, indent=2))

        if results:
            df = pd.DataFrame(results)
            df.columns = ["Name", "Strengths", "Weaknesses", "Score"]
            total_df = pd.concat([total_df, df], ignore_index=True) 

    output_path = f"./results/sorted_cv_{Department}_{output_version}.csv"
    total_df = total_df.sort_values(by="Score", ascending=False)
    total_df["Rank"] = range(1, len(total_df) + 1)
    total_df.to_csv(output_path, index=False)

    logger.info(f"✅ Batch analysis complete. Results saved to {output_path}")
    
    return total_df

if __name__ == "__main__":
    folder = "/Users/mdarifulislamshakil/ztrios/cv-sort/AI-Intern-9-Nov-2025"
    JDI = "SE001"
    Department = "Software_Engineering"
    output_version = "v2"
    output_df = pipeline(folder, JDI, Department, output_version)

