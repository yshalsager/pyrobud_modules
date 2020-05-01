"""
Android module for pyrobud userbot
Author: yshalsager <ysh-alsager@hotmail.com>

This module is used to:
- Get Magisk Latest download links
- Search an Android device's codename
- Get an Android device's information
- Get an Android device's specifications

Dependencies: beautifulsoup4
"""
import json
import re

from bs4 import BeautifulSoup

from pyrobud import command, module


class AndroidModule(module.Module):
    name: str = "Android Tools"
    disabled: bool = False

    @command.desc("Get latest magisk releases")
    @command.alias("ma")
    async def cmd_magisk(self, ctx: command.Context):
        await ctx.respond("Processing...")

        url: str = 'https://raw.githubusercontent.com/topjohnwu/magisk_files'
        releases: str = '**Latest Magisk Releases:**\n\n'
        for variant in ['master/stable', 'master/beta', 'canary/release', 'canary/debug']:
            async with self.bot.http.get(
                    f"{url}/{variant}.json") as resp:
                data: dict = json.loads(await resp.text())
                name: str = variant.split('_')[0].capitalize()
                releases += f'**{name}**: [ZIP v{data["magisk"]["version"]}]' \
                            f'({data["magisk"]["link"]}) | ' \
                            f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | ' \
                            f'[Uninstaller]({data["uninstaller"]["link"]})\n'
        return releases

    @command.desc("Search Android device name")
    @command.usage("[codename]", reply=True)
    async def cmd_device(self, ctx: command.Context):
        await ctx.respond("Processing...")

        codename = ctx.segments[1]
        reply: str = f"**Search results for {codename}**:\n\n"
        async with self.bot.http.get(
                "https://raw.githubusercontent.com/androidtrackers/"
                "certified-android-devices/master/by_device.json") as resp:
            data: dict = json.loads(await resp.text())
            results: list = data.get(codename)
            if results:
                for item in results:
                    reply += f"**Brand**: {item['brand']}\n" \
                             f"**Name**: {item['name']}\n" \
                             f"**Model**: {item['model']}\n\n"
            else:
                reply += "None\n"
            return reply

    @command.desc("Search Android device codename")
    @command.usage("[brand name]", reply=True)
    async def cmd_codename(self, ctx: command.Context):
        await ctx.respond("Processing...")

        if len(ctx.segments) >= 3:
            brand: str = ctx.segments[1]
            device: str = ' '.join(ctx.segments[2:])
        else:
            return "Some parameters are missing. Read the usage!"

        reply: str = f"**Search results for {brand} {device}**:\n\n"
        async with self.bot.http.get(
                "https://raw.githubusercontent.com/androidtrackers/"
                "certified-android-devices/master/by_brand.json") as resp:
            data: dict = json.loads(await resp.text())
            devices: list = data.get(brand)
            results: list = [i for i in devices
                             if i["name"].lower() == device.lower()
                             or i["model"] == device.lower()]
            if results:
                if len(results) > 8:
                    results = results[:8]
                for item in results:
                    reply += f"**Device**: {item['device']}\n" \
                             f"**Name**: {item['name']}\n" \
                             f"**Model**: {item['model']}\n\n"
            else:
                reply += "None\n"
            return reply

    @command.desc("Search Android device specifications")
    @command.usage("[search query]", reply=True)
    async def cmd_specs(self, ctx: command.Context) -> str:
        await ctx.respond("Processing...")

        brand: str = ctx.segments[1]
        query: str = ' '.join(ctx.segments[2:])
        reply: str = f"**Search results for {query}**:\n\n"

        async with self.bot.http.get(
                "https://www.devicespecifications.com/en/brand-more") as resp:
            brands: list = BeautifulSoup(await resp.text(), 'html.parser').find('div', {
                'class': 'brand-listing-container-news'}).findAll('a')
            try:
                brand_page_url: str = [i['href'] for i in brands
                                       if brand.lower() == i.text.strip().lower()][0]
            except IndexError:
                return f"`Can't find information about {brand}!`"

        async with self.bot.http.get(brand_page_url) as resp:
            devices: list = BeautifulSoup(await resp.text(), 'html.parser').findAll(
                'div', {'class': 'model-listing-container-80'})
            try:
                device_page_url: list = [
                    i.a['href']
                    for i in BeautifulSoup(str(devices), 'html.parser').findAll('h3')
                    if query in i.text.strip().lower()]
            except IndexError:
                return f"`can't find information about {query}!`"

        if len(device_page_url) > 2:
            device_page_url = device_page_url[:2]
        for url in device_page_url:
            async with self.bot.http.get(url) as resp:
                info: BeautifulSoup = BeautifulSoup(await resp.text(), 'html.parser')
                reply: str = '\n' + info.title.text.split('-')[0].strip() + '\n'
                info: BeautifulSoup = info.find('div', {'id': 'model-brief-specifications'})
                specifications: list = re.findall(r'<b>.*?<br/>', str(info))
                for item in specifications:
                    title: str = re.findall(r'<b>(.*?)</b>', item)[0].strip()
                    data: str = re.findall(r'</b>: (.*?)<br/>', item)[0] \
                        .replace('<b>', '').replace('</b>', '').strip()
                    reply += f'**{title}**: {data}\n'
        return reply
