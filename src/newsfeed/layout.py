import dash_bootstrap_components as dbc
from dash import dcc, html


# logo/image section
def create_logo():
    """Creates the logo section of the layout"""
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Img(
                        id="midjourney-logo",
                        src="assets/midjourney-logo.png",
                        style={
                            "position": "absolute",
                            "top": "-2%",
                            "left": "-2%",
                            "width": "250px",
                        },
                    )
                ]
            )
        )
    )


# blog heading section
def create_blog_heading():
    """Creates the blog heading section of the layout"""
    return dbc.Col(
        dbc.Card(dbc.CardBody([dbc.Row(id="blog-heading", style={"text-align": "center"})]))
    )


# dropdown for data types (hidden by default)
def create_data_type_dropdown():
    """creates the dropdown for data types"""
    return dbc.Col(
        dbc.Card(
            html.Div(
                [
                    dbc.CardGroup(
                        dcc.Dropdown(
                            id="data-type-dropdown",
                            className="hidden",
                            options=[
                                {"label": "All Blogs", "value": "all_blogs"},
                                {"label": "Google-ai", "value": "google_ai"},
                                {"label": "MIT", "value": "mit"},
                                {"label": "AI-Blog", "value": "ai_blog"},
                            ],
                            value="all_blogs",
                            style={"width": "300px", "height": "0px"},
                        )
                    )
                ],
                style={"justify-content": "center"},
            ),
            style={"display": "none"},
        )
    )


# dropdown for blog choices
def create_blog_choice_dropdown():
    """creates the dropdown for blog choices"""
    return dbc.Col(
        dbc.Card(
            html.Div(
                [
                    dbc.CardGroup(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Label(
                                                    "Select a Blog",
                                                    html_for="dropdown-choice",
                                                    style={
                                                        "fontSize": "18px",
                                                        "fontFamily": "Roboto",
                                                        "marginBottom": "10px",
                                                    },
                                                ),
                                                width={"size": 3},
                                            ),
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id="dropdown-choice",
                                                    options=[
                                                        {
                                                            "label": "All Blogs",
                                                            "value": "all_blogs",
                                                        },
                                                        {
                                                            "label": "Google-ai",
                                                            "value": "google_ai",
                                                        },
                                                        {"label": "MIT", "value": "mit"},
                                                        {"label": "AI-Blog", "value": "ai_blog"},
                                                    ],
                                                    value="all_blogs",
                                                    style={"width": "300px"},
                                                ),
                                                width={"size": 3},
                                            ),
                                        ]
                                    )
                                ]
                            )
                        )
                    )
                ],
                style={"display": "flex", "justify-content": "center"},
            )
        )
    )


# creates layout
def create_layout():
    """Creates the layout for the dashboard"""
    return dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        className="mb-44",
                        children=[
                            dbc.Row(children=[create_logo(), create_blog_heading()]),
                            dbc.Row(
                                children=[
                                    create_data_type_dropdown(),
                                    create_blog_choice_dropdown(),
                                ]
                            ),
                        ],
                    )
                ),
                style={
                    "position": "fixed",
                    "top": 0,
                    "width": "100%",
                    "z-index": 1000,
                    "height": "170px",
                    "backgroundColor": "white",
                },
            ),
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        id="content-container",
                        style={
                            "justifyContent": "center",
                            "alignItems": "center",
                            "height": "100vh",
                            "maxWidth": "1080px",
                            "alignSelf": "center",
                            "margin": "0 auto",
                        },
                    )
                ),
                style={"marginTop": "170px"},
            ),
            dcc.Store(id="blogs-df"),
        ]
    )


layout = create_layout()
