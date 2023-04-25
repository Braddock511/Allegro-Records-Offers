# Management Records Offers
The "Allegro Records Offers" application is a tool designed to help users effectively manage their record offers on Allegro, one of the largest online marketplaces in Poland. Thanks to this application, users can easily list their products on Allegro and edit existing offers. The application features a user-friendly interface that allows you to quickly and easily upload your products to the Allegro platform. Users can add product photos, descriptions, prices, and other important details to create engaging and informative listings that will appeal to potential buyers. In addition, the user can clear the background of the image and view the statistics of the offers. You can also list your records on discogs

# Configuration
  
  1. Get allegro client id and client secret (https://developer.allegro.pl/tutorials/jak-zaczac-prace-z-rest-api-4RAvV2bgwtj)
  2. Complete all environment in application/compose.yml (https://docs.imagekit.io/api-reference/api-introduction, https://azure.microsoft.com/pl-pl/products/app-service/api/, https://www.discogs.com/developers)
  3. In terminal -> cd application, docker-compose up --build
  4. The application should run on localhost:8080

# Used tools

- Docker 20.10.16
- Allegro API - communication with Allegro
- Azure API - model OCR and clear background image
- ImageKit API - image upload 
- Discogs API  - get records data
- FastAPI - own API
- PostgreSQL - database
- Vue.js - interface