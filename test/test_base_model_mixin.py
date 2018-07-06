from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Column, String)
from models.base_model_mixin import BaseModelMixin
import unittest

Base = declarative_base()
engine = create_engine('mysql://root@localhost/test_db',
                       echo=True)


class TestModel(BaseModelMixin, Base):
    __tablename__ = 'test_model'
    test_field = Column(String(36), nullable=True, default='')


class TestBaseModelMixin(unittest.TestCase):

    def setUp(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def tearDown(self):
        self.session.close_all()
        Base.metadata.drop_all(engine)

    def test_is_test_table_created(self):
        self.assertEqual(TestModel.__tablename__, "test_model")

    def test_is_default_column_created(self):
        default_columns = ["test_model_id", "test_model_pid", "created_by",
                           "created_at", "updated_by", "updated_at",
                           "deleted_by", "deleted_at", "deleted"]
        for default_column in default_columns:
            with self.subTest(default_column=default_column):
                self.assertIn(default_column, TestModel.__table__.columns)

    def test_test_table_field_created(self):
        self.assertIn("test_field", TestModel.__table__.columns)

    def test_is_test_model_has_base_model_mixin_default_methods(self):
        default_methods = ["get_by_id", "get_by_pid", "create", "update"]

        for default_method in default_methods:
            with self.subTest(default_method=default_method):
                self.assertTrue(callable(getattr(TestModel, default_method)))

    def test_create(self):
        params = {"test_field": "test_data"}
        record = TestModel.create(params=params, session=self.session)
        self.session.commit()

        self.assertEqual(1, record.internal_id)
        self.assertIsNot(None, record.public_id)
        self.assertEqual("test_data", record.test_field)
        self.assertIsNot(None, record.created_at)
        self.assertEqual(False, record.deleted)
