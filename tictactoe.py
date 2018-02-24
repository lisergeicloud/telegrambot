import telegram
from telegram import InlineKeyboardMarkup


def get_reply(board_size):
    buttons = []
    for i in range(0, board_size * board_size, board_size):
        row = [telegram.InlineKeyboardButton(' ', callback_data=str(i + x)) for x in range(board_size)]
        buttons.append(row)
    return buttons
