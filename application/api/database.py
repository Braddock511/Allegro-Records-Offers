from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from os import environ

user = environ.get("POSTGRES_USER")
password = environ.get("POSTGRES_PASSWORD")
host = environ.get("POSTGRES_HOST")
port = environ.get("POSTGRES_PORT")
db = environ.get("POSTGRES_DB")

if not user:
    user = "postgres"
    password = "admin"
    host = "localhost"
    port = "5432"
    db = "postgres"

# define the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

def post_credentials(allegro_id: str, allegro_secret: str, allegro_token: str) -> None:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()

    class Credentials(Base):
        __tablename__ = "credentials"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)

        api_imagekit_id = Column(String)
        api_imagekit_secret = Column(String)
        api_imagekit_endpoint = Column(String)

        api_azure_subscription_key = Column(String)
        api_azure_endpoint = Column(String)

        api_discogs_id = Column(String)
        api_discogs_secret = Column(String)
        api_discogs_token = Column(String)

        api_allegro_id = Column(String)
        api_allegro_secret = Column(String)
        api_allegro_token = Column(String)

    # create the table if it does not exist
    Base.metadata.create_all(engine)
    
    data_to_insert = {
        "api_imagekit_id": environ.get("API_IMAGEKIT_ID"),
        "api_imagekit_secret": environ.get("API_IMAGEKIT_SECRET"),
        "api_imagekit_endpoint": environ.get("API_IMAGEKIT_ENDPOINT"),
        "api_azure_subscription_key": environ.get("API_AZURE_SUBSCRIPTION_KEY"),
        "api_azure_endpoint": environ.get("API_AZURE_ENDPOINT"),
        "api_discogs_id": environ.get("API_DISCOGS_ID"),
        "api_discogs_secret": environ.get("API_DISCOGS_SECRET"),
        "api_discogs_token": environ.get("API_DISCOGS_TOKEN"),
        "api_allegro_id": allegro_id,
        "api_allegro_secret": allegro_secret,
        "api_allegro_token": allegro_token
    }       

    data_image_instance = Credentials(**data_to_insert)
    session.add(data_image_instance)
    session.commit()
    session.close()

def get_credentials() -> list:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()

    class Credentials(Base):
        __tablename__ = "credentials"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)

        api_imagekit_id = Column(String)
        api_imagekit_secret = Column(String)
        api_imagekit_endpoint = Column(String)

        api_azure_subscription_key = Column(String)
        api_azure_endpoint = Column(String)

        api_discogs_id = Column(String)
        api_discogs_secret = Column(String)
        api_discogs_token = Column(String)

        api_allegro_id = Column(String)
        api_allegro_secret = Column(String)
        api_allegro_token = Column(String)
    
    # Get credentials from database
    row = session.query(Credentials).order_by(Credentials.id.desc()).limit(1).first()
    credentials = []

    credentials.append(row.api_imagekit_id)
    credentials.append(row.api_imagekit_secret)
    credentials.append(row.api_imagekit_endpoint)

    credentials.append(row.api_azure_subscription_key)
    credentials.append(row.api_azure_endpoint)

    credentials.append(row.api_discogs_id)
    credentials.append(row.api_discogs_secret)
    credentials.append(row.api_discogs_token)

    credentials.append(row.api_allegro_id)
    credentials.append(row.api_allegro_secret)
    credentials.append(row.api_allegro_token)
    
    return credentials

def post_data_image(data: dict) -> None:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()

    class Data_Image(Base):
        __tablename__ = "data_image"
        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        data = Column(String)
        url = Column(String)

    # create the table if it does not exist
    Base.metadata.create_all(engine)

    # create a dictionary of the data to be inserted into the data_image
    for data_item in data:
        session.add(Data_Image(data=data_item['data'], url=data_item['url']))

    session.commit()
    session.close()

def get_data_image() -> dict:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()
    
    class Data_Image(Base):
        __tablename__ = "data_image"

        id = Column(Integer, primary_key=True, index=True)
        data = Column(String)
        url = Column(String)

    # get all rows from the data_image table
    data_images = session.query(Data_Image).all()

    output = {"data": [], "url": []}
    for data_image in data_images:
        output['data'].append(data_image.data)
        output['url'].append(data_image.url)

    session.execute(text('TRUNCATE data_image'))
    session.commit()
    session.close()

    return output