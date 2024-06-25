import sqlalchemy as sql
from sqlalchemy.types import TEXT

# Code here ...
engine = sql.create_engine('sqlite:///artist_info.db')
