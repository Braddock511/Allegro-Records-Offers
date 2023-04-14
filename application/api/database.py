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

# Define the database URL
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

    # Create the table if it does not exist
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

    credentials_data = Credentials(**data_to_insert)
    session.add(credentials_data)
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
    
    credentials = {
        "api_imagekit_id": row.api_imagekit_id,
        "api_imagekit_secret": row.api_imagekit_secret,
        "api_imagekit_endpoint": row.api_imagekit_endpoint,
        "api_azure_subscription_key": row.api_azure_subscription_key,
        "api_azure_endpoint": row.api_azure_endpoint,
        "api_discogs_id": row.api_discogs_id,
        "api_discogs_secret": row.api_discogs_secret,
        "api_discogs_token": row.api_discogs_token,
        "api_allegro_id": row.api_allegro_id,
        "api_allegro_secret": row.api_allegro_secret,
        "api_allegro_token": row.api_allegro_token
    }  

    return credentials

def post_text_from_image(text_from_images: list) -> None:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()
    
    Session = sessionmaker(bind=engine)
    session = Session()

    class Image_Data(Base):
        __tablename__ = "image_data"
        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        text_from_image = Column(String)
        url = Column(String)

    # Create the table if it does not exist
    Base.metadata.create_all(engine)

    # Create a dictionary of the data to be inserted into the image_data
    for data_item in text_from_images:
        session.add(Image_Data(text_from_image=data_item['text_from_image'], url=data_item['url']))

    session.commit()
    session.close()

def get_text_from_image() -> dict:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()
    
    class Image_Data(Base):
        __tablename__ = "image_data"
        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        text_from_image = Column(String)
        url = Column(String)

    # Get all rows from the image_data table
    rows = session.query(Image_Data).all()

    data_image = {"text_from_image": [], "url": []}
    
    for row in rows:
        data_image['text_from_image'].append(row.text_from_image)
        data_image['url'].append(row.url)

    session.execute(text('TRUNCATE image_data'))
    session.commit()
    session.close()

    return data_image
