import json
import pymongo
import urllib3
import time
from datetime import date
from pymongo import MongoClient

class RestApiManager:
    def __init__(self):
        self.http = urllib3.PoolManager()
    
    def fetch(self, url, method, fields = None, headers = None):
        print("Request details : url={}  method={}  fields={}  headers={}".format(url, method, fields, headers))
        response = self.call_api(url, method, fields, headers)
        return response
    
    def call_api(self, url, method, query, header): 
        #print("Downloading")
        i = 0
        while i < 3:
            #print("Inside while loop")
            response = self.http.request(method, url, fields = query, headers = header)
            print("Response Status = {}".format(response.status))
            #print("Response Data = {}".format(response.data))
            #print(response.data)
            if response.status == 200 :
                break
            else:
                i+=1
                print("Failed {} times".format(i))
        return response
    
class DownloadProgressState:
    def __init__(self, date = "NA",api_calls_today = 0, current_batch = 0, record_no = 0, overall_status = "In Progress"):
        self.batch = current_batch
        self.record = record_no
        self.status = overall_status
        self.api_calls_today = api_calls_today
        self.date = date
        
    def reset_date(self):
        self.date = date.today().strftime('%d/%m/%Y') if self.api_calls_today == 0 else self.date
    
    def reset_api_call_count(self):
        self.api_calls_today = 0
        
    def get_state_dict(self):
        state = {
                    "_id" : "state001",
                    "batch_in_progress" : self.batch,
                    "last_downloaded_record_in_the_batch" : self.record,
                    "overall_status" : self.status,
                    "api_calls_today" : self.api_calls_today,
                    "last_api_call_date" : self.date
                }
        #print(state)
        return state
    
    def initialize_state(self, state):
        self.batch = state['batch_in_progress']
        self.record = state['last_downloaded_record_in_the_batch']
        self.status = state['overall_status']
        self.api_calls_today = state['api_calls_today']
        self.date = state['last_api_call_date']
        

class DataStateMachine:
    
    def __init__(self, mongodbclient):
        self.mongo = mongodbclient
   
    def update_state(self, state_obj):
        self.mongo.upsert_one({"_id" : "state001"}, state_obj.get_state_dict(), "State")
        
    
    def get_current_state(self) :
        if self.mongo.count_documents("State") == 0:
            state_obj = DownloadProgressState()
            self.update_state(state_obj)
        current_state = self.mongo.find_one("State", query = {"_id" : "state001"})
        #print(current_state)
        current_state_obj = DownloadProgressState()
        current_state_obj.initialize_state(current_state)
        return current_state_obj

class MongoDBClient:
    
    def __init__(self, db_name):
        self.mongoclient = MongoClient('mongodb://localhost:27017/')
        self.db = self.mongoclient[db_name]
        self.collection_dict = {}
        
    def create_collection(self, name):
        collection = self.db[name]
        self.collection_dict = {name : collection}
        
    def count_documents(self, name, query = {}):
        return self.get_collection(name).count_documents(query)
        
    def find_one(self, name, query = {}):
        return self.get_collection(name).find_one(query)
            
    def get_collection(self, name):
        if isinstance(self.collection_dict.get(name), type(None)):
            self.create_collection(name)
        return self.collection_dict.get(name)
        
    def insert_one(self, json_data, coll_name):
        try:
            self.get_collection(coll_name).insert_one(json_data)
        except DuplicateKeyError:
            print("Duplicate Key")
            
    def upsert_one(self, match, json_data, coll_name):
        try:
            self.get_collection(coll_name).replace_one(match, json_data, upsert = True)
        except:
            print("Error")
            
    def update(self, match, json_data, coll_name):
        try:
            self.get_collection(coll_name).update_one(match, json_data)
        except:
            print("Error")

