import argparse
import json
import os
from pathlib import Path

from transformers import MarianMTModel, MarianTokenizer


# Template function to initialise translation model
def translate_initialised(text, model, tokenizer):
    tokenized_text = tokenizer([text], return_tensors="pt")
    translated_output = model.generate(**tokenized_text)
    translated_text = tokenizer.batch_decode(translated_output, skip_special_tokens=True)[0]
    return translated_text


def translate_summaries(blog_name):
    # This defines which defines which language will be translated from and to
    model_name = "Helsinki-NLP/opus-mt-en-sv"

    # Initialises the model
    model = MarianMTModel.from_pretrained(model_name)

    # Initialize translation model and tokenizer
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    # Get Path with summaries
    path_to_summaries = (
        Path(__file__).parent.parent.parent / "data/data_warehouse" / blog_name / "summaries"
    )
    # define path to save summaries
    path_swedish_summaries = Path("data/data_svenska/data_warehouse") / blog_name / "sv_summaries"
    path_swedish_summaries.mkdir(exist_ok=True, parents=True)

    for filename in os.listdir(path_to_summaries):
        if filename.endswith(".json"):
            full_path = os.path.join(path_to_summaries, filename)

            # Load JSON file
            with open(full_path, "r") as f:
                data = json.load(f)

            # Loop through each json file and pick out each item frm the keys
            for key in data.keys():
                # Do not translate 'unique_id'
                if key == "unique_id":
                    continue

                # Only translate strings
                if isinstance(data[key], str):
                    data[key] = translate_initialised(data[key], model, tokenizer)

            # Save updated JSON back to file
            save_path = path_swedish_summaries / filename

            # Save updated JSON back to file
            with open(save_path, "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)


def main(blog_name):
    print("Initialising translations...")
    translate_summaries(blog_name=blog_name)
    print("Summarising completed sucessfully!")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--blog_name", type=str, required=True, choices=["mit", "google_ai", "ai_blog", "open_ai"]
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    blog_name = args.blog_name
    main(blog_name)
