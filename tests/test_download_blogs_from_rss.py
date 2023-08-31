from newsfeed import download_blogs_from_rss


def test_import_project() -> None:
    print("Running test_import_project...")
    download_blogs_from_rss.main(blog_name="mit")
    print("Test completed.")


def test_imports():
    essential_modules = [
        "datetime",
        "pydantic",
        "argparse",
        "pathlib",
        "requests",
        "sys",
        "newsfeed.download_blogs_from_rss",
    ]

    for module in essential_modules:
        try:
            __import__(module)
        except ImportError:
            assert False, f"Failed to import {module}"
