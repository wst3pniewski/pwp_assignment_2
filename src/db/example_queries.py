import random
from datetime import datetime

from sqlalchemy import create_engine, delete, func, select, update
from sqlalchemy.orm import Session

from .models import Base, DataPoint, Experiment

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
