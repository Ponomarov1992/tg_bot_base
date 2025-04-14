from itertools import batched
from string import Template

from telegram import KeyboardButton, ReplyKeyboardMarkup

from src import configs, messages


def make_main_menu_buttons() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(f'{messages.CONSULTATION_BTN_LABEL} ✍️')],
        [
            KeyboardButton(f'{messages.CONTACT_WITH_US_BTN_LABEL} 📞'),
            KeyboardButton(f'{messages.OUR_SOCIAL_NETWORKS_BTN_LABEL} 🌐'),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_template(template_name: str) -> Template:
    """Template name with extension"""
    template_file = configs.BASE_DIR / 'src' / 'templates' / template_name
    with open(template_file, 'r') as file:
        return Template(file.read())


def build_buttons(buttons: list[str], n_cols: int) -> list[list[str]]:
    """
    Build a list of buttons arranged in columns.

    Args:
        buttons (iterable): The buttons to arrange.
        n_cols (int): The number of columns.

    Returns:
        list[list[str]]: The arranged buttons.
    """
    menu = []
    for batch in batched(buttons, n_cols):
        batch = list(batch)
        menu.append(batch)

    return menu


def build_reply_menu(buttons: list, n_cols: int, additional_button: str = None) -> ReplyKeyboardMarkup:
    """
    Build a reply menu (ReplyKeyboardMarkup) with buttons arranged in columns and an optional additional button.

    Args:
        buttons (list): The buttons to arrange.
        n_cols (int): The number of columns.
        additional_button (str, optional): An additional button to add at the end. Defaults to None.

    Returns:
        ReplyKeyboardMarkup: The reply menu markup.
    """
    keyboard = build_buttons(buttons, n_cols)
    if additional_button:
        keyboard.append([additional_button])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


MAIN_MENU_BUTTONS = make_main_menu_buttons()
