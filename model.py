
import requests
global business_list  

def search(term, location, api_key):
    global business_list
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    search_api_url = 'https://api.yelp.com/v3/businesses/search'

    # -- We can start adding price range or minimum rating as parameters --
    params = {'term': term, 
          'location': location,
          'limit': 12}

    # -- succesfully sends and renders items on results.html --
    response = requests.get(search_api_url, headers=headers, params=params, timeout=5).json()
    business_list = []
    for x in range(params["limit"]): 
        business_list.append(response["businesses"][x])
        # print(response["businesses"][x]["price"])

    # -- algorithm that can somewhat identify small businesses --
    # -- might need to include Yelp Program API
    return business_list
