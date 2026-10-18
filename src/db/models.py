import random
from datetime import datetime

from sqlalchemy import create_engine, delete, false, select, update
from sqlalchemy.orm import Mapped, Session, declarative_base, mapped_column

Base = declarative_base()


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    created_at: Mapped[datetime]
    type: Mapped[int]
    finished: Mapped[bool] = mapped_column(default=False, server_default=false())

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id!r}, title={self.title!r}"
            f", created_at={self.created_at!r}, type={self.type!r}"
            f", finished={self.finished!r}"
        )


class DataPoint(Base):
    __tablename__ = "datapoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    real_value: Mapped[float]
    target_value: Mapped[float]

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id!r}, real_value={self.real_value!r}, target_value={self.target_value!r}"
        )


if __name__ == "__main__":
    engine = create_engine("sqlite:///experiments.db", echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all([
            Experiment(
                title="random_forest", created_at=datetime.now(), type=0, finished=True
            ),
            Experiment(title="xgboost", created_at=datetime.now(), type=1),
        ])
        session.add_all([
            DataPoint(real_value=random.random(), target_value=random.random())
            for _ in range(10)
        ])
        session.commit()

    with Session(engine) as session:
        experiments = session.scalars(select(Experiment)).all()
        data_points = session.scalars(select(DataPoint)).all()
        print(f"Experiments: {experiments}")
        print(f"Data pointse {data_points}")

    with Session(engine) as session:
        session.execute(update(Experiment).values(finished=True))
        experiments = session.scalars(select(Experiment)).all()
        print(f"Experiments: {experiments}")
        session.commit()

    with Session(engine) as session:
        session.execute(delete(Experiment))
        session.execute(delete(DataPoint))
        session.commit()
