from newsfeed.dashboard import get_news_data


def test_get_news_data_source_mit():
    df = get_news_data(news_blog_source="mit")
    # checks that the source column exists in the dataframe.
    assert "source" in df.columns
    # checks that all rows in the source column are "mit".
    assert all(df["source"] == "mit")


def test_get_news_data_source_google_ai():
    df = get_news_data(news_blog_source="google_ai")
    assert "source" in df.columns
    assert all(df["source"] == "google_ai")


def test_get_news_data_source_ai_blog():
    df = get_news_data(news_blog_source="ai_blog")
    assert "source" in df.columns
    assert all(df["source"] == "ai_blog")


def test_get_news_data_source_all_blogs():
    df = get_news_data(news_blog_source="all_blogs")
    assert "source" in df.columns
    assert set(df["source"].unique()) == {"mit", "google_ai", "ai_blog"}
