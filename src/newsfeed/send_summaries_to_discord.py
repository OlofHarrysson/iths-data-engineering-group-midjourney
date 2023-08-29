import asyncio
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
        print(f"Directory {folder_path} does not exist.")
        return []

    # This line iterates throght each item in the folder and adds every file that is a json
    # into the json_files
    json_files = [file for file in folder_path.iterdir() if file.suffix == ".json"]

    # Each json is read and parsed into a python object using json.load and then added into articles list
    articles = []
    for json_file in json_files:
        with open(json_file) as f:
            articles.append(json.load(f))
    return articles


# The function below formats each summary item that will sent to discord to have
# the format seen below in message_content
def format_summary_message(summary_item, group_name):
    blog_title = summary_item.get("title", "N/A")
    summary_item = summary_item.get("blog_summary", "N/A")
    formatted_summary_item = summary_item.replace(".\n", ".\n> ")

    message_content = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔔 **New Article Alert from {group_name}** 🔔\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📁 **Group Name:** \n> {group_name}\n\n"
        f"📰 **Blog Title:** \n> {blog_title}\n\n"
        f"▶️ **New Article Summary:**\n\n> {formatted_summary_item}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    return message_content


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
        for summary in summaries:
            message_content = format_summary_message(summary, group_name)
            await webhook.send(content=message_content)


if __name__ == "__main__":
    args = utils.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_summary_to_discord(blog_name=args.blog_name))
