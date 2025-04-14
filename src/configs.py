import os
from pathlib import Path

from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent  # root directory of the project
BOT_TOKEN = os.getenv('BOT_TOKEN')
CRM_API_TOKEN = os.getenv('CRM_API_TOKEN')
CRM_API_URL = os.getenv('CRM_API_URL', 'http://localhost:8000')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# for templates
TELEGRAM_CONTACT_URL = os.getenv('TELEGRAM_CONTACT_URL', 'https://t.me/')
WHATSAPP_CONTACT_URL = os.getenv('WHATSAPP_CONTACT_URL', 'https://whatsapp.com/')
INSTAGRAM_URL = os.getenv('INSTAGRAM_URL', 'https://www.instagram.com/topinteriordesignllc/')
WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://top-interior-design.com/')
FACEBOOK_URL = os.getenv('FACEBOOK_URL', 'https://www.facebook.com/profile.php?id=61559231076337')

if not BOT_TOKEN and not CRM_API_TOKEN:
    raise ValueError('You must provide BOT_TOKEN and CRM_API_TOKEN in the environment variables')

logger.add(BASE_DIR / 'logs' / 'logs.log', level='DEBUG', rotation='100 MB', compression='zip')
