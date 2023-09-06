import asyncio
import hashlib
import json
from pathlib import Path

import aiohttp
from discord import AsyncWebhookAdapter, Webhook

from newsfeed import utils

# webhook_url = "https://discord.com/api/webhooks/1131522847509069874/Lwk1yVc4w623xpRPkKYu9faFdMNvV5HTZ3TCcL5DgsIgeqhEvo9tBookvuh2S4IWysTt"
webhook_url = "https://discord.com/api/webhooks/1143986724867940452/dkS0pJmG-qQwDoqVJrmrFSOLyXB4gAq7pSfYE74FG1bPmEp_dAuRoaHIzgdkImSFU5dE"


# This function gets articles from a folder when called and the specific folder is sent in the function
async def get_articles_from_folder(folder_path):
    # This line just checks if the path to the folder sent in as input exist and if it doesnt, an empty list is returned
    if not folder_path.exists():
        raise FileNotFoundError(f"Directory {folder_path} does not exist.")

    # This line iterates throght each item in the folder and adds every file that is a json
    # into the json_files
    json_files = [file for file in folder_path.iterdir() if file.suffix == ".json"]

    # Each json is read and parsed into a python object using json.load and then added into articles list
    articles = []
    for json_file in json_files:
        with open(json_file) as f:
            loaded_json = json.load(f)
            articles.append(loaded_json)

    return articles


# The function below formats each summary item that will sent to discord to have
# the format seen below in message_content
def format_summary_message(summary_item, group_name):
    technical_summary = summary_item.get("blog_summary_technical")
    non_technical_summary = summary_item.get("blog_summary_non_technical")
    blog_title = summary_item.get("title")

    if non_technical_summary is None or blog_title is None or technical_summary is None:
        raise ValueError("Article missing a title or blog summary")

    formatted_non_tech_summary_item = non_technical_summary.replace(".\n", ".\n> ")
    formatted_tech_summary_item = technical_summary.replace(".\n", ".\n> ")

    message_content = (
        f"🔔 **Article Alert from {group_name}** 🔔\n\n"
        f"📰 **Blog Title:** \n> {blog_title}\n\n"
        f"▶️ **Technical Summary:**\n> {formatted_tech_summary_item}\n\n"
        f"▶️ **Non-Technical Summary:**\n> {formatted_non_tech_summary_item}\n\n"
    )
    return message_content


# function that truncates the summary to 2000 characters, otherwise discord will give us an error
def truncate_string(input_str, max_len=2000):
    if len(input_str) > max_len:
        input_str = (
            input_str[: max_len - 3] + "..."
        )  # removes the last 3 characters and replaces them with "..."
    return input_str


# Explanations of hash_summary, read_sent_log, write_sent_log and send_summary_to_discord are in: tests/only_new_summaries_explained.py
# generates a hash for each summary (that goes into the sent log)
def hash_summary(summary):
    return hashlib.sha256(json.dumps(summary, sort_keys=True).encode()).hexdigest()


# reads the sent log file
def read_sent_log():
    try:
        with open("sent_log.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# writes to the sent log file
def write_sent_log(sent_log):
    with open("sent_log.json", "w") as f:
        json.dump(sent_log, f)


# This async function first uses the aiohttp.ClientSession to create an http session
# Then a webhook is created with an asynchronous adapter
# The summaries are loop through then sent to the discord webhook chanel
async def send_summary_to_discord(blog_name):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
        folder_path = (
            Path(__file__).parent.parent.parent / f"data/data_warehouse/{blog_name}/summaries"
        )
        group_name = "Midjourney"
        summaries = await get_articles_from_folder(folder_path)
        sent_log = read_sent_log()

        for summary in summaries:
            summary_hash = hash_summary(summary)

            # If summary is not in hash, then it goes through this if statement
            if summary_hash not in sent_log:
                message_content = format_summary_message(summary, group_name)
                message_content = truncate_string(
                    message_content
                )  # Runs message through truncate function, making sure it is less than 2000 characters
                await webhook.send(
                    content=message_content
                )  # Only sends message within this if-statement

                sent_log.append(summary_hash)
                write_sent_log(sent_log)
                await asyncio.sleep(1)


def main(blog_name):
    print(f"Starting to send summaries for {blog_name}...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_summary_to_discord(blog_name=blog_name))
    print(f"Done sending summaries for {blog_name}")


if __name__ == "__main__":
    args = utils.parse_args()
    main(blog_name=args.blog_name)
