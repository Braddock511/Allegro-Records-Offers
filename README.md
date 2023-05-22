# Management Records Offers
The "Allegro Records Offers" application is a tool to help users effectively manage their record offers on Allegro, one of the largest Internet portals in Poland. The user can send photos of the discs from which there is a read text, and then get data from the Discogs website, and in this way users can list their vinyl records or CDs on Allegro and edit existing offers. In addition, the user can clear the background of the image and view the statistics of offers. You can also list your records on discogs

# Interface preview
![alt text](https://ik.imagekit.io/ybcdqxxka/USING/app.png?updatedAt=1684776481135)

# Configuration
  
  1. Get allegro client id and client secret (https://developer.allegro.pl/tutorials/jak-zaczac-prace-z-rest-api-4RAvV2bgwtj)
  2. Complete all environment in application/compose.yml (https://docs.imagekit.io/api-reference/api-introduction, https://ocr.space/OCRAPI, https://www.discogs.com/developers)
  3. In terminal -> cd application, docker-compose up --build
  4. The application should run on localhost:8080

# Used tools

- Docker 20.10.16
- Allegro API - communication with Allegro
- OCR Space API - model OCR
- ImageKit API - image upload 
- Discogs API  - get records data
- FastAPI - own API
- PostgreSQL - database
- Rembg - clear background image
- Vue.js - interface
