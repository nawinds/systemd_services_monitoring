import sqlalchemy

from .db_session import SqlAlchemyBase


class Service(SqlAlchemyBase):
    """
    Variable object linked to 'variables' table of DB
    """
    __tablename__ = 'services'

    name = sqlalchemy.Column(sqlalchemy.String,
                             primary_key=True, index=True, unique=True)
