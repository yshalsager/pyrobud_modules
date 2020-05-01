"""
Articles Scraper Module for pyrobud userbot
Author: yshalsager <ysh-alsager@hotmail.com>

This module is used to get the content of an article without leaving Telegram.

Dependencies: newspaper3k
"""
import re

from newspaper import Article, ArticleException

from pyrobud import command, module


class ArticlesModule(module.Module):
    name: str = "Articles Scraper"
    disabled: bool = False
    regex: str = r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.' \
                 r'[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*))'

    @command.desc("Scrap article content")
    @command.alias("con")
    @command.usage("[url]", reply=True)
    async def cmd_content(self, ctx: command.Context) -> str:
        url: str = ctx.input or ctx.segments[1]
        url: str = re.search(self.regex, url).group(1)
        article: Article = Article(url)
        try:
            article.download()
            article.parse()
            await ctx.respond(f"**{article.title}**\n{article.publish_date}\n\n{article.text}",
                              overflow="split")
        except ArticleException:
            return "Failed to scrape the article!"
