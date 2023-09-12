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
                            "width": "300px",
                        },
                    )
                ]
            ),
        )
    )


# blog heading section
def create_blog_heading():
    """Creates the blog heading section of the layout"""
    return dbc.Col(
        dbc.Card(dbc.CardBody([dbc.Row(id="blog-heading", style={"text-align": "center"})])),
        style={"overflow": "hidden"},
    )


# dropdown for data types (hidden by default)
def create_data_type_dropdown():
    """creates the dropdown for data types"""
    return dbc.Col(
        dbc.Card(
            html.Div(
                [
                    dcc.Dropdown(
                        id="data-type-dropdown",
                        className="hidden",
                        options=[
                            {"label": "All Blogs", "value": "all_blogs"},
                            {"label": "Google AI", "value": "google_ai"},
                            {"label": "MIT", "value": "mit"},
                            {"label": "Artificial Intelligence Blog", "value": "ai_blog"},
                            {"label": "OpenAI", "value": "open_ai"},
                        ],
                        value="all_blogs",
                        style={"width": "0px", "height": "0px"},
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
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                id="dropdown-choice",
                                options=[
                                    {
                                        "label": "All Blogs",
                                        "value": "all_blogs",
                                    },
                                    {
                                        "label": "Google AI",
                                        "value": "google_ai",
                                    },
                                    {"label": "MIT", "value": "mit"},
                                    {
                                        "label": "Artificial Intelligence Blog",
                                        "value": "ai_blog",
                                    },
                                    {"label": "OpenAI", "value": "open_ai"},
                                ],
                                value="all_blogs",
                                style={"width": "300px", "margintop": "100px"},
                            ),
                        ),
                    ],
                    style={"margintop": "25px"},
                ),
                style={},
            )
        )
    )


def language_choice():
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "justifyContent": "space-evenly",
                            "alignItems": "center",
                            "height": "100%",
                            "padding": "35px",
                            "backgorundColor": "white",
                        },
                        children=[
                            html.Button(
                                "🇬🇧 English",
                                style={"padding": "8px", "marginRight": "15px"},
                                id="btn-english",
                            ),
                            html.Button("🇸🇪 Swedish", style={"padding": "8px"}, id="btn-swedish"),
                        ],
                    )
                ],
                style={"bottom": "0px", "width": "100%"},
            ),
        ),
        style={"position": "relative"},
    )


def logo_row():
    return html.Div(
        style={
            "display": "flex",
            "justifyContent": "space-between",
        },
        children=[
            html.Div(create_logo(), style={"flex": "1"}),
            html.Div(create_blog_heading(), style={"flex": "4"}),
            html.Div(language_choice(), style={"flex": "1"}),
        ],
    )


def dropdown_select_blogs():
    return html.Div(
        dbc.Card(
            dbc.CardBody(
                children=[
                    dbc.Col(
                        create_data_type_dropdown(),
                        width={"size": 6, "offset": 3},
                    ),
                    dbc.Col(
                        create_blog_choice_dropdown(),
                        width={"size": 6, "offset": 3},
                    ),
                ]
            ),
        ),
        style={
            "flex": "3",
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "marginTop": "0px",
        },
    )


def search_input():
    return html.Div(
        dcc.Input(
            autoComplete="off",
            placeholder="search in titles",
            id="search-input",
            type="text",
            value="",
            style={
                "width": "100%",
                "height": "100%",
                "padding": "6px",
                "fontSize": "16px",
            },
        ),
        style={
            "flex": "3",
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
        },
    )


def search_button():
    return html.Div(
        html.Button(
            "search",
            id="search-btn",
            style={
                "height": "100%",
                "padding": "7px",
                "fontSize": "14px",
            },
        ),
        style={
            "flex": "1",
            "display": "flex",
            "justifyContent": "left",
            "alignItems": "left",
            "width": "20px",
            "marginLeft": "15px",
            "height": "100%",
        },
    )


def header_content():
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                className="mb-4",
                children=[
                    dbc.Row(children=[logo_row()]),
                    dbc.Row(
                        children=[
                            html.Div(
                                children=[
                                    dropdown_select_blogs(),
                                    search_input(),
                                    search_button(),
                                ],
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "maxWidth": "1080px",
                                    "alignContent": "center",
                                    "alignItems": "center",
                                    "margin": "auto",
                                },
                            )
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
    )


def news_content():
    return dbc.Card(
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
    )


# creates layout
def create_layout():
    """Creates the layout for the dashboard"""
    return dbc.Container(
        [
            header_content(),
            news_content(),
            dcc.Store(id="blogs-df"),
            dcc.Store(id="language-store", data={"language": "english"}),
        ]
    )


layout = create_layout()
