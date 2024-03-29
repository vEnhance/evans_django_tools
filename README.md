# evans_django_tools

This is a submodule containing a bunch of stuff that I use between multiple
Django projects.
Things here were originally written for use with
[OTIS-WEB](https://github.com/vEnhance/otis-web),
but I then found myself copy-pasting this code in other
Python web applications I was writing. Hence this repository.

(Right now, I am assuming I am the sole user of this package.
If any person other than me expresses interest in using this,
open an issue, and I will (eventually) submit it to PyPi.)

## Discord webhook handler

This is a wrapper script that implements a handler
for logging commands to send Discord webhooks.
For web applications running Django, it will additionally
provide some `request` information in the webhook embed.

1. This package needs the `requests` and `python-dotenv` packages.
2. Add this repository as a submodule of your project.
3. Import it using `from evans_django_tools import DiscordWebhookHandler`.
4. Add standard `logging` commands. For example,

   ```python
   import logging
   from evans_django_tools import DiscordWebhookHandler

   logger = logging.getLogger('root')
   logger.setLevel(logging.INFO)
   logger.addHandler(DiscordWebhookHandler())
   logger.addHandler(logging.StreamHandler())
   ```

5. You should set environment variable `WEBHOOK_URL` to the target webhook URL.
6. If you want different channels for different error levels,
   use `WEBHOOK_CRITICAL_URL`, `WEBHOOK_ERROR_URL`, etc.
   Otherwise `WEBHOOK_URL` is used by default.
7. The package adds three new log levels: `VERBOSE_LOG_LEVEL = 15`,
   `SUCCESS_LOG_LEVEL = 25`, `ACTION_LOG_LEVEL = 35`.

## Test suite

The file `evans_django_tools/testsuite.py` has a bunch of homemade helper
functions for writing Django tests.

## Bash scripts for local checks

To use the `lint.sh` automatically on `git push`, create an executable file
`.git/hooks/pre-push` with content `./evans_django_tools/lint.sh`.
This will run the `lint.sh` script automatically before pushing anything (and
abort the push if any issues are detected).

Running `./evans_django_tools/bypass-lint.sh` causes
`./evans_django_tools/lint.sh` to do nothing for the current commit, hence the
name.

## GitHub workflow

This repository has a Github reusable workflow that you can use that runs
essentially the same checks as `lint.sh`. To use it, create
`.github/workflows/django-audit.yml` in your main repository and include
something like the following:

```yaml
name: Django Audit

on:
  push:
    branches: ["*"]
  pull_request:
    branches: ["*"]
jobs:
  audit:
    uses: vEnhance/evans_django_tools/.github/workflows/django-audit.yml@main
```
