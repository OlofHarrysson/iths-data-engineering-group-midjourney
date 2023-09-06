import json
import os
from pathlib import Path

import dash
import pandas as pd
from dash import Input, Output, State
from dash.dependencies import Input, Output

from layouts.article_item import (
    dashboard_content_container,
    news_artcle_div,
    title_heading_for_dashboard,
)
from newsfeed.layout import layout

app = dash.Dash(
    __name__,
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
)
app.layout = layout

server = app.server
NEWS_ARTICLES_SUMMARY_SOURCES = {
    "mit": Path(__file__).parent.parent.parent / f"data/data_warehouse/mit/summaries",
    "google_ai": Path(__file__).parent.parent.parent / f"data/data_warehouse/google_ai/summaries",
    "ai_blog": Path(__file__).parent.parent.parent / f"data/data_warehouse/ai_blog/summaries",
}
NEWS_ARTICLES_ARTICLE_SOURCES = {
    "mit": Path(__file__).parent.parent.parent / f"data/data_warehouse/mit/articles",
    "google_ai": Path(__file__).parent.parent.parent / f"data/data_warehouse/google_ai/articles",
    "ai_blog": Path(__file__).parent.parent.parent / f"data/data_warehouse/ai_blog/articles",
}
SWEDISH_NEWS_ARTICLES_SUMMARY_SOURCES = {
    "mit": Path(__file__).parent.parent.parent / f"data_svenska/data_warehouse/mit/sv_summaries",
    "google_ai": Path(__file__).parent.parent.parent
    / f"data_svenska/data_warehouse/google_ai/sv_summaries",
    "ai_blog": Path(__file__).parent.parent.parent
    / f"data_svenska/data_warehouse/ai_blog/sv_summaries",
}


# This function takes reads the json files then returns a df of the said json file. This should
# for example be a path for summaries json files
def read_json_files_to_df(folder_path):
    df_list = []
    # the os.listdir lists all the files in the folder/directory  specified by folder_path
    # passed in the function
    for filename in os.listdir(folder_path):
        # Filter out non json files
        if filename.endswith(".json"):
            # Here I attach each json file to the path of the folder_path
            # such that i can read it as such .../articles/article.json
            # then read the article and parse it this to a python object
            with open(os.path.join(folder_path, filename), "r") as f:
                data = json.load(f)
                df_list.append(data)
    # return dataframe from the list of python objects
    return pd.DataFrame(df_list)


# This function returns a blog articles from either a specific source or from all
# depending on the arguments inputed in the function when the function is called
def get_news_data(news_blog_source="all_blogs", language="english"):
    # Check which language user press to determine which data to use
    if language == "english":
        source_dict = {
            "mit": "mit",
            "google_ai": "google_ai",
            "ai_blog": "ai_blog",
            "all_blogs": ["mit", "google_ai", "ai_blog"],
        }
        source_data = NEWS_ARTICLES_SUMMARY_SOURCES
    elif language == "swedish":
        source_dict = {
            "mit": "mit",
            "google_ai": "google_ai",
            "ai_blog": "ai_blog",
            "all_blogs": ["mit", "google_ai", "ai_blog"],
        }
        source_data = SWEDISH_NEWS_ARTICLES_SUMMARY_SOURCES
    else:
        raise ValueError("Oops! Only english and swedish are supported languages!")

    # Rest of the code remains largely the same
    if news_blog_source not in source_dict:
        raise ValueError("Invalid choice. Use 'mit', 'google_ai', 'ai_blog', or 'all_blogs'")

    if news_blog_source == "all_blogs":
        df_list = []
        for source in source_dict["all_blogs"]:
            temp_df = read_json_files_to_df(source_data[source])
            temp_df["source"] = source
            df_list.append(temp_df)
        return pd.concat(df_list, ignore_index=True)

    df = read_json_files_to_df(source_data[source_dict[news_blog_source]])
    df["source"] = source_dict[news_blog_source]
    return df


def fetch_and_prepare_articles(language, df):
    if language == "english":
        articles_sources = NEWS_ARTICLES_ARTICLE_SOURCES
    else:
        articles_sources = NEWS_ARTICLES_ARTICLE_SOURCES

    all_articles_df = pd.concat(
        [read_json_files_to_df(articles_sources[key]) for key in articles_sources]
    )

    required_cols = ["unique_id", "link", "published"]
    if not all(col in all_articles_df.columns for col in required_cols):
        raise ValueError(
            "Missing required columns unique_id, link and published date in articles dataframe"
        )

    news_item_with_date = []
    for index, row in df.iterrows():
        title = row["title"]
        summary_technical = row["blog_summary_technical"]
        summary_non_technical = row["blog_summary_non_technical"]
        unique_id = row["unique_id"]

        # Look up the additional data based on the unique_id
        additional_data = all_articles_df[all_articles_df["unique_id"] == unique_id]

        # Fetch link and published date if the unique_id is found
        if not additional_data.empty:
            link = additional_data.iloc[0]["link"]
            published_date = additional_data.iloc[0]["published"]
            news_item_with_date.append(
                news_artcle_div(
                    title, published_date, summary_technical, summary_non_technical, link, language
                )
            )

        else:
            raise ValueError(f"No matching additional info for Id: {unique_id}")

    return news_item_with_date


@app.callback(Output("blogs-df", "data"), [Input("data-type-dropdown", "value")])
def blogs_df(selected_data_type):
    # Get the news data based on the selected type
    news_data = get_news_data(selected_data_type)
    # Convert the DataFrame to a dictionary of records and return
    return news_data.to_dict("records")


@app.callback(
    Output("language-store", "data"),
    [Input("btn-english", "n_clicks"), Input("btn-swedish", "n_clicks")],
    [State("language-store", "data")],
)
def update_language(n_clicks_english, n_clicks_swedish, data):
    # get click context
    ctx = dash.callback_context

    # check if button is clicked and which button recieved a click event
    if not ctx.triggered_id or ctx.triggered_id == "None":
        raise dash.exceptions.PreventUpdate

    if "btn-english" in ctx.triggered_id:
        data["language"] = "english"
    elif "btn-swedish" in ctx.triggered_id:
        data["language"] = "swedish"

    return data


@app.callback(
    [Output("blog-heading", "children"), Output("content-container", "children")],
    [
        Input("dropdown-choice", "value"),
        Input("language-store", "data"),
    ],
    [
        State("blogs-df", "data"),
    ],
)
def display_blogs(choice, language_data, blogs_data):
    language = language_data.get("language", "english")
    news_data = get_news_data(choice, language=language)

    if (
        "title" not in news_data.columns
        or "blog_summary_technical" not in news_data.columns
        or "unique_id" not in news_data.columns
    ):
        return "No title", "No Summary"

    news_item_with_date = fetch_and_prepare_articles(language, news_data)

    heading = title_heading_for_dashboard(heading="The Midjourney Journal")

    # Sort the list by date
    sorted_news_item_with_date = sorted(news_item_with_date, key=lambda x: x["date"], reverse=True)

    # Extract the sorted divs
    sorted_news_item = [item["div"] for item in sorted_news_item_with_date]

    content = dashboard_content_container(sorted_news_item)
    return heading, content


if __name__ == "__main__":
    app.run_server(debug=True)
