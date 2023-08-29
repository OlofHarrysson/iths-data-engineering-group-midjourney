import json
import os
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly_express as px
from dash.dependencies import Input, Output
from layout import layout

app = dash.Dash(
    __name__,
    # external_stylesheets=stylesheets,
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
)
app.layout = layout
server = app.server
NEWS_ARTICLES_SOURCES = {
    "articles": Path(__file__).parent.parent.parent / f"data/data_warehouse/mit/articles",
    "summaries": Path(__file__).parent.parent.parent / f"data/data_warehouse/mit/summaries",
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
    articles = NEWS_ARTICLES_SOURCES["articles"]
    summaries = NEWS_ARTICLES_SOURCES["summaries"]
    if news_blog_source == "articles":
        df = read_json_files_to_df(articles)
        df["source"] = "Articles"
    elif news_blog_source == "summaries":
        df = read_json_files_to_df(summaries)
        df["source"] = "Summaries"
    elif news_blog_source == "all_blogs":
        articles_df = read_json_files_to_df(articles)
        articles_df["source"] = "Articles"

        summaries_df = read_json_files_to_df(summaries)
        summaries_df["source"] = "Summaries"

        df = pd.concat([articles_df, summaries_df], ignore_index=True)
    else:
        raise ValueError("Invalid choice. Use 'articles', 'summaries', or 'all_blogs'")

    return df


@app.callback(Output("blogs-df", "data"), [Input("data-type-dropdown", "value")])
def blogs_df(selected_data_type):
    if selected_data_type == "all_blogs":
        all_blogs = get_news_data("all_blogs")
        return all_blogs.to_dict("records")
    elif selected_data_type == "summaries":
        summaries = get_news_data("summaries")
        return summaries.to_dict("records")
    elif selected_data_type == "articles":
        articles = get_news_data("articles")
        return articles.to_dict("records")


@app.callback(
    [Output("blog-heading", "children"), Output("content-container", "children")],
    [Input("dropdown-choice", "value")],
)
def display_blogs(choice):
    df = get_news_data(choice)

    if "title" not in df.columns or "blog_summary" not in df.columns:
        return "No title", "No description"

    # Source ChatGPT
    # This code automatically changes each title item into an H1 tag and
    # descriptions into paragraph tag
    titles = [dash.html.H2(title) for title in df["title"]]
    descriptions = [dash.html.P(description) for description in df["blog_summary"]]

    # Combine titles and descriptions
    news_item = []
    for title, description in zip(titles, descriptions):
        div = [dash.html.H5(title), dash.html.P(description), dash.html.Br(), dash.html.Br()]
        news_item.append(dash.html.Div(div))

    heading = dash.html.Div([dash.html.H2("The Midjourney Journal"), dash.html.Br()])
    content = dash.html.Div(news_item)
    return heading, content


if __name__ == "__main__":
    app.run_server(debug=True)
