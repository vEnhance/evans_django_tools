import logging
import os
import sys
import unittest

from .handler import DiscordWebhookHandler, truncate


class TestLogger(unittest.TestCase):
    def test_short_log(self):
        handler = DiscordWebhookHandler()
        factory = logging.getLogRecordFactory()
        msg = "You. This is a warning. Isn't that bad?"
        args = ()
        try:
            raise ValueError("HEY! Watch where you're going!")
        except ValueError:
            record = factory(
                __name__, logging.WARNING, "test_logger", 11, msg, args, sys.exc_info()
            )
            payload = handler.get_payload(record)
            self.assertLessEqual(len(payload["embeds"][0]["description"]), 2000)
            resp = handler.post_response(record)
        if os.getenv("WEBHOOK_URL") is not None:
            resp = handler.post_response(record)
            assert resp is not None
            self.assertLessEqual(resp.status_code, 299)

    def test_truncate(self):
        self.assertLess(len(truncate("aoeu" * 1000, 800)), 820)

    def test_long_log(self):
        handler = DiscordWebhookHandler()
        factory = logging.getLogRecordFactory()
        msg = "Whoa. Another warning. But this one is really long!\n" * 1000
        args = ()
        try:
            raise ValueError("OH NO. Your code is playing possum. WHY?\n" * 500)
        except ValueError:
            record = factory(
                __name__, logging.WARNING, "test_logger", 99, msg, args, sys.exc_info()
            )
            payload = handler.get_payload(record)
            self.assertLessEqual(len(payload["embeds"][0]["description"]), 2000)
            if os.getenv("WEBHOOK_URL") is not None:
                resp = handler.post_response(record)
                assert resp is not None
                self.assertLessEqual(resp.status_code, 299)
