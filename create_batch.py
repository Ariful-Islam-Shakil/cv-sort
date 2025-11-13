import json
from typing import List
import tiktoken
from read_cv import save_cv_data_to_json


def read_json_file(file_path: str) -> List[str]:
    """
    Read a JSON file that contains a list of CV texts.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of strings.")
    return data


def tokenize_and_batch(texts: List[str], max_tokens: int, model_name: str = "gpt-3.5-turbo") -> List[List[str]]:
    """
    Tokenize all texts and group them into batches under a token limit.

    Args:
        texts: List of CV texts (strings)
        max_tokens: Maximum number of tokens allowed per batch
        model_name: Tokenizer model name (default: GPT-3.5)
    
    Returns:
        List of batches (each batch = list of strings)
    """
    enc = tiktoken.encoding_for_model(model_name)
    batches = []
    current_batch = []
    current_tokens = 0

    for text in texts:
        tokens = len(enc.encode(text))

        # if adding this text exceeds the limit → start new batch
        if current_tokens + tokens > max_tokens:
            batches.append(current_batch)
            current_batch = [text]
            current_tokens = tokens
        else:
            current_batch.append(text)
            current_tokens += tokens

    # append last batch
    if current_batch:
        batches.append(current_batch)
    batches = ["\n\n".join(batch) for batch in batches]
    return batches


if __name__ == "__main__":
    data_path = "/Users/mdarifulislamshakil/ztrios/cv-sort/cv_data.json"
    batch_path = "/Users/mdarifulislamshakil/ztrios/cv-sort/cv_batches.json"
    cv_texts = read_json_file(data_path)
    batches = tokenize_and_batch(cv_texts, max_tokens=3000, model_name="gpt-3.5-turbo")
    save_cv_data_to_json(batches, batch_path)