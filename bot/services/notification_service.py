from bot.keyboards.notification_keyboard import NotificationKeyboard

class NotificationService:
    def __init__(self):
        self.keyboard = NotificationKeyboard()

    def get_notification_keyboard(self):
        return self.keyboard.get_markup()
