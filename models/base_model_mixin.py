from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Integer, Column, String, Boolean, TIMESTAMP, text
import uuid
import logging


class BaseModelMixin(object):
    """Base Model Mixin for reusable columns and methods.

    Default columns:
    - <tablename>_id (Integer)
    - <tablename>_pid (String(36))
    - created_by (String(36)
    - created_at (Timestamp)
    - created_by (String(36)
    - updated_at (Timestamp)
    - updated_by (String(36))
    - deleted_at (Timestamp)
    - deleted_by (String(36)
    - deleted (Boolean)

    Default methods:
    - get_by_id()
    - get_by_pid()
    - create()
    - update()

    example usage:

        from base_model_mixin import BaseModelMixin

        class MyModel(BaseModelMixin, Base):
            username = Column(String(36))
            firstname = Column(String(36))
            lastname = Column(String(36))

        or

        from sqlalchemy.ext.declarative import declarative_base
        from base_model_mixin import BaseModelMixin
        Base = declarative_base(cls=BaseModelMixin)

        class MyModel(Base):
            username = Column(String(36))
            firstname = Column(String(36))
            lastname = Column(String(36))


    """
    __table_args_ = {"mysql_charset": "utf8", "mysql_engine": "InnoDB"}

    created_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String(36), nullable=True, default='')
    updated_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("CURRENT_TIMESTAMP ON \
                                             UPDATE CURRENT_TIMESTAMP"))
    updated_by = Column(String(36), nullable=True, default='')
    deleted = Column(Boolean, default=False)
    deleted_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("NULL"))
    deleted_by = Column(String(36), nullable=True, default='')
    deleted = Column(Boolean, default=False)

    @declared_attr
    def internal_id(cls):
        """Generate internal id.

        Generate internal id for a specific table.
        internal id is prepended by "tablename_"

        example:

            user_id

        """
        internal_id = "{tablename}_id".format(tablename=cls.__tablename__)
        return Column(internal_id, Integer, primary_key=True)

    @declared_attr
    def public_id(cls):
        """Generate public id.

        Generate public id for a specific table.
        public id is prepended by "tablename_"

        example:

            user_pid

        """
        public_id = "{tablename}_pid".format(tablename=cls.__tablename__)
        return Column(public_id, String(36), default=uuid.uuid4().hex)

    @classmethod
    def get_by_id(cls, id, session):
        """Get active record using internal id.

        Parameters:
            - id(int)
            - session(object)

        Return:
            Object Instance

        Example usage:

            record =  MyModel.get_by_id(id=1, session=session)
            print(record)  # <models.my_model.MyModel object at 0x7f321bece358>

        Genearated Query:

            # TODO
            - include genearated query.

        """
        try:
            record = (session.query(cls)
                             .filter_by(column_id=id)
                             .filter(cls.deleted != 1)
                             .scalar())
            return record
        except Exception as e:
            logging.exception("Expected error: %s" % e, exc_info=True)
            return None

    @classmethod
    def get_by_pid(cls, pid, session):
        """Get active record using public id.

        Parameters:
            - id(string)
            - session(object)

        Return:
            Object Instance

        Example usage:

            record =  MyModel.get_by_id(pid="b90060a09fb211e7abc4cec278b6b50a",
                                        session=session)
            print(record)  # <models.my_model.MyModel object at 0x7f321bece358>

        Genearated Query:

            # TODO
            - include genearated query.

        """
        try:
            record = (session.query(cls)
                             .filter_by(column_pid=pid)
                             .filter(cls.deleted != 1)
                             .first())
            return record
        except Exception as e:
            logging.exception("Expected error: %s" % e, exc_info=True)
            return None

    @classmethod
    def create(cls, params, session):
        """Create new record.

        Parameters:
            - params(dict)
            - session(object)

        Return:
            Object Instance

        Example usage:

            create_params = {"column": "sample value"}
            record =  MyModel.create(params=create_params, session=session)
            print(record)  # <models.my_model.MyModel object at 0x7f321bece358>

        Genearated Query:

            # TODO
            - include genearated query.

        """
        try:
            cls = cls()
            for key, value in params.items():
                if hasattr(cls, key):
                    setattr(cls, key, value)

            session.add(cls)
            session.flush()

            return cls
        except Exception as e:
            logging.exception("Expected error: %s" % e, exc_info=True)
            return None

    @classmethod
    def update(cls, params, session):
        """Update record with new values.

        Parameters:
            - params(dict)
            - session(object)

        Return:
            Object Instance

        Example usage:

            create_params = {"tablename_id": 1, "column": "sample value"}
            record =  MyModel.create(params=create_params, session=session)
            print(record)  # <models.my_model.MyModel object at 0x7f321bece358>

        Genearated Query:

            # TODO
            - include genearated query.

        """
        try:
            editable_columns = params.get("editable_columns", [])

            column_id = "{tablename}_id".format(tablename=cls.__tablename__)
            if column_id not in params.keys():
                return None

            record = (session.query(cls)
                             .filter_by(column_id=params.get(id))
                             .filter(cls.deleted != 1)
                             .scalar())

            if not record:
                return None

            for key, value in params.items():
                if hasattr(cls, key) and key in editable_columns:
                    setattr(record, key, value)

            session.add(record)
            session.flush()

            return record
        except Exception as e:
            logging.exception("Expected error: %s" % e, exc_info=True)
            return None
