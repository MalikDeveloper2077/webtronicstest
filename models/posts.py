import sqlalchemy
from sqlalchemy.orm import relationship

from db import metadata


LIKE_VALUE = 1
DISLIKE_VALUE = 2

posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("text", sqlalchemy.Text),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey(
        "users.id", ondelete='CASCADE'
    ))
)


estimations = sqlalchemy.Table(
    "estimations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("value", sqlalchemy.Integer, default=0),  # LIKE_VALUE, DISLIKE_VALUE
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey(
        "users.id", ondelete='CASCADE'
    )),
    sqlalchemy.Column("post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey(
        "posts.id", ondelete='CASCADE'
    ))
)
