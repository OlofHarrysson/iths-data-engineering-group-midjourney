import argparse
import time
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
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


# This function is detached and scrapes OpenAi blog in
def extract_openai_articles(soup):
    articles = []
    blog_links = soup.find_all("a", {"class": "ui-link group relative cursor-pointer"})
    for link in blog_links:
        blog_url = "https://openai.com" + link["href"]
        response = requests.get(blog_url)
        response.raise_for_status()
        time.sleep(0.2)
        blog_soup = BeautifulSoup(response.text, "html.parser")
        title = blog_soup.find(class_="f-display-2")
        description = blog_soup.find(class_="mt-spacing-4 f-subhead-1 ui-richtext")

        target_blog_article = blog_soup.find_all(class_="ui-richtext")

        if target_blog_article:
            p_elements = target_blog_article
            blog_article = " ".join(p.get_text() for p in p_elements)
        published_date = blog_soup.find(class_="f-meta-2")

        if title and description and blog_article and published_date:
            title = title.get_text()
            description = description.get_text()
            unique_id = create_uuid_from_string(title)
            published_date = pd.to_datetime(published_date.get_text()).date()
            words = blog_article.split()
            max_words = 1500
            blog_text = blog_article
            if len(words) > max_words:
                blog_text = " ".join(words[:max_words])
            article_information = BlogInfo(
                unique_id=unique_id,
                title=title,
                description=description,
                link=blog_url,
                blog_text=blog_text,
                published=published_date,
                timestamp=datetime.now(),
            )
            articles.append(article_information)
    return articles


def extract_articles_from_xml(parsed_xml: BeautifulSoup, blog_name):
    articles = []
    if blog_name == "open_ai":
        soup = parsed_xml
        articles = extract_openai_articles(soup)

    else:
        for item in parsed_xml.find_all(["item", "entry"]):
            raw_blog_text = item.find("content:encoded" if "item" in item.name else "content").text
            soup = BeautifulSoup(raw_blog_text, "html.parser")
            title = item.title.text
            unique_id = create_uuid_from_string(title)
            blog_text = soup.get_text()

            # Limit blog_text to 1500 words to fit GPT3.5-turbo summarize model which has maximum 4097 tokens (~3000 words)
            # Words exciding 1500 are truncated
            max_words = 1500
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
    articles = extract_articles_from_xml(parsed_xml, blog_name=blog_name)
    save_articles(articles, blog_name)
    print(f"Done processing {blog_name}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blog_name", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(blog_name=args.blog_name)
