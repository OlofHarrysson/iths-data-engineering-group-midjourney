from datetime import datetime

import dash


def news_artcle_div(title, published_date, summary, ntsummary, link):
    date_object = datetime.strptime(published_date, "%Y-%m-%d")
    formatted_date = date_object.strftime("%b %d, %Y")

    collapsible_summary = dash.html.Details(
        [
            dash.html.Summary("Show Non-Technical Summary", style={"fontWeight": "bold"}),
            dash.html.P(
                ntsummary,
                style={
                    "margin": "10px 0",
                    "textAlign": "left",
                    "fontFamily": "Roboto",
                    "fontSize": "16",
                    "fontWeight": "400",
                    "lineHeight": "1.4",
                },
            ),
        ]
    )

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
        collapsible_summary,
        dash.html.A(
            href=link,
            target="_blank",
            style={
                "textDecoration": "underline",
                "textAlign": "left",
                "fontFamily": "Roboto",
                "color": "teal",
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
    return {"date": date_object, "div": dash.html.Div(div, style={"padding": "10px"})}


def title_heading_for_dashboard(heading: str):
    heading = dash.html.Div(
        [
            dash.html.H1(
                heading,
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
    return heading


def dashboard_content_container(children):
    content = dash.html.Div(children=children)
    return content
