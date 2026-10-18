from datetime import datetime

from sqlalchemy import Column, ForeignKey, Table, false
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

Base = declarative_base()

subjects_experiments = Table(
    "subjects_experiments",
    Base.metadata,
    Column(
        "subject_id", ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "experiment_id",
        ForeignKey("experiments.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    created_at: Mapped[datetime]
    type: Mapped[int]
    finished: Mapped[bool] = mapped_column(default=False, server_default=false())
    data_points: Mapped[list["DataPoint"]] = relationship(back_populates="experiment")

    subjects = relationship(
        "Subject", secondary=subjects_experiments, back_populates="experiments"
    )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id!r}, title={self.title!r}"
            f", created_at={self.created_at!r}, type={self.type!r}"
            f", finished={self.finished!r}"
            f", n_datapoints={len(self.data_points)}"
        )


class DataPoint(Base):
    __tablename__ = "datapoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    real_value: Mapped[float]
    target_value: Mapped[float]
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))
    experiment: Mapped["Experiment"] = relationship(back_populates="data_points")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id!r}, real_value={self.real_value!r}"
            f", target_value={self.target_value!r}"
        )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(default=False, server_default=false())
    experiments = relationship(
        "Experiment", secondary=subjects_experiments, back_populates="subjects"
    )
