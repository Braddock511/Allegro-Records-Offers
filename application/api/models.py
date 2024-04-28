from pydantic import BaseModel

class ImagesRequest(BaseModel):
    userKey: str
    images: list
    listing: dict

class ImageRequest(BaseModel):
    userKey: str
    image: str

class DiscogsInfoRequest(BaseModel):
    userKey: str
    index: int
    allegroData: dict
    
class DiscogsInfoImageRequest(BaseModel):
    userKey: str
    index: int
    numberImages: int
    typeRecord: str
    image_data: list

class NewSearchRequest(BaseModel):
    userKey: str
    newSearch: str
    typeRecord: str
    allegroData: dict

class UserKeyRequest(BaseModel):
    userKey: str

class AllegroAuthRequest(BaseModel):
    client_id: str
    client_secret: str

class AllegroTokenRequest(BaseModel):
    userKey: str
    discogs_token: str
    client_id: str
    client_secret: str
    device_code: str

class AllergoEditDescRequest(BaseModel):
    userKey: str
    offerId: str
    images: list
    newEditData: dict
    listingSimilar: bool
    editPrice: bool
    editDescription: bool
    toBuy: bool

class AllergoEditImageRequest(BaseModel):
    userKey: str
    offerId: str
    images: list
    
class AllegroListingRequest(BaseModel):
    userKey: str
    offer_data: dict
    carton: str
    typeRecord: str
    typeOffer: str
    duration: str
    clear: bool
    
class AllegroOffersRequest(BaseModel):
    userKey: str
    limit: str
    offset: str
    typeOffer: str
    typeRecord: str
    genre: str

class AllegroOffersRequest(BaseModel):
    userKey: str
    offerId: str

class DiscogsListingRequest(BaseModel):
    userKey: str
    listing_id: str
    mediaCondition: str
    sleeveCondition: str
    carton: str
    price: str
    images: list
    
class SwapAllRequest(BaseModel):
    userKey: str
    swapCarton: str
    withCarton: str

class SwapSpecificRequest(BaseModel):
    userKey: str
    swapCarton: str
    withCarton: str
    offerId: str

class Listing(BaseModel):
    listing: str
