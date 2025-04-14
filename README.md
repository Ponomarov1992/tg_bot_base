# README #

Telegram bot for TID [CRM](https://bitbucket.org/tid-project/crm) project.

### Requirements ###
- Python 3.12
- [python-telegram-bot](https://docs.python-telegram-bot.org/en/latest/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [loguru](https://github.com/Delgan/loguru)

### Local development ###
1. Install dependencies: `pip install -r requirements-dev.txt`
2. Install pre-commit hooks: `pre-commit install`
3. Create `.env` file with environment variables (see `.env.example`)
4. Run bot: `make run-bot` or `python -m src`

### Environment variables ###
See `.env.example` file for environment variables that should be set:

- `BOT_TOKEN` - Telegram bot token
- `CRM_API_TOKEN` - CRM API token
- `CRM_API_URL` - CRM API URL
- `DEBUG` - Debug mode (default: `False`), enable via `DEBUG=True`
