from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('mysql://root@localhost/test_db',
                       echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from models.user_model import UserModel


def recreate_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_create():
    recreate_db()
    params = {"extra_data": "ryan"}
    new_user = UserModel.create(params=params, session=session)
    session.commit()
    return new_user


def test_get_by_id():
    recreate_db()
    params = {"extra_data": "ryan"}
    UserModel.create(params=params, session=session)
    user = UserModel.get_by_id(id=1, session=session)
    return user


def test_update():
    recreate_db()
    params = {"extra_data": "ryan"}
    created_user = UserModel.create(params=params, session=session)
    session.commit()
    print("Created User %s" % created_user)

    update_params = {"extra_data": "jayson", "id": created_user.id}
    updated_user = UserModel.update(params=update_params, session=session)
    session.commit()
    return updated_user
