from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import BIGINT,VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE
from sqlalchemy.types import DATE, DATETIME
from bot.database.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[BIGINT] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[BIGINT] = mapped_column(BIGINT)
    title: Mapped[VARCHAR] = mapped_column(VARCHAR)
    start_at: Mapped[DATE] = mapped_column(DATE)
    amount: Mapped[INTEGER] = mapped_column(INTEGER)
    currency: Mapped[INTEGER] = mapped_column(INTEGER)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    period: Mapped[VARCHAR] = mapped_column(VARCHAR)
    pan: Mapped[INTEGER] = mapped_column(INTEGER)
    latest_notify_at = mapped_column(DateTime, nullable=True)
