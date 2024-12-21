import logging

from telegram._utils.types import ReplyMarkup
from bot.services.notification_service import NotificationService
from bot.utils.format_amount import format_amount
from bot.utils.format_subscription_message import format_subscription_message
from sqlalchemy import Date, and_, create_engine, extract, func, or_
from telegram.constants import ParseMode
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler
from telegram.helpers import escape_markdown
import datetime

from bot.core.config import Settings, parse_settings
from bot.database.models.subscription import Subscription

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет! Запустите приложение через меню. О подписках я буду сообщать заранее.')

async def send_notifications(context: ContextTypes.DEFAULT_TYPE) -> None:
    engine = create_engine(str(config.postgres.dsn))
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    Session = sessionmaker(bind=engine)
    session = Session()

    today = datetime.date.today()

    query = select(
        Subscription,
        (extract('day', Subscription.start_at)).label('day_to_start')
    ).filter(
        and_(
            or_(
                Subscription.latest_notify_at < today,
                Subscription.latest_notify_at == None
            ),
            or_(
                # and_(
                #     Subscription.period == 'annualy',
                #     extract('month', Subscription.start_at) == today.month - 1,
                #     extract('day', Subscription.start_at) >= today.day - 2
                # ),
                and_(
                    Subscription.period == 'monthly',
                    or_(
                        func.extract('day', Subscription.start_at) == today.day,
                        func.extract('day', Subscription.start_at) == (today + datetime.timedelta(days=1)).day,
                        func.extract('day', Subscription.start_at) == (today + datetime.timedelta(days=2)).day,
                    ),
                ),
                and_(
                    Subscription.period == 'weekly',
                    (extract('day', Subscription.start_at - today) % 7).between(0, 2)
                )
            )
        )
    )

    subs = session.scalars(query)

    # notification_service = NotificationService()
    # reply_markup = notification_service.get_notification_keyboard()
    subs = session.execute(query).all()

    for subscription in subs:
        logging.info(f'delta: {subscription[1]}')
        today_day = datetime.date.today().day

        message = format_subscription_message(subscription[0], subscription[1] - today_day)
        message = f"*{message}*"

        await context.bot.send_message(chat_id=subscription[0].user_id, text=message, parse_mode=ParseMode.MARKDOWN)
        subscription[0].latest_notify_at = datetime.datetime.now(datetime.timezone.utc)
        session.add(subscription[0])
        session.commit()

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed

    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.answer(text=f"Selected option: {query.data}")
    # await query.edit_message_text(text=f"Selected option: {query.data}")

if __name__ == '__main__':
    config: Settings = parse_settings()
    application = ApplicationBuilder().token(config.bot.token).build()
    
    start_handler = CommandHandler('start', start)
    # application.add_handler(CommandHandler('interval', set_reminder_interval))
    application.add_handler(start_handler)
    # application.add_handler(CallbackQueryHandler(button))

    application.job_queue.run_repeating(send_notifications, interval=getattr(config.bot, 'interval_jobs', 300), first=0)
    
    application.run_polling()
