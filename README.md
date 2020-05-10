## python url shorter using flask (microservice pattern)  ##
### docker file is included in the root directory ###
### technology stack ###
    flask
    tinydb (databse> db/database.json)
    marshmello
    webargs
####  create virtual env from the `requirements.txt ` activate the virtualenv and run `python main.py` from the root of the project directory 
 
 post method example :
        curl --location --request POST 'http://127.0.0.1:5000/shortener/api' \
--header 'Content-Type: application/json' \
--header 'Content-Type: text/plain' \
--data-raw '{
	"url":"https://www.pcworld.com/article/191812/Long_URL_Please.html",
	"title":"longUrl"
	
}'

get method :
        
        curl --location --request GET 'http://127.0.0.1:5000/shortener/api?title=long'
   result:
 `[
    {
        "short_url": "http://127.0.0.1:5000/shortener/api/f5ab248f",
        "hourly_hits_ratio": "192.857",
        "url": "https://www.pcworld.com/article/191812/Long_URL_Please.html",
        "id": "f5ab248f",
        "created_at": "2020-05-10 13:16:11.015140",
        "title": "longUrl",
        "hits": 3,
        "hit_times": [
            "2020-05-10 13:16:46.417509",
            "2020-05-10 13:17:13.196109",
            "2020-05-10 13:17:42.861120"
        ]
  `   
                
api should return all pages which have partial or full match 

and when short url like `http://127.0.0.1:5000/shortener/api/84cfe3d4`
hited then it will redirect to the full url and generate report for it 


`
"hourly_hits_ratio": "10.335",  
"hit_times": [
            "2020-05-10 01:50:39.258688",
            "2020-05-10 02:07:54.929824",
            "2020-05-10 02:08:04.799635"
        ],
        "hits": 3,`
        


 
 #### docker run step ####

Build>> `docker build -t flask-url-shortner:latest .`
 
 run>> `docker run -d -p 5000:5000 flask-url-shortner `