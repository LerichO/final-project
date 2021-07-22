import requests
global businesses

def search(term, location, api_key ):
    global businesses
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    search_api_url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': term, 
          'location': location,
          'limit': 10}
    response = requests.get(search_api_url, headers=headers, params=params, timeout=5).json()
    businesses = {
        "name":[],
        "location":[]
    }
    for x in range(params["limit"]):
       name = response["businesses"][x]["name"]
       location = response["businesses"][x]["location"]["city"]
       businesses["name"].append(name)
       businesses["location"].append(location)
    return businesses
