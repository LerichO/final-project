import requests
global businesses

def search(term, location, api_key ):
    global business_list
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    search_api_url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': term, 
          'location': location,
          'limit': 10}
    response = requests.get(search_api_url, headers=headers, params=params, timeout=5).json()
    business_list = []
    for x in range(params["limit"]):
       business_list.append(response["businesses"][x]) #this might not run for now but I'll probabl get back to it tonight/friday 
                                                       # -Lerich
    return business_list
