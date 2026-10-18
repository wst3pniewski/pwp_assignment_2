from datetime import datetime

from sqlalchemy import create_engine, false
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    created_at: Mapped[datetime]
    type: Mapped[int]
    finished: Mapped[bool] = mapped_column(default=False, server_default=false())


class DataPoint(Base):
    __tablename__ = "datapoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    real_value: Mapped[float]
    target_value: Mapped[float]


if __name__ == "__main__":
    engine = create_engine("sqlite:///experiments.db", echo=True)
    Base.metadata.create_all(engine)
