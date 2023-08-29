import argparse
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from newsfeed.datatypes import BlogInfo


def create_uuid_from_string(title):
    assert isinstance(title, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, title))


def load_metadata(blog_name):
    metadata_path = Path("data/data_lake") / blog_name / "metadata.xml"
    with open(metadata_path) as f:
        xml_text = f.read()

    parsed_xml = BeautifulSoup(xml_text, "xml")
    return parsed_xml


def extract_articles_from_xml(parsed_xml):
    articles = []
    for item in parsed_xml.find_all(["item", "entry"]):
        raw_blog_text = item.find("content:encoded" if "item" in item.name else "content").text
        soup = BeautifulSoup(raw_blog_text, "html.parser")
        title = item.title.text
        unique_id = create_uuid_from_string(title)
        blog_text = soup.get_text()

        # Limit blog_text to 2800 words to fit GPT3.5-turbo summarize model which has maximum 4097 tokens (~3000 words)
        # Words exciding 2800 are truncated
        max_words = 2800
        words = blog_text.split()
        if len(words) > max_words:
            blog_text = " ".join(words[:max_words])

        if "item" in item.name:  # Handle "item" structure as for mit and ai_blog
            article_info = BlogInfo(
                unique_id=unique_id,
                title=title,
                description=item.description.text,
                link=item.link.text,
                blog_text=blog_text,
                published=pd.to_datetime(item.pubDate.text).date(),
                timestamp=datetime.now(),
            )
        else:  # Handle "entry" structure as for google_ai
            article_info = BlogInfo(
                unique_id=unique_id,
                title=title,
                link=item.find_all("link")[1]["href"],
                blog_text=blog_text,
                published=pd.to_datetime(item.published.text).date(),
                timestamp=datetime.now(),
            )

        articles.append(article_info)

    return articles


def save_articles(articles, blog_name):
    save_dir = Path("data/data_warehouse", blog_name, "articles")
    save_dir.mkdir(exist_ok=True, parents=True)
    for article in articles:
        # try/except to skip articles which raise errors
        try:
            save_path = save_dir / article.get_filename()
            with open(save_path, "w") as f:
                f.write(article.json(indent=2))
        except Exception as e:
            print(f"Error saving article: {e}")
            continue


def main(blog_name):
    print(f"Processing {blog_name}")
    parsed_xml = load_metadata(blog_name)
    articles = extract_articles_from_xml(parsed_xml)
    save_articles(articles, blog_name)
    print(f"Done processing {blog_name}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blog_name", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(blog_name=args.blog_name)
