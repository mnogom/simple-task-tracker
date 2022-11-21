from datetime import datetime

from faker import Faker
import random

from app import models, schemas
from app.db.session import SessionLocal


def create_user(fake: Faker):
    full_name = fake.name()
    email = fake.unique.email()
    hashed_password = fake.password()
    db_user = models.User(email=email,
                          hashed_password=hashed_password,
                          full_name=full_name)

    return db_user


def create_task(owner_id: int, fake: Faker):
    name = fake.bs()
    status = random.choice((
        'not_started',
        'in_progress',
        'finished',
        'canceled',
    ))
    deadline = fake.date_between(start_date=datetime.today(), end_date=datetime(2023, 12, 31))
    description = fake.paragraph(nb_sentences=5)

    db_task = models.Task(name=name,
                          status=status,
                          deadline=deadline,
                          description=description,
                          owner_id=owner_id)

    return db_task


def fill_with_fake_data(user_count=1000, tasks_per_user=1000):
    fake = Faker()
    db_users = []
    db_tasks = []

    with SessionLocal() as db:

        if db.query(models.User).count() > 0:
            return

        for _i in range(user_count):
            print(_i)
            db_user = create_user(fake=fake)
            db_users.append(db_user)
            for _j in range(tasks_per_user):
                db_task = create_task(owner_id=random.randint(1, user_count + 1), fake=fake)
                db_tasks.append(db_task)

        db.add_all(db_users)
        db.add_all(db_tasks)
        db.commit()


if __name__ == '__main__':
    fill_with_fake_data()

    user_id = 75

    with SessionLocal() as db:
        start = datetime.now()
        print(' ------ start just query ------')
        print(' --- 1 --- ')
        user = db.query(models.User).get(user_id)
        print(' --- 2 --- ')
        out_1 = schemas.User.from_orm(user)
        print(' ------ end just query ------')
        stop = datetime.now()

    print('>' * 5, stop - start)

    with SessionLocal() as db:
        start = datetime.now()
        print(' ------ start join query ------')
        print(' --- 1 --- ')
        user = db.query(models.User).filter(models.User.id == user_id).join(models.Task).first()
        print(' --- 2 --- ')
        out_2 = schemas.User.from_orm(user)
        print(' ------ end join query ------')
        stop = datetime.now()

    print('>' * 5, stop - start)

    assert out_1 == out_2
