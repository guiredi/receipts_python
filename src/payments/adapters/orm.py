from datetime import datetime

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date, text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper

from payments.domain import model

metadata = MetaData()

transactions = Table(
    "transactions",
    metadata,
    Column('uuid',
           UUID(as_uuid=True),
           server_default=text('uuid_generate_v4()'),
           unique=True, nullable=False, primary_key=True),
    Column("payment_method", String(255)),
    Column("gateway", String(255)),
    Column("value", Integer, nullable=False),
    Column("created_at", Date, default=datetime.utcnow),
    Column("updated_at", Date, nullable=True),
)

mapper(model.Transaction, transactions)
