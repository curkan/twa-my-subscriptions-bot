from .base import BaseKeyboard

class NotificationKeyboard(BaseKeyboard):
    def __init__(self):
        super().__init__()
        self.add_button("Уже оплачено", "paid")
        self.add_button("Отключить оповещения по этой подписке", "disable_notification")
