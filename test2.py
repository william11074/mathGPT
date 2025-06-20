from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey


engine = create_engine("postgresql://postgres:supabasetesting@db.uexllsxcfbknokvcdrvr.supabase.co:5432/postgres", echo = True)
metadata_obj = MetaData()
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)
metadata_obj.create_all(engine)