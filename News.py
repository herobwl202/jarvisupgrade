import requests
from ss import *
from ss import *
api_adress = "http://newsapi.org/v2/top-headlines?country=us&apiKey=" + key
json_data = requests.get(api_adress).json() # search for the URL

ar = []

def news():
    for i in range(3):
        ar.append("Number " + str(i+1)+". " + json_data["articles"][i]["title"]+".")

    return ar