class RestClient:
    
    IMDB = "Imdb"
    TMDB = "Tmdb"
    BATCH_SIZE = 20
    DAILY_API_CALL_LIMIT = 800
    
    def __init__(self, movies_df):
        self.manager = RestApiManager()
        self.nosqlclient = MongoDBClient("Movies")
        self.df = movies_df
        self.state_machine = DataStateMachine(self.nosqlclient)
        
    def insertIntoMongo(self, data, name):
        self.nosqlclient.insert_one(json_data = data, coll_name = name)
        
    def receive_response(self, response, collection):
        self.response = response
        self.insertIntoMongo(data = response, name = collection)
    
    def update_state(self, state_obj):
        self.state_machine.update_state(state_obj)
        
    def fetch_data(self):
        #Loading last saved state from mongodb
        state = self.state_machine.get_current_state()
        overall_status = state.status
        if overall_status == "Complete":
            return
        last_call_date = state.date
        if last_call_date == "NA" or date.today().strftime('%d/%m/%Y') != last_call_date:
            state.reset_api_call_count()
            state.reset_date()
        api_calls_count = state.api_calls_today

        #Checking if the daily api call limit has already reached before calling the apis
        if api_calls_count >= RestClient.DAILY_API_CALL_LIMIT:
            return

        #Initializing local state variables from the fetched state
        batch_size = RestClient.BATCH_SIZE
        count = state.record
        batch = state.batch

        #Calculating the start index to continue where the program left off last time
        start = (batch * batch_size ) + count

        rapid_api_headers = {
                        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com",
                        "X-RapidAPI-Key": "20dccd3f53msh93dd7799c09edf4p170a44jsn6e58dc3354e4"
                    }
        for index, movie in self.df.iloc[start:].iterrows():

            imdbid = movie['imdbId']
            tmdbid = movie['tmdbId']
            movieid = movie['movieId']

            # print("Imdb Id = {}  Tmdb Id = {} Movie Id = {}".format(imdbid, tmdbid, movieid))

            #Prepending tt and 0's to transform the imdb ids to it's correct format 
            querystring = {"r":"json","i":"tt{}".format(str(imdbid).zfill(7))}

            #Api urls
            imdburl = "https://movie-database-alternative.p.rapidapi.com/"
            tmdburl = "https://api.themoviedb.org/3/movie/{}?api_key=34716158ed3bedaedfa4dd37ea314e12".format(tmdbid)
            
            try:
                #Calling rapid api for IMDB data
                imdbresponse = self.manager.fetch(imdburl, "GET", fields = querystring, headers = rapid_api_headers)
                imdbdict = json.loads(imdbresponse.data)
                imdbdict['_id'] = movieid
                if imdbresponse.status == 200:
                    self.receive_response(imdbdict, self.IMDB)

                #Calling tmdb api 
                tmdbresponse = self.manager.fetch(tmdburl, "GET")
                tmdbdict = json.loads(tmdbresponse.data)
                tmdbdict['_id'] = movieid
                if tmdbresponse.status == 200:
                    self.receive_response(tmdbdict, self.TMDB)
                
                api_calls_count += 1
                if imdbresponse.status == 200 or tmdbresponse.status == 200:
                    count += 1
                else:
                    continue
            
                #print("\nRecord count : {}  Api Call Count : {}  Batch count : {} \n".format(str(count), str(api_calls_count), str(batch)))
                should_update_state = False
                should_return = False
                status = "In Progress"
                
                #Updating api call state when download is complete
                if ((batch * batch_size ) + count) == len(self.df):
                    print("Downloaded all records from the server")
                    should_update_state = True
                    should_return = True
                    status = "Complete"
                #Checking after each api call if the daily limit has reached, update the api call state and return
                elif api_calls_count >= RestClient.DAILY_API_CALL_LIMIT:
                    print("Max Api call limit for the day reached")
                    should_return = True
                    should_update_state = True
                #Checking if the end of a batch has arrived and update the state
                elif count >= batch_size:
                    print("Batch number : {} downloaded successfully".format(str(batch)))
                    batch += 1
                    count = count - batch_size if count > batch_size else 0
                    should_update_state = True
                if should_update_state:
                    new_state = DownloadProgressState(date = date.today().strftime('%d/%m/%Y'), api_calls_today = api_calls_count,                                                                 current_batch = batch, record_no = count, overall_status = status)
                    new_state.reset_date()
                    self.update_state(new_state)
                    time.sleep(3)
                    if should_return:
                        return
                
            except:
                    new_state = DownloadProgressState(date = date.today().strftime('%d/%m/%Y'), api_calls_today = api_calls_count, 
                                                             current_batch = batch, record_no = count)
                    self.update_state(new_state)
                    continue
