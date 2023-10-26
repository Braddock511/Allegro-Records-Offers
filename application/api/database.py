import json
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import declarative_base, sessionmaker
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
KEYS = {"test": ""}

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

class Credentials(Base):
        __tablename__ = "credentials"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)

        user_folder = Column(String, unique=True)
        
        api_imagekit_id = Column(String)
        api_imagekit_secret = Column(String)
        api_imagekit_endpoint = Column(String)

        api_ocr_space = Column(String)

        api_discogs_token = Column(String)

        api_allegro_id = Column(String)
        api_allegro_secret = Column(String)
        api_allegro_token = Column(String)

class ImageData(Base):
    __tablename__ = "image_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    credentials_folder = Column(String, ForeignKey("credentials.user_folder"))
    text_from_image = Column(String)
    url = Column(String)

class AllegroOffers(Base):
    __tablename__ = "allegro_offers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    credentials_folder = Column(String, ForeignKey("credentials.user_folder"))    
    offer_id = Column(String)
    offer_data = Column(String)

class AllegroPayments(Base):
    __tablename__ = "allegro_payments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    credentials_folder = Column(String, ForeignKey("credentials.user_folder"))    
    payment = Column(String)

class Flags(Base):
    __tablename__ = "flags"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    credentials_folder = Column(String, ForeignKey("credentials.user_folder"))
    load_offers = Column(Boolean)
    load_payment = Column(Boolean)

Base.metadata.create_all(engine)

# Database scripts
Session = sessionmaker(bind=engine)

def post_credentials(user_key: str, discogs_token: str, allegro_id: str, allegro_secret: str, allegro_token: str) -> bool:
    if user_key in KEYS.keys():
        Session = sessionmaker(bind=engine)
        
        user_folder = KEYS[user_key]

        with Session() as session:
            try:
                # Check if there is a record for the given user_key
                credentials_data = session.query(Credentials).filter_by(user_folder=user_folder).one()
                
                # Update record
                credentials_data.api_discogs_token = discogs_token
                credentials_data.api_allegro_id = allegro_id
                credentials_data.api_allegro_secret = allegro_secret
                credentials_data.api_allegro_token = allegro_token

                session.commit()
                return True

            except NoResultFound:
                
                data_to_insert = {
                    "user_folder": user_folder,
                    "api_imagekit_id": environ.get("API_IMAGEKIT_ID"),
                    "api_imagekit_secret": environ.get("API_IMAGEKIT_SECRET"),
                    "api_imagekit_endpoint": environ.get("API_IMAGEKIT_ENDPOINT"),
                    "api_ocr_space": environ.get("API_OCR_SPACE"),
                    "api_allegro_id": allegro_id,
                    "api_allegro_secret": allegro_secret,
                    "api_allegro_token": allegro_token
                }

                credentials_data = Credentials(**data_to_insert)
                session.add(credentials_data)
                session.commit()
                post_false_flags(user_key)
                
                return True
    
    return False

def get_credentials(user_key: str) -> Dict[str, str]:
    Session = sessionmaker(bind=engine)
    with Session() as session:
        row = session.query(Credentials).filter_by(user_folder=KEYS[user_key]).one()
        credentials = row.__dict__
        credentials['user_key'] = user_key
    
    return credentials

def post_text_from_image(user_key: str, text_from_images: List[Dict[str, str]]) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        for text_from_image in text_from_images:
            for data_item in text_from_image:
                session.add(ImageData(credentials_folder=KEYS[user_key], text_from_image=data_item['text_from_image'], url=data_item['url']))
            
        session.commit()

def get_text_from_image(user_key: str) -> List[Dict[str, Column[str]]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Get all rows from the image_data table
        rows = session.query(ImageData).filter_by(credentials_folder=KEYS[user_key]).all()
        data_image = [{"text_from_image": row.text_from_image, "url": row.url} for row in rows]
        session.commit()

    return data_image

def delete_image_data(user_key: str) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        session.query(ImageData).filter(ImageData.credentials_folder == KEYS[user_key]).delete()
        session.commit()

def post_allegro_offers(user_key: str, offers: List[Dict[str, str]]) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        for offer in offers:
            offer_id = offer['id']
            offer_data = json.dumps(offer)
            session.add(AllegroOffers(credentials_folder=KEYS[user_key], offer_id=offer_id, offer_data=offer_data))


        row_flags = session.query(Flags).filter_by(credentials_folder=KEYS[user_key]).order_by(Flags.id.desc()).first()
        row_flags.load_offers = True

        session.commit()

def get_allegro_offers(user_key: str) -> List[Dict[str, Column[str]]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        rows = session.query(AllegroOffers).filter_by(credentials_folder=KEYS[user_key]).all()
        allegro_offers = [{"offer_id": row.offer_id, "offer_data": row.offer_data} for row in rows]
        session.commit()

    return allegro_offers

def post_payments(user_key: str, payments: List[Dict[str, str]]) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        for payment in payments:
            payment = json.dumps(payment)
            session.add(AllegroPayments(credentials_folder=KEYS[user_key], payment=payment))

        row_flags = session.query(Flags).filter_by(credentials_folder=KEYS[user_key]).order_by(Flags.id.desc()).first()
        row_flags.load_payment = True

        session.commit()

def get_payments(user_key: str) -> List[Column[str]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        rows = session.query(AllegroPayments).filter_by(credentials_folder=KEYS[user_key]).all()
        allegro_payments = [row.payment for row in rows]
        
        session.commit()

    return allegro_payments

def post_false_flags(user_key: str) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            flags = session.query(Flags).filter_by(credentials_folder=KEYS[user_key]).one()
            
            flags.load_offers = False
            flags.load_payment = False

            session.commit()

        except NoResultFound:
            session.add(Flags(credentials_folder=KEYS[user_key], load_offers=False, load_payment=False))
            session.commit()
        
def get_flags(user_key: str) -> Dict[str, Column[bool]]:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        row = session.query(Flags).filter_by(credentials_folder=KEYS[user_key]).one()
        flags = {"load_offers": row.load_offers, "load_payment": row.load_payment}
        session.commit()

    return flags

def delete_allegro_offers(user_key: str) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        session.query(AllegroOffers).filter(AllegroOffers.credentials_folder == KEYS[user_key]).delete()
        session.commit()

def delete_allegro_payments(user_key: str) -> None:
    Session = sessionmaker(bind=engine)

    with Session() as session:
        session.query(AllegroPayments).filter(AllegroPayments.credentials_folder == KEYS[user_key]).delete()
        session.commit()

