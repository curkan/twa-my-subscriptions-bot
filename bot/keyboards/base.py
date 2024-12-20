from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class BaseKeyboard:
    def __init__(self):
        self.keyboard = []

    def add_button(self, text, callback_data):
        self.keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    def get_markup(self):
        return InlineKeyboardMarkup(self.keyboard)
