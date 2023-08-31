from newsfeed import download_blogs_from_rss


def test_import_project() -> None:
    print("Running test_import_project...")
    download_blogs_from_rss.main(blog_name="mit")
    print("Test completed.")


def test_imports():
    essential_modules = [
        "pydantic",
        "argparse",
        "requests",
        "newsfeed.download_blogs_from_rss",
        "dash",
        "dash_bootstrap_components",
        "pandas",
        "dash.dependencies",
        "bs4",
        "aiohttp",
        "discord",
        "openai",
        "tiktoken",
        "dotenv",
        "langchain",
    ]

    for module in essential_modules:
        try:
            __import__(module)
        except ImportError:
            assert False, f"Failed to import {module}"
