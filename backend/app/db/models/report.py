from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base_model import BaseModel


class Report(BaseModel):
    """
    Electricity service report.
    """

    __tablename__ = "reports"

    community: Mapped[str] = mapped_column(String(100))

    outage: Mapped[bool] = mapped_column(Boolean)