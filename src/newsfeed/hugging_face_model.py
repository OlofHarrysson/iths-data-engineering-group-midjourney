import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline


def summarize_text_with_hugging_face(
    text, model_name="facebook/bart-large-cnn", max_length=250, min_length=25
):
    """
    Summarize the given text using the specified model.

    Parameters:
    - text (str): The text to summarize.
    - model_name (str): The name of the pre-trained model to use.
    - max_length (int): The maximum length of the summary.
    - min_length (int): The minimum length of the summary.

    Returns:
    - str: The summary of the text.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    summarization_pipeline = pipeline(
        "summarization", model=model_name, tokenizer=tokenizer, device=0
    )  # device=0 if you have a GPU
    summary = summarization_pipeline(
        text, max_length=max_length, min_length=min_length, do_sample=False
    )
    return summary[0]["summary_text"]
