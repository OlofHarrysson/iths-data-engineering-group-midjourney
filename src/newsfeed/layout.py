# layout.py
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    [
        html.Img(
            id="midjourney-logo",
            src="assets/midjourney-logo.png",
            style={"position": "absolute", "top": "-2%", "left": "-2%", "width": "250px"},
        ),
        html.H1("Article Summarizer", style={"text-align": "center"}),
        html.H2(id="summary-timestamp", children="", style={"text-align": "center"}),
        html.Hr(),
        # 'Select a Blog' dropdown centered and above 'Select an Article'
        html.Div(
            [  # New parent div
                dbc.CardGroup(
                    [
                        dbc.Label("Select a Blog:", html_for="article-dropdown"),
                        dcc.Dropdown(
                            id="blog-dropdown",
                            options=[
                                {"label": "Blog 1", "value": "Blog 1"},
                                {"label": "Blog 2", "value": "Blog 2"},
                                # Add more options as needed
                            ],
                            value="Blog 1",  # Default value
                            style={"width": "300px"},  # Set the width to 300px
                        ),
                    ],
                    style={"display": "inline-block", "margin-top": "-5px"},
                )
            ],
            style={"display": "flex", "justify-content": "center"},
        ),  # Flexbox centering
        html.Br(),  # Add some space between dropdowns
        # 'Select an Article' dropdown
        html.Div(
            [  # New parent div
                dbc.CardGroup(
                    [
                        dbc.Label("Select an Article:", html_for="article-dropdown"),
                        dcc.Dropdown(
                            id="article-dropdown",
                            options=[
                                {"label": "Article 1", "value": "Article 1"},
                                {"label": "Article 2", "value": "Article 2"},
                                # Add more options as needed
                            ],
                            value="Article 1",  # Default value
                            style={"width": "300px"},  # Set the width to 300px
                        ),
                    ],
                    style={"display": "inline-block", "margin-top": "-5px"},
                )
            ],
            style={"display": "flex", "justify-content": "center"},
        ),  # Flexbox centering
        # add a button to generate summary
        html.Div(
            [
                dbc.CardGroup(
                    [
                        dbc.Button(
                            "Generate Summary",
                            id="generate-summary-button",
                            color="primary",
                            className="mr-1",
                        ),
                    ],
                    style={"margin-top": "20px"},
                )
            ],
            style={"display": "flex", "justify-content": "center"},
        ),
        html.Hr(style={"margin-top": "10px"}),
        html.H2(id="summary-title", style={"text-align": "center"}),
        html.Div(id="summary-content", style={"text-align": "center"}),
        html.Div(id="article-date", style={"text-align": "center"}),
        html.Div(id="article-link", style={"text-align": "center"}),
    ],
    style={"text-align": "center"},
)
