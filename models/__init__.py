from models.posts import posts
from models.users import users
from db import metadata, engine


metadata.create_all(bind=engine)
