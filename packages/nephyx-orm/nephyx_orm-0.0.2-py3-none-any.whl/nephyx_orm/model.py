
import re
import datetime
import uuid
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


# TODO https://alembic.sqlalchemy.org/en/latest/naming.html

#convention = {
#    "ix": "ix_%(column_0_label)s",
#    "uq": "uq_%(table_name)s_%(column_0_name)s",
#    "ck": "ck_%(table_name)s_%(constraint_name)s",
#    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#    "pk": "pk_%(table_name)s",
#}

#metadata = MetaData(naming_convention=convention)

#Base = declarative_base(metadata=metadata)

class ModelBase(DeclarativeBase):

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        names = re.split("(?=[A-Z])", self.__name__)
        return "_".join([x.lower() for x in names if x])


class UuidMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class AuditMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.current_timestamp())

