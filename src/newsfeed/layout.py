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
                    dbc.CardGroup(
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
                                                width={"size": 3},
                                            ),
                                        ],
                                        style={"margintop": "25px"},
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


# creates layout
def create_layout():
    """Creates the layout for the dashboard"""
    return dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        className="mb-4",
                        children=[
                            dbc.Row(
                                children=[
                                    html.Div(
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
                                ]
                            ),
                            dbc.Row(
                                children=[
                                    dbc.Col(create_data_type_dropdown(), width=1),
                                    dbc.Col(create_blog_choice_dropdown(), width=7),
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
            dcc.Store(id="language-store", data={"language": "english"}),
        ]
    )


layout = create_layout()
