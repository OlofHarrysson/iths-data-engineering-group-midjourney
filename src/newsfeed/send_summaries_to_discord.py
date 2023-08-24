import asyncio
import json
from pathlib import Path

import aiohttp
from discord import AsyncWebhookAdapter, Webhook

# webhook_url = "https://discord.com/api/webhooks/1131522847509069874/Lwk1yVc4w623xpRPkKYu9faFdMNvV5HTZ3TCcL5DgsIgeqhEvo9tBookvuh2S4IWysTt"
webhook_url = "https://discord.com/api/webhooks/1143986724867940452/dkS0pJmG-qQwDoqVJrmrFSOLyXB4gAq7pSfYE74FG1bPmEp_dAuRoaHIzgdkImSFU5dE"


async def get_articles_from_folder(folder_path):
    if not folder_path.exists():
        print(f"Directory {folder_path} does not exist.")
        return []
    json_files = [file for file in folder_path.iterdir() if file.suffix == ".json"]
    articles = []
    for json_file in json_files:
        with open(json_file) as f:
            articles.append(json.load(f))
    return articles


def format_summary_message(article, group_name):
    blog_title = article.get("title", "N/A")
    timestamp = article.get("timestamp", "N/A")
    link = article.get("link", "N/A")
    summary = article.get("description", "N/A")
    formatted_summary = summary.replace(".\n", ".\n> ")
    message_content = (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📁 **__Group Name:__**\n• {group_name}\n\n"
        f"📰 **__Blog Title:__**\n• {blog_title}\n\n"
        f"▶️ **__New Article Summary:__**\n\n> {formatted_summary}\n\n"
        f"🔗 **Link** {link}\n"
    )
    return message_content


async def send_summary_to_discord():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
        current_path = Path.cwd()
        folder_path = current_path.parent.parent / "data/data_warehouse/mit/articles"
        group_name = "Midjourney"

        articles = await get_articles_from_folder(folder_path)
        for article in articles:
            message_content = format_summary_message(article, group_name)
            await webhook.send(content=message_content)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_summary_to_discord())
