from bot.database.models.subscription import Subscription
from bot.utils.format_amount import format_amount

def format_subscription_message(subscription: Subscription, delta):
    subscription_date = subscription.start_at.__format__('%Y-%m-%d')
    amount_text = f'{format_amount(subscription.amount)} за подписку «{subscription.title}»'
    if delta == 0:
        return f'Сегодня будет списано {amount_text}!'
    elif delta == 1:
        return f'Завтра будет списано {amount_text}!'
    elif delta in [2]:
        return f'Через {abs(delta)} дня будет списано {amount_text}!'
    else:
        return f'{subscription_date} будет списано {amount_text}'
