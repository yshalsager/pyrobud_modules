"""
Currency Converter Module for pyrobud userbot
Author: yshalsager <ysh-alsager@hotmail.com>

This module is used to get the exchange rate of different currencies.

How to configure:
- Get an API key from https://free.currconv.com
- Add a section to the userbot config.toml file like this:

[currency_converter]
api_key = "0000000000xxxxx"
"""
import asyncio

from pyrobud import command, module


class CurrencyModule(module.Module):
    name: str = "Currency Converter"
    disabled: bool = False

    async def on_load(self) -> None:
        self.api_key: str = self.bot.config['currency_converter']['api_key']

    @command.desc("Get currency conversion rate")
    @command.alias("currency")
    @command.usage("[amount currency_from currency_to]", reply=True)
    async def cmd_cr(self, ctx: command.Context) -> str:
        if not self.api_key:
            return "No API key provided!"

        await ctx.respond("Processing...")
        await asyncio.sleep(1)

        if len(ctx.segments) == 4:
            amount: str = ctx.segments[1]
            currency_from: str = ctx.segments[2].upper()
            currency_to: str = ctx.segments[3].upper()
        else:
            return "Some parameters are missing. Read the usage!"

        async with self.bot.http.get(
                f"https://free.currconv.com/api/v7/convert?apiKey={self.api_key}&q="
                f"{currency_from}_{currency_to}&compact=ultra") as resp:
            json: dict = await resp.json()
            value: float = json[f'{currency_from}_{currency_to}']
            result: round = round(float(amount) * value, 5)
            return f"**{amount} {currency_from}** is: **{result} {currency_to}**"
