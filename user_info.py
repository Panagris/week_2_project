import sqlalchemy as sql

# Code here ...
engine = sql.create_engine('sqlite:///tutor.db')

# This file handles the database, having functions that write and read to the database
# that can be called by other files in the directory.
'''
metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("user_name", String(100), primary_key=True),
    Column(
        "bio",
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb"),
    ),
) '''


metadata_obj = sql.MetaData()

user = sql.Table(
    "user",
    metadata_obj,
    sql.Column("id", int(100), primary_key=True),
    sql.Column("user_name", String(100), primary_key=True),
    sql.Column(
        "bio",
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb"),
    ),
)


def print_subject_list():
    subjects [
        {'id': 1, 'name': 'Math'},
        {'id': 2, 'name': 'History'},
        {'id': 3, 'name': 'Science'},
    ]
class User(Base):
     __tablename__ = "users"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(30))
     previous_subjects: = Mapped[List[str]]
     progress = Mapped[List[str]]
     

     addresses: Mapped[List["Address"]] = relationship(
         back_populates="user", cascade="all, delete-orphan"
     )

     def __repr__(self) -> str:
         return f"User(id={self.id!r}, name={self.name!r}, previous_subjects={self.previous_subjects!r}, progress = {self.})"