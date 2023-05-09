import os

from dotenv import load_dotenv
from sqlalchemy import String, select
from sqlalchemy.orm import Session, Mapped 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine


# Define the models
class Base(DeclarativeBase):
    pass


class Restaurant(Base):
    __tablename__ = "restaurants2"
    id: Mapped[int] = mapped_column("id", String, primary_key=True)
    name: Mapped[str] = mapped_column("name", String)


# Connect to the database
load_dotenv(".env")
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
if DBHOST != "localhost":
    DATABASE_URI += "?sslmode=require"

engine = create_engine(DATABASE_URI, echo=True)

# Create tables in database
Base.metadata.create_all(engine)

# Insert data and issue queries
with Session(engine) as session:
    # insert restaurant
    restaurant = Restaurant(
        id="8",
        name="Mak Dosa",
    )
    session.add(restaurant)
    session.commit()

    # select restaurant option 1
    restaurants = session.query(Restaurant).filter_by(name="Mak Dosa").all()
    print(restaurants)

    query = select(Restaurant).where(Restaurant.name == "Mak Dosa")
    restaurants2 = session.execute(query).scalars().all()
    print(restaurants2)
    