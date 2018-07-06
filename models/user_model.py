from app import Base
from sqlalchemy import (Column, String)
from models.base_model_mixin import BaseModelMixin


class UserModel(BaseModelMixin, Base):
    __tablename__ = 'user_table'
    user_name = Column(String(36), nullable=True, default='')

    def __repr__(self):
        return "<UserModel(user_id='%s', user_name=%s)>" % (self.user_id,
                                                            self.user_name)

    @classmethod
    def update(cls, params, session):
        params["editable_columns"] = ["extra_data"]

        return super(UserModel, cls).update(params, session)
