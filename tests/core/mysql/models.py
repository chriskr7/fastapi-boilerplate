from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from core.db.mysql.session import Base


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(40))
