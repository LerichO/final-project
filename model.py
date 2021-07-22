import requests
def search(term, location, api_key ):

    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    search_api_url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': term, 
          'location': location,
          'limit': 10}
    response = requests.get(search_api_url, headers=headers, params=params, timeout=5).json()

    return response["businesses"][0]["name"]
