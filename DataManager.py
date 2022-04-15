import json
import pymongo
import urllib3
from pymongo import MongoClient

class RestApiManager:
    def __init__(self):
        self.http = urllib3.PoolManager()
    
    def fetch(self, url, method, fields = None, headers = None):
        print("Request details : url={}  method={}  fields={}  headers={}".format(url, method, fields, headers))
        response = self.call_api(url, method, fields, headers)
        return response
    
    def call_api(self, url, method, query, header):
        print("Downloading")
        i = 0
        while i < 3:
            print("Inside while loop")
            response = self.http.request(method, url, fields = query, headers = header)
            print("Response Status = {}".format(response.status))
            if response.status == 200 :
                return response.data
            else:
                i+=1
                print("Failed {} times".format(i))
        if i == 3:
            return None
                
        
class MongoDBClient:
    
    def __init__(self, db_name):
        self.mongoclient = MongoClient('mongodb://localhost:27017/')
        self.db = self.mongoclient[db_name]
        self.collection_dict = {}
        
    def create_collection(self, name):
        collection = self.db[name]
        self.collection_dict = {name : collection}
        
    def get_collection(self, name):
        if isinstance(self.collection_dict.get(name), type(None)):
            self.create_collection(name)
        return self.collection_dict.get(name)
        
    def insert_one(self, json_data, coll_name):
        self.get_collection(coll_name).insert_one(json_data)
        
class RestClient:
    
    IMDB = "Imdb"
    TMDB = "Tmdb"
    
    def __init__(self, df):
        self.manager = RestApiManager()
        self.nosqlclient = MongoDBClient("Movies")
        self.collection = ""
        self.movies_df = df
        
    def insertIntoMongo(self, data, name):
        self.nosqlclient.insert_one(json_data = data, coll_name = name)
        
    def receive_response(self, response):
        self.response = response
        self.insertIntoMongo(data = response, name = self.collection)

    def load_State(self):
        return DownloadProgressState()
        
    def fetch_data(self):
        count = 0
        headers = {
                        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com",
                        "X-RapidAPI-Key": "20dccd3f53msh93dd7799c09edf4p170a44jsn6e58dc3354e4"
                    }
        for index, movie in self.movies_df.iterrows():
            if count == 1:
                return
            imdbid = movie['imdbId']
            tmdbid = movie['tmdbId']
            movieid = movie['movieId']
            
            print("Imdb Id = {}  Tmdb Id = {}".format(imdbid, tmdbid))
            self.collection = self.IMDB
            querystring = {"r":"json","i":"tt{}".format(str(imdbid).zfill(7))}

            imdburl = "https://movie-database-alternative.p.rapidapi.com/"
            tmdburl = "https://api.themoviedb.org/3/movie/{}?api_key=34716158ed3bedaedfa4dd37ea314e12".format(tmdbid)
            imdbresponse = self.manager.fetch(imdburl, "GET", fields = querystring, headers = headers)
            imdbdict = json.loads(imdbresponse)
            imdbdict['_id'] = movieid
            self.receive_response(imdbdict)
            self.collection = self.TMDB
            tmdbresponse = self.manager.fetch(tmdburl, "GET")
            tmdbdict = json.loads(tmdbresponse)
            tmdbdict['_id'] = movieid
            self.receive_response(tmdbdict)
            count += 1
