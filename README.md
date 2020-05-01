# Pyrobud Custom Modules

This repository contains my custom [pyrobud](https://github.com/kdrag0n/pyrobud) modules.



## How to use?

- Clone the repository to `pyrobud/pyrobud/custom_modules`

- Install dependencies using `pip install -r requirements.txt`



## Available modules:

### Android stuff:

A collection of scrapers that allows you to:

- Get Magisk Latest download links.

- Search an Android device's codename.

- Get an Android device's information.

- Get an Android device's specifications.

### Currency Converter:

A small module for getting the exchange rate of different currencies. Ported from [skittles9823's Paperplane module](https://github.com/RaphielGang/Telegram-Paperplane/commit/bdcea6116ec3c843297e6fdc0e58911656089401).

#### Note:

To use this module you must get an API key from https://free.currconv.com, the add a section to the userbot config.toml file like this:

```toml
[currency_converter]
api_key = "0000000000xxxxx"
```

### Articles Scraper

A module to get the content of an article without leaving Telegram, using [newspaper3k](https://github.com/codelucas/newspaper).
