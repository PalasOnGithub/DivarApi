import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import jwt
import datetime


class Client:
    def __init__(self , header:dict = None , db_usage:bool = False , db_name:str = None):
        '''
            setting up things needed to run the instance , but all the arguments are clearly optional!
            wrote by Love and Tea from @RealPalas , dedicated to iranian devs
        '''
        self._header = header
        self._Cookie = self._header.get('Cookie')
        self._db_name = db_name if db_name and db_usage == True else 'db.sqlite3'

        if self._header is None:
            self._header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        
    def get_newest_category(self , city:str , category_name:str , jsonify:bool = False  , json_path:str = 'data_file.json', db_usage:bool = False , db_table_name:str = 'information'):
        
        url = f'https://divar.ir/s/{city}/{category_name}'
        req = requests.get(url, headers=self._header)

        if req.status_code == 200 or 201:
            soup = BeautifulSoup(req.text, "html.parser")

            all_data = soup.find_all("script" , {"type": "application/ld+json"})
            all_data = all_data[-1]

            if jsonify:
                try:
                    with open(json_path, "w") as write_file:
                        jsn = json.loads(all_data.string)
                        json.dump(jsn, write_file , indent=4 , sort_keys=True)

                except ValueError:
                    raise ValueError('an error accoured when tried to jsonify the data')
            
            elif db_usage:
                #making and stablishing databse connection
                db_connection = sqlite3.connect(self._db_name)
                db_cursor = db_connection.cursor()

                #repesent the table rows
                db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {db_table_name}
                    (context TEXT ,type TEXT ,accommodationCategory TEXT ,description TEXT ,floorSize TEXT ,address TEXT ,latitude TEXT ,longitude TEXT ,image_url TEXT ,name TEXT ,numberOfRooms TEXT ,url TEXT ,web_info TEXT)''')
                
                db_connection.commit() # commiting the table in db

                jsn = json.loads(all_data.string)
                data = json.dumps(jsn, indent=4 , sort_keys=True)# making a json from raw bs4 instance

                #preparing db insert statement
                sqlite_insert_with_param = f"""INSERT INTO {db_table_name}
                    (context, type, email, accommodationCategory, description, floorSize, address, latitude, longitude, image_url, name, numberOfRooms , url, web_info) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?);"""
                
                cache_list = list()
                reverse_data = json.loads(data)# returning the json into python stracture so we can read the data
                for obj in reverse_data:
                    cache_list.append(tuple(obj['@context'] , 
                     obj['@type'] , 
                     obj['accommodationCategory'] , 
                     obj['description'] , 
                     obj['floorSize']['value'] ,
                     obj['geo']['address'] , 
                     obj['geo']['latitude'] , 
                     obj['geo']['longitude'] , 
                     obj['image'] , 
                     obj['name'] , 
                     obj['numberOfRooms'] , 
                     obj['url'] , 
                     obj['web_info']['city_persian']))

                    try:
                        db_cursor.executemany(sqlite_insert_with_param, cache_list)
                        db_connection.commit()
                        print("Total", db_cursor.rowcount, f"Records inserted successfully into {db_table_name} table")

                    except Exception as e:
                        raise Exception(f'{e}\n couldnt make the row in database \n be sure the data doesnt exists before this and change the connection to sqlite3!')
                
                db_cursor.close()
                db_connection.close()

            else:
                return all_data #returning the main data in bs4 instance format 
    
    def get_number(self , Token:str):
        try:
            jwt_token = self._Cookie.split('; token=')[1].split(';')[0]
            payload = jwt.decode(jwt_token , algorithms = ['HS512'])
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            
            self._lark = False if datetime.datetime.now() > exp_time else True

        except Exception as e:
            raise Exception(f'{e} the was an error during checking the jwt token')

        if self._lark:
            req = requests.get(
                f"https://api.divar.ir/v8/postcontact/web/contact_info/{Token}", headers=self._session
            )

            if req.status_code == 200 or 201:
                jsn = json.loads()

                if jsn['widget_list'][0]['data']['title'] == '\u0634\u0645\u0627\u0631\u0647 \u0645\u062e\u0641\u06cc \u0634\u062f\u0647 \u0627\u0633\u062a':
                    return 'Hidden Number!'
                
                else:
                    return jsn['widget_list'][0]['data']['action']['payload']['phone_number']
                
            else:
                raise Exception('Couldnt find the Token you specified , please replace it with a good one')
                
        else:
            raise Exception('The JWT Token is expired , plz replace it and try again')
        
    def get_post_pic(self , id:int , Token:str , path:str):
        try:
            jwt_token = self._Cookie.split('; token=')[1].split(';')[0]
            payload = jwt.decode(jwt_token , algorithms = ['HS512'])
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            
            self._lark = False if datetime.datetime.now() > exp_time else True

            if self._lark:
                req = requests.get(
                f"https://s100.divarcdn.com/static/thumbnails/{id}/{Token}.jpg", headers=self._header
                )
                
                if req.status_code == 200 or 201:
                    with open(path, 'wb') as file:
                        for chunk in req:
                            file.write(chunk)

                else:
                    raise Exception(f'{req.status_code} -> Bad Request!')
                
            else:
                raise Exception('the cookie you specified is not correct! or jwt is expired')

        except Exception as e:
            raise Exception(f'{e} the was an error during checking the jwt token')
        

    def __str__(self):
        return 'an instance of DivarApi pkg'
        
    
                

