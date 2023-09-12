from datetime import datetime

import dash


def news_artcle_div(
    title, published_date, technical_summary, non_technical_summary, link, language, article_source
):
    date_object = datetime.strptime(published_date, "%Y-%m-%d")
    formatted_date = date_object.strftime("%b %d, %Y")

    article_source_prefix = "by" if language == "english" else "av"
    collapsible_label = (
        "Show Non-Technical Summary"
        if language == "english"
        else "Visa Icke-Teknisk Sammanfattning"
    )
    published_on_label = "Published On" if language == "english" else "Publicerad"
    link_label = "Read more..." if language == "english" else "Läs mer här på engelska..."

    collapsible_summary = dash.html.Details(
        [
            dash.html.Summary(collapsible_label, style={"fontWeight": "bold"}),
            dash.html.P(
                non_technical_summary,
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
            f"{published_on_label}: {formatted_date} {article_source_prefix} {article_source}",
            style={
                "fontSize": "16px",
                "fontFamily": "Roboto",
                "fontWeight": "900",
                "color": "teal",
            },
        ),
        dash.html.P(
            technical_summary,
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
        dash.html.Div(
            [
                dash.html.A(
                    f"{link_label}",
                    href=link,
                    target="_blank",
                    style={
                        "textDecoration": "none",
                        "textAlign": "left",
                        "fontFamily": "Roboto",
                        "color": "teal",
                    },
                )
            ],
            style={"textAlign": "right"},
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
