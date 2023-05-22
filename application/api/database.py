import json
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from os import environ
from typing import List, Dict

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

# Create database
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

class Credentials(Base):
        __tablename__ = "credentials"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)

        api_imagekit_id = Column(String)
        api_imagekit_secret = Column(String)
        api_imagekit_endpoint = Column(String)

        api_ocr_space = Column(String)

        api_discogs_token = Column(String)

        api_allegro_id = Column(String)
        api_allegro_secret = Column(String)
        api_allegro_token = Column(String)

class Image_Data(Base):
    __tablename__ = "image_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text_from_image = Column(String)
    url = Column(String)

class AllegroOffers(Base):
    __tablename__ = "allegro_offers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    offer_id = Column(String)
    offer_data = Column(String)

class AllegroPayments(Base):
    __tablename__ = "allegro_payments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    payment = Column(String)

class Flags(Base):
    __tablename__ = "flags"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    load_offers = Column(Boolean)
    load_payment = Column(Boolean)

Base.metadata.create_all(engine)

# Database scripts
Session = sessionmaker(bind=engine)
with Session() as session:
    if session.query(Flags).limit(1).count() == 0:
        session.add(Flags(load_offers=False, load_payment=False))
        session.commit() 

def post_credentials(allegro_id: str, allegro_secret: str, allegro_token: str) -> None:
    if not all([allegro_id, allegro_secret, allegro_token]):
        raise ValueError("Allegro credentials are missing")
    
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        data_to_insert = {
            "api_imagekit_id": environ.get("API_IMAGEKIT_ID"),
            "api_imagekit_secret": environ.get("API_IMAGEKIT_SECRET"),
            "api_imagekit_endpoint": environ.get("API_IMAGEKIT_ENDPOINT"),
            "api_ocr_space": environ.get("API_OCR_SPACE"),
            "api_discogs_token": environ.get("API_DISCOGS_TOKEN"),
            "api_allegro_id": allegro_id,
            "api_allegro_secret": allegro_secret,
            "api_allegro_token": allegro_token
        }      

        credentials_data = Credentials(**data_to_insert)
        session.add(credentials_data)
        session.commit()


def get_credentials() -> Dict[str, str]:
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Get credentials from database
        row = session.query(Credentials).order_by(Credentials.id.desc()).limit(1).first()
        credentials = row.__dict__
        del credentials['_sa_instance_state']

    return credentials

def post_text_from_image(text_from_images: List[Dict[str, str]]) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Delete all rows from the table
        session.query(Image_Data).delete()

        # Create a dictionary of the data to be inserted into the image_data
        for data_item in text_from_images:
            session.add(Image_Data(text_from_image=data_item['text_from_image'], url=data_item['url']))

        session.commit()

def get_text_from_image() -> List[Dict[str, Column[str]]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Get all rows from the image_data table
        rows = session.query(Image_Data).all()
        data_image = [{"text_from_image": row.text_from_image, "url": row.url} for row in rows]
        session.commit()

    return data_image

def truncate_image_data() -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        session.execute(text('TRUNCATE image_data'))
        session.commit()

def post_allegro_offers(offers: List[Dict[str, str]]) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        if session.query(AllegroOffers).limit(1).count() == 0:
            for offer in offers:
                offer_id = offer['id']
                offer_data = json.dumps(offer)
                session.add(AllegroOffers(offer_id=offer_id, offer_data=offer_data))

            flags = get_flags()

            if not flags['load_payment']:
                session.add(Flags(load_offers=True, load_payment=False))
            else:
                last_row = session.query(Flags).order_by(Flags.id.desc()).first()
                last_row.load_offers = True

            session.commit()

def get_allegro_offers() -> List[Dict[str, Column[str]]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        rows = session.query(AllegroOffers).all()
        allegro_offers = [{"offer_id": row.offer_id, "offer_data": row.offer_data} for row in rows]
        session.commit()

    return allegro_offers

def post_payments(payments: List[Dict[str, str]]) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        if session.query(AllegroPayments).limit(1).count() == 0:
            for payment in payments:
                payment = json.dumps(payment)
                session.add(AllegroPayments(payment=payment))
            
            last_row = session.query(Flags).order_by(Flags.id.desc()).first()
            last_row.load_payment = True
            session.commit()

def get_payments() -> List[Column[str]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        rows = session.query(AllegroPayments).all()
        allegro_payments = [row.payment for row in rows]
        
        session.commit()

    return allegro_payments

def post_false_flags() -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        session.add(Flags(load_offers=False, load_payment=False))
        session.commit()
        
def get_flags() -> Dict[str, Column[bool]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        row = session.query(Flags).order_by(Flags.id.desc()).limit(1).first()
        flags = {"load_offers": row.load_offers, "load_payment": row.load_payment}
        session.commit()

    return flags

def truncate_allegro_offers() -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        session.execute(text('TRUNCATE allegro_offers'))
        session.commit()

def truncate_allegro_payments() -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        session.execute(text('TRUNCATE allegro_payments'))
        session.commit()

