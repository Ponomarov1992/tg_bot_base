from telegram import Contact, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from src import messages, services, utils
from src.api import API


GET_USER_CONTACT = 1


async def request_user_contact_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tg_id = update.effective_user.id

    user = await services.get_user_by_tg_id(tg_id)

    if user:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=messages.USER_ALREADY_EXISTS, reply_markup=utils.MAIN_MENU_BUTTONS
        )
        return ConversationHandler.END

    contact_button = KeyboardButton(messages.SEND_CONTACT_LABEL, request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
    await context.bot.send_message(chat_id=tg_id, text=messages.SEND_CONTACT_FOR_USING_BOT, reply_markup=reply_markup)

    return GET_USER_CONTACT


async def request_user_contact_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact: Contact = update.message.contact
    user = update.effective_user
    user_data = {
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'phone_number': contact.phone_number,
        'telegram_data': {
            'tg_id': update.effective_user.id,
            'username': user.username,
            'language_code': user.language_code,
        },
    }

    is_success, resp_data = await API.create_client(user_data)
    if not is_success:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.ERROR_WHILE_CREATING_USER)
        return ConversationHandler.END

    if is_success:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=messages.USER_HAS_REGISTERED, reply_markup=utils.MAIN_MENU_BUTTONS
        )

    return ConversationHandler.END


GET_CONTACT_CH = ConversationHandler(
    allow_reentry=True,
    entry_points=[CommandHandler('start', request_user_contact_start)],
    states={GET_USER_CONTACT: [MessageHandler(filters.CONTACT, request_user_contact_end)]},
)
