import logging
import os
import pprint
import socket
from collections import OrderedDict
from typing import Any, Optional, TypedDict

import requests
from dotenv import load_dotenv

VERBOSE_LOG_LEVEL = 15
SUCCESS_LOG_LEVEL = 25
ACTION_LOG_LEVEL = 35
logging.addLevelName(VERBOSE_LOG_LEVEL, "VERBOSE")
logging.addLevelName(SUCCESS_LOG_LEVEL, "SUCCESS")
logging.addLevelName(ACTION_LOG_LEVEL, "ACTION")

load_dotenv()

COLORS = {
    "default": 2040357,
    "error": 14362664,
    "critical": 14362664,
    "warning": 16497928,
    "info": 2196944,
    "verbose": 6559689,
    "debug": 2196944,
    "success": 2210373,
    "action": 17663,
}
EMOJIS = {
    "default": ":loudspeaker:",
    "error": ":x:",
    "critical": ":skull_crossbones:",
    "warning": ":warning:",
    "info": ":bell:",
    "verbose": ":mega:",
    "debug": ":microscope:",
    "success": ":rocket:",
    "action": ":factory_worker:",
}


def truncate(s: str, n: int = 800) -> str:
    if len(s) > n:
        return s[: n // 2] + "\n...\n" + s[-n // 2 :]
    return s


class Payload(TypedDict):
    username: str
    embeds: list[dict[str, Any]]


class DiscordWebhookHandler(logging.Handler):
    def get_payload(self, record: logging.LogRecord) -> Payload:
        self.format(record)
        level = record.levelname.lower().strip()
        emoji = EMOJIS.get(level, ":question:")
        color = COLORS.get(level, 0xAAAAAA)

        # this only works in django
        try:
            user = record.request.user.first_name + " " + record.request.user.last_name  # type: ignore
        except AttributeError:
            user = "anonymous"
        s = str(getattr(record, "status_code", ""))
        if s:
            s = "**" + s + "**"
        else:
            s = "None"

        fields = [
            {
                "name": "Status",
                "value": s,
                "inline": True,
            },
            {
                "name": "Level",
                "value": record.levelname.title(),
                "inline": True,
            },
            {
                "name": "Scope",
                "value": f"`{record.name}`",
                "inline": True,
            },
            {
                "name": "Module",
                "value": f"`{record.module}`",
                "inline": True,
            },
            {
                "name": "User",
                "value": user,
                "inline": True,
            },
            {
                "name": "Filename",
                "value": f"{record.lineno}:`{record.filename}`",
                "inline": True,
            },
        ]

        description_parts = OrderedDict()

        # if the message is short (< 1 line), we set it as the title
        if "\n" not in record.message:
            title = f"{emoji} {record.message[:200]}"
        # otherwise, set the first line as title and include the rest in description
        else:
            i = record.message.index("\n")
            title = f"{emoji} {record.message[:i]}"
            msg_key = ":green_heart: MESSAGE :green_heart:"
            description_parts[msg_key] = truncate(record.message[i + 1 :])

        # if exc_text nonempty, add that to description
        if record.exc_text is not None:
            # always truncate r.exc_text to at most 600 chars since it's fking long
            msg_key = ":yellow_heart: EXCEPTION :yellow_heart:"
            description_parts[msg_key] = truncate(record.exc_text)

        # if request data is there, include that too
        if hasattr(record, "request"):
            request = getattr(record, "request")
            s = ""
            s += f"> **Method** {request.method}\n"
            s += f"> **Path** `{request.path}`\n"
            s += f"> **Content Type** {request.content_type}\n"
            s += f'> **Agent** {request.headers.get("User-Agent", "Unknown")}\n'
            if request.user.is_authenticated:
                s += f'> **User** {getattr(request.user, "username", "wtf")}\n'
            if request.method == "POST":
                # redact the token for evan's personal api
                d: dict[str, Any] = {}
                for k, v in request.POST.items():
                    if k == "token" or k == "password":
                        d[k] = "<redacted>"
                    else:
                        d[k] = v
                s += r"POST data" + "\n"
                s += r"```" + "\n"
                pp = pprint.PrettyPrinter(indent=2)
                s += pp.pformat(d)
                s += r"```"
            if request.FILES is not None and len(request.FILES) > 0:
                s += "Files included\n"
                for name, fileobj in request.FILES.items():
                    s += (
                        f"> `{name}` ({fileobj.size} bytes, { fileobj.content_type })\n"
                    )

            chars_remaining = 1800 - sum(len(v) for v in description_parts.values())
            description_parts[":blue_heart: REQUEST :blue_heart:"] = s[:chars_remaining]

        embed = {"title": title, "color": color, "fields": fields}

        desc = ""
        for k, v in description_parts.items():
            desc += k + "\n" + v.strip() + "\n"
        if desc:
            embed["description"] = desc

        data: Payload = {
            "username": socket.gethostname(),
            "embeds": [embed],
        }
        return data

    def get_url(self, record: logging.LogRecord) -> Optional[str]:
        return os.getenv(
            f"WEBHOOK_URL_{record.levelname.upper()}", os.getenv("WEBHOOK_URL")
        )

    def post_response(self, record: logging.LogRecord) -> Optional[requests.Response]:
        data = self.get_payload(record)
        url = self.get_url(record)
        if url is not None:
            return requests.post(url, json=data)
        else:
            return None

    def emit(self, record: logging.LogRecord):
        self.post_response(record)
