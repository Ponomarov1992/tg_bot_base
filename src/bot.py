from telegram import Update, ext
from telegram.ext import CommandHandler, MessageHandler, filters

from src import messages
from src.commands import base, start_cmd
from src.commands.consultation import CONSULTATION_CH
from src.configs import BOT_TOKEN, logger


def main() -> None:
    application = ext.Application.builder().token(BOT_TOKEN).build()
    application.add_handler(start_cmd.GET_CONTACT_CH)
    application.add_handler(CommandHandler('menu', base.menu_cmd))
    application.add_handler(CONSULTATION_CH)
    application.add_handler(
        MessageHandler(filters=filters.Regex(rf'^{messages.CONTACT_WITH_US_BTN_LABEL}'), callback=base.contact_with_us)
    )
    application.add_handler(
        MessageHandler(
            filters=filters.Regex(rf'^{messages.OUR_SOCIAL_NETWORKS_BTN_LABEL}'), callback=base.our_social_networks
        )
    )

    try:
        logger.info('Bot is running')
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info('Bot is stopping')
        application.stop_running()
