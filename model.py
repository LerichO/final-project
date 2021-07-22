import requests
def search(term, location, api_key ):

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
    for x in 10:
       name = response["businesses"][x]["name"]
       location = response["businesses"][0]["location"]["city"]
       businesses["name"].append(name)
       businesses["location"].append(location)
    return businesses
