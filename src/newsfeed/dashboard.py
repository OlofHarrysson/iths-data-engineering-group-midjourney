import json
import os
from pathlib import Path

import dash
import pandas as pd
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
def get_news_data(news_blog_source="all_blogs"):
    # Define a dictionary to map user choices to their respective source names
    source_dict = {
        "mit": "mit",
        "google_ai": "google_ai",
        "ai_blog": "ai_blog",
        "all_blogs": ["mit", "google_ai", "ai_blog"],
    }

    # Check if the user choice is valid, raise an error if it's not
    if news_blog_source not in source_dict:
        raise ValueError("Invalid choice. Use 'mit', 'google_ai', 'ai_blog', or 'all_blogs'")

    # Handle the case where data from all blogs are requested
    if news_blog_source == "all_blogs":
        # Initialize an empty list to store DataFrames for each blog source
        df_list = []
        # Loop through each blog source
        for source in source_dict["all_blogs"]:
            # Read JSON files for the given blog source into a DataFrame
            temp_df = read_json_files_to_df(NEWS_ARTICLES_SUMMARY_SOURCES[source])
            # Add a new column to identify the source of each article
            temp_df["source"] = source
            # Append the DataFrame to our list
            df_list.append(temp_df)
        # Concatenate all DataFrames into a single DataFrame and return
        return pd.concat(df_list, ignore_index=True)

    # Handle the case where data from a single blog is requested
    df = read_json_files_to_df(NEWS_ARTICLES_SUMMARY_SOURCES[source_dict[news_blog_source]])
    # Add a new column to identify the source of each article
    df["source"] = source_dict[news_blog_source]
    # Return the DataFrame
    return df


@app.callback(Output("blogs-df", "data"), [Input("data-type-dropdown", "value")])
def blogs_df(selected_data_type):
    # Get the news data based on the selected type
    news_data = get_news_data(selected_data_type)
    # Convert the DataFrame to a dictionary of records and return
    return news_data.to_dict("records")


@app.callback(
    [Output("blog-heading", "children"), Output("content-container", "children")],
    [Input("dropdown-choice", "value")],
)
def display_blogs(choice):
    df = get_news_data(choice)

    if (
        "title" not in df.columns
        or "blog_summary_technical" not in df.columns
        or "unique_id" not in df.columns
    ):
        return "No title", "No Summary"

    # Read article data from various sources
    mit_articles_df = read_json_files_to_df(NEWS_ARTICLES_ARTICLE_SOURCES["mit"])
    google_ai_articles_df = read_json_files_to_df(NEWS_ARTICLES_ARTICLE_SOURCES["google_ai"])
    ai_blog_articles_df = read_json_files_to_df(NEWS_ARTICLES_ARTICLE_SOURCES["ai_blog"])

    # Combine all articles into single dataframe for easy look up
    all_articles_df = pd.concat([mit_articles_df, google_ai_articles_df, ai_blog_articles_df])

    # This ensures that columns with links and published date are actually available
    # otherwise raise an error
    if (
        "unique_id" not in all_articles_df.columns
        or "link" not in all_articles_df.columns
        or "published" not in all_articles_df.columns
    ):
        raise ValueError(f"No link or published_date for this id")

    news_item_with_date = []

    print(df.head())

    # Loop through each row in the summaries dataframe
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
                    title, published_date, summary_technical, summary_non_technical, link
                )
            )

        else:
            raise ValueError(f"No matching additional info for Id: {unique_id}")

        # Create the HTML Div for this particular news item

    heading = title_heading_for_dashboard(heading="The Midjourney Journal")

    # Sort the list by date
    sorted_news_item_with_date = sorted(news_item_with_date, key=lambda x: x["date"], reverse=True)

    # Extract the sorted divs
    sorted_news_item = [item["div"] for item in sorted_news_item_with_date]

    content = dashboard_content_container(sorted_news_item)
    return heading, content


if __name__ == "__main__":
    app.run_server(debug=True)
