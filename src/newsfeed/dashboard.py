import json
import os
from datetime import datetime
from pathlib import Path

import dash
import pandas as pd
from dash.dependencies import Input, Output

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
    mit = NEWS_ARTICLES_SUMMARY_SOURCES["mit"]
    google_ai = NEWS_ARTICLES_SUMMARY_SOURCES["google_ai"]
    ai_blog = NEWS_ARTICLES_SUMMARY_SOURCES["ai_blog"]

    if news_blog_source == "mit":
        df = read_json_files_to_df(mit)
        df["source"] = "mit"
    elif news_blog_source == "google_ai":
        df = read_json_files_to_df(google_ai)
        df["source"] = "google_ai"
    elif news_blog_source == "ai_blog":
        df = read_json_files_to_df(ai_blog)
        df["source"] = "ai_blog"
    elif news_blog_source == "all_blogs":
        mit_df = read_json_files_to_df(mit)
        mit_df["source"] = "mit"

        google_ai_df = read_json_files_to_df(google_ai)
        google_ai_df["source"] = "google_ai"

        ai_blog = read_json_files_to_df(ai_blog)
        ai_blog["source"] = "ai_blog"

        df = pd.concat([mit_df, google_ai_df, ai_blog], ignore_index=True)
    else:
        raise ValueError("Invalid choice. Use 'mit', 'google_ai', 'ai_blog', or 'all_blogs'")

    return df


@app.callback(Output("blogs-df", "data"), [Input("data-type-dropdown", "value")])
def blogs_df(selected_data_type):
    if selected_data_type == "all_blogs":
        all_blogs = get_news_data("all_blogs")
        return all_blogs.to_dict("records")
    elif selected_data_type == "google_ai":
        google_ai = get_news_data("google_ai")
        return google_ai.to_dict("records")
    elif selected_data_type == "mit":
        mit = get_news_data("mit")
        return mit.to_dict("records")
    elif selected_data_type == "ai_blog":
        ai_blog = get_news_data("ai_blog")
        return ai_blog.to_dict("records")


@app.callback(
    [Output("blog-heading", "children"), Output("content-container", "children")],
    [Input("dropdown-choice", "value")],
)
def display_blogs(choice):
    df = get_news_data(choice)

    if (
        "title" not in df.columns
        or "blog_summary" not in df.columns
        or "unique_id" not in df.columns
    ):
        return "No title", "No Summary"

    # Read article data from various sources
    mit_articles_df = read_json_files_to_df(NEWS_ARTICLES_ARTICLE_SOURCES["mit"])
    google_ai_articles_df = read_json_files_to_df(NEWS_ARTICLES_ARTICLE_SOURCES["google_ai"])
    ai_blog_articles_df = read_json_files_to_df(NEWS_ARTICLES_ARTICLE_SOURCES["ai_blog"])

    # Combine all articles into single dataframe for easy look up
    all_articles_df = pd.concat([mit_articles_df, google_ai_articles_df, ai_blog_articles_df])
    print(all_articles_df)

    # This ensures that columns with links and published date are actually available
    # otherwise raise an error
    if (
        "unique_id" not in all_articles_df.columns
        or "link" not in all_articles_df.columns
        or "published" not in all_articles_df.columns
    ):
        raise ValueError(f"No link or published_date for this id")

    news_item = []

    # Loop through each row in the summaries dataframe
    for index, row in df.iterrows():
        title = row["title"]
        summary = row["blog_summary"]
        unique_id = row["unique_id"]

        # Look up the additional data based on the unique_id
        additional_data = all_articles_df[all_articles_df["unique_id"] == unique_id]

        # Fetch link and published date if the unique_id is found
        if not additional_data.empty:
            link = additional_data.iloc[0]["link"]
            published_date = additional_data.iloc[0]["published"]
        else:
            raise ValueError(f"No matching additional info for Id: {unique_id}")

        # Create the HTML Div for this particular news item
        date_object = datetime.strptime(published_date, "%Y-%m-%d")
        formatted_date = date_object.strftime("%b %d, %Y")

        div = [
            dash.html.H2(title, style={"color": "grey", "fontFamily": "Roboto"}),
            dash.html.P(
                f"Published On: {formatted_date}",
                style={
                    "fontSize": "16px",
                    "fontFamily": "Roboto",
                    "fontWeight": "900",
                    "color": "grey",
                },
            ),
            dash.html.P(
                summary,
                style={
                    "margin": "10px 0",
                    "textAlign": "left",
                    "fontFamily": "Roboto",
                    "fontSize": "16",
                    "fontWeight": "400",
                    "lineHeight": "1.4",
                },
            ),
            dash.html.A(
                f"Link: Read More Here...",
                href=link,
                target="_blank",
                style={
                    "textDecoration": "underline",
                    "textAlign": "left",
                    "fontFamily": "Roboto",
                    "color": "teal",
                },
            ),
            dash.html.Br(),
            dash.html.Br(),
            dash.html.Hr(),
        ]
        news_item.append(dash.html.Div(div, style={"padding": "10px"}))

    heading = dash.html.Div(
        [
            dash.html.H1(
                "The Midjourney Journal",
                style={
                    "fontFamily": "Roboto",
                    "color": "black",
                    "marginTop": "20",
                    "fontSize": "30",
                },
            ),
            dash.html.Br(),
        ]
    )
    content = dash.html.Div(news_item)
    return heading, content


if __name__ == "__main__":
    app.run_server(debug=True)
