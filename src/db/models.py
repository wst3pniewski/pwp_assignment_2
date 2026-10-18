import random
from datetime import datetime

from sqlalchemy import ForeignKey, create_engine, delete, false, func, select, update
from sqlalchemy.orm import (
    Mapped,
    Session,
    declarative_base,
    mapped_column,
    relationship,
)

Base = declarative_base()


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    created_at: Mapped[datetime]
    type: Mapped[int]
    finished: Mapped[bool] = mapped_column(default=False, server_default=false())
    data_points: Mapped[list["DataPoint"]] = relationship(back_populates="experiment")

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


if __name__ == "__main__":
    engine = create_engine("sqlite:///experiments.db", echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all([
            Experiment(
                title="random_forest",
                created_at=datetime.now(),
                type=0,
                finished=True,
                data_points=[
                    DataPoint(real_value=random.random(), target_value=random.random())
                    for _ in range(20)
                ],
            ),
            Experiment(
                title="xgboost",
                created_at=datetime.now(),
                type=1,
                data_points=[
                    DataPoint(real_value=random.random(), target_value=random.random())
                    for _ in range(10)
                ],
            ),
        ])
        # session.add_all([
        #     DataPoint(real_value=random.random(), target_value=random.random())
        #     for _ in range(10)
        # ])
        session.commit()

with Session(engine) as session:
    experiments = session.scalars(select(Experiment)).all()
    # experiments = session.scalars(select(Experiment, DataPoint).join(DataPoint))
    data_points = session.scalars(select(DataPoint)).all()
    print(f"Experiments: {experiments}")
    # print(f"Data pointse {data_points}")

with Session(engine) as session:
    stmt = (
        select(
            Experiment.id,
            func.avg(DataPoint.real_value),
            func.sum(DataPoint.real_value),
        )
        .join(Experiment.data_points)
        .group_by(Experiment.id)
    )
    res = session.execute(stmt).all()
    print(f"Avg and sum of experiment's data points: {res}")

with Session(engine) as session:
    session.execute(update(Experiment).values(finished=True))
    experiments = session.scalars(select(Experiment)).all()
    print(f"Experiments: {experiments}")
    session.commit()

with Session(engine) as session:
    session.execute(delete(Experiment))
    session.execute(delete(DataPoint))
    session.commit()
