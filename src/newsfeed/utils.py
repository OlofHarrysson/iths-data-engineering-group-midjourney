import argparse
from pathlib import Path


def parse_args():
    # Parse command-line arguments for sending summaries to Discord.
    # Returns a Namespace object with the parsed arguments.

    parser = argparse.ArgumentParser(description="Enables running scripts in the terminal")
    parser.add_argument("--blog_name", type=str, help="Name of the specific blog source")
    return parser.parse_args()


formated_source = {
    "mit": "MIT",
    "google_ai": "Google Artificial Intelligence",
    "ai_blog": "Artificial Intelligence Blog",
    "open_ai": "OpenAI",
}

source_dict = {
    "mit": "mit",
    "google_ai": "google_ai",
    "ai_blog": "ai_blog",
    "open_ai": "open_ai",
    "all_blogs": ["mit", "google_ai", "ai_blog", "open_ai"],
}
NEWS_ARTICLES_SUMMARY_SOURCES = {
    "mit": Path(__file__).parent.parent.parent / f"data/data_warehouse/mit/summaries",
    "google_ai": Path(__file__).parent.parent.parent / f"data/data_warehouse/google_ai/summaries",
    "ai_blog": Path(__file__).parent.parent.parent / f"data/data_warehouse/ai_blog/summaries",
    "open_ai": Path(__file__).parent.parent.parent / f"data/data_warehouse/open_ai/summaries",
}
NEWS_ARTICLES_ARTICLE_SOURCES = {
    "mit": Path(__file__).parent.parent.parent / f"data/data_warehouse/mit/articles",
    "google_ai": Path(__file__).parent.parent.parent / f"data/data_warehouse/google_ai/articles",
    "ai_blog": Path(__file__).parent.parent.parent / f"data/data_warehouse/ai_blog/articles",
    "open_ai": Path(__file__).parent.parent.parent / f"data/data_warehouse/open_ai/articles",
}
SWEDISH_NEWS_ARTICLES_SUMMARY_SOURCES = {
    "mit": Path(__file__).parent.parent.parent
    / f"data/data_svenska/data_warehouse/mit/sv_summaries",
    "google_ai": Path(__file__).parent.parent.parent
    / f"data/data_svenska/data_warehouse/google_ai/sv_summaries",
    "ai_blog": Path(__file__).parent.parent.parent
    / f"data/data_svenska/data_warehouse/ai_blog/sv_summaries",
    "open_ai": Path(__file__).parent.parent.parent
    / f"data/data_svenska/data_warehouse/open_ai/sv_summaries",
}
