# dwhandler

This is a wrapper script that implements a handler
for logging commands to send Discord webhooks.
For web applications running Django, it will additionally
provide some `request` information in the webhook embed.

It was originally written for use with
[OTIS-WEB](https://github.com/vEnhance/otis-web),
but I then found myself copy-pasting this code in other
Python web applications I was writing.
Hence this repository.

## Usage

1. This package needs the `requests` and `python-dotenv` packages.
2. Add this repository as a submodule of your project.
3. Import it using `from discord_webhook_handler import DiscordWebhookHandler`.
4. Add standard `logging` commands.

## PyPi

Right now, I am assuming I am the sole user of this package.
If any person other than me expresses interest in using this,
open an issue, and I will (eventually) submit it to PyPi.
