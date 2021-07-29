
import requests
global business_list


# -- Algorithm to find highest review count of all businesses --
def find_highest_review_count(b_list_raw):
    sorted_list = []
    for x in range(len(b_list_raw)):
        sorted_list.append(b_list_raw[x]["review_count"])
        # print(b_list_raw[x]["review_count"]) # -- for debugging --
    sorted_list = sorted(sorted_list)
    # print(sorted_list) # -- for debugging --
    highest = sorted_list[len(sorted_list) - 1]
    print("highest review count: " + str(highest))
    return highest

# -- Algorithm to find lowest review count of all businesses --
def find_lowest_review_count(b_list_raw):
    sorted_list = []
    for x in range(len(b_list_raw)):
        sorted_list.append(b_list_raw[x]["review_count"])
        # print(b_list_raw[x]["review_count"]) # -- for debugging --
    sorted_list = sorted(sorted_list)
    lowest = sorted_list[0]
    print("lowest review count: " + str(lowest))
    return lowest

# -- Algorithm to find median review count of all businesses --
def find_median_review_count(b_list_raw):
    sorted_list = []
    for x in range(len(b_list_raw)):
        sorted_list.append(b_list_raw[x]["review_count"])
    sorted_list = sorted(sorted_list)
    print("median: " + str(sorted_list[int(len(sorted_list) / 2)]))
    return sorted_list[int(len(sorted_list) / 2)]

# -- Algorithm to find average review count of all businesses --
def find_average_review_count(b_list_raw):
    total = 0
    for x in range(len(b_list_raw)):
        total += b_list_raw[x]["review_count"]
    print("average: " + str(float(total) / len(b_list_raw)) + "\n")
    return float(total) / len(b_list_raw)

# -- algorithm that can somewhat identify small businesses --
# -- might need/want to include Yelp Program API --
def small_business_sort(api_url, headers, location, b_list):
    processed = []
    score_list = []
    highest_review_count = find_highest_review_count(b_list)
    lowest_review_count = find_lowest_review_count(b_list) # -- leave here in case of debugging purposes --
    median_review_count = find_median_review_count(b_list)
    average_review_count = find_average_review_count(b_list)
    true_mid = float(median_review_count + average_review_count) / 2

    # -- meat of the algorithm --
    for x in range(len(b_list)):
        score = 0

        # -- Step 1 --
        score += (highest_review_count - b_list[x]["review_count"])
        if b_list[x]["review_count"] < median_review_count:
            # print(true_mid - b_list[x]["review_count"]) # -- for debugging --
            score -= (true_mid - b_list[x]["review_count"]) * 2
        # print(score) # -- for debugging --

        # -- Step 2 --
        score += int((b_list[x]["rating"] - 3) * 300)

        # -- Step 3. --
        if b_list[x].get("price", None) != None:
            # print(b_list[x].get("price", None)) # -- for debugging --
            score += ((4 - len(b_list[x]["price"])) * 200)
        else:
            score += 600
        # print(score) # -- for debugging --

        # -- Step 4. --
        b_item_name = b_list[x]["name"]
        b_item_categories = b_list[x].get("categories", None) # -- leave here for future usage --
        b_item_params = {'term': b_item_name,
                         'location': location,
                        #  'categories': b_item_categories,
                         'radius': 40000}
        b_items = requests.get(api_url, headers=headers, params=b_item_params, timeout=5).json()
        # print(b_items)
        clone_count = 0
        for iteration in b_items["businesses"]:
            if b_item_name == iteration["name"] and b_list[x]["location"]["address1"] != iteration["location"]["address1"]:
                # if b_list[x]["location"]["address1"] == iteration["location"]["address1"]:
                #     clone_count += 1
                clone_count +=1
        # count_calc = clone_count / 10
        score -= clone_count*200
        
        score = int(score)
        # processed[b_list[x]["review_count"]] = score
        processed.append({'business': b_list[x],
                          'score': score})
        score_list.append(score)
    export = []
    processed = sorted(processed, key = lambda i: i['score'],reverse=True)

    print ("The list printed sorting by age in descending order: ")
    for i in range(len(processed)):
        # print(str(processed[i]["score"]) + " : " + str(processed[i]["business"]["name"])) # -- for debugging --
        if processed[i]["score"] > processed[int(len(processed) / 2) - 1]["score"]:
            export.append(processed[i]["business"])
    
    # -- START OF DEBUGGING --
    sorted_list = []
    for x in range(len(b_list)):
        sorted_list.append(b_list[x]["review_count"])
    # print(b_list_raw[x]["review_count"]) # -- for debugging --
    # sorted_list = sorted(sorted_list)
    # for count in sorted_list:
    #     print(str(count) + " : " + str(processed[count]))
    print(sorted_list)  # -- for debugging --
    # print(processed) # -- for debugging --
    # -- END OF DEBUGGING --

    return export

def search(term, location, api_key):
    global business_list
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    search_api_url = 'https://api.yelp.com/v3/businesses/search'

    # -- We can start adding price range or minimum rating as parameters --
    params = {'term': term,
              'location': location,
              'limit': 50}  # -- find out how to change out limit --

    # -- START OF DEBUGGING --
    # cheddars_cat = [
    #         {
    #            "alias":"chicken_wings",
    #            "title":"Chicken Wings"
    #         },
    #         {
    #            "alias":"hotdogs",
    #            "title":"Fast Food"
    #         }
    #      ]
    # cheddars_params = {'term': "Cheddar's Scratch Kitchen",
    #                    'location': location,
    #                    'radius': 40000}
    # cheddars = requests.get(search_api_url, headers=headers, params=cheddars_params, timeout=5).json()
    # # print(cheddars)
    # for x in cheddars["businesses"]:
    #     if x.get("name", None) == "Cheddar's Scratch Kitchen":
    #         print(x)
    # -- END OF DEBUGGING --

    response = requests.get(search_api_url, headers=headers, params=params, timeout=5).json()

    exported_list = []
    # -- will eventually return a FINAL list of busiesses --
    exported_list = small_business_sort(search_api_url, headers, location, response["businesses"])
    business_list = []
    for item in exported_list:
        business_list.append(item)

    # -- Method 2
    # business_list = {"total": response["total"],"businesses" : [], "region": response["region"]}
    # business_list["businesses"] = exported_list

    #  -- Method 1 --
    # for x in range(len(response["businesses"])): # -- change response/processed --
    #     business_list.append(response["businesses"][x])
    #     # print(response["businesses"][x]["price"])
    return business_list
