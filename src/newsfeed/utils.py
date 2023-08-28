import argparse


def parse_args():
    # Parse command-line arguments for sending summaries to Discord.
    # Returns a Namespace object with the parsed arguments.

    parser = argparse.ArgumentParser(description="Enables running scripts in the terminal")
    parser.add_argument("--blog_name", type=str, help="Name of the specific blog source")
    return parser.parse_args()
