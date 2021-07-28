
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
# -- might need to include Yelp Program API --
def small_business_sort(term, b_list):
    processed = {}
    score_list = []
    highest_review_count = find_highest_review_count(b_list)
    lowest_review_count = find_lowest_review_count(b_list)
    median_review_count = find_median_review_count(b_list)
    average_review_count = find_average_review_count(b_list)
    true_mid = float(median_review_count + average_review_count) / 2

    # -- meat of the algorithm --
    for x in range(len(b_list)):
        # #reviews_api_url = 'https://api.yelp.com/v3/businesses/' + b_list[x]["id"] + "/reviews"
        # #-- ^^ use this for later somewhere else ^^ --
        score = 0

        # Step 1.
        score += (highest_review_count - b_list[x]["review_count"])

        # Step 2.
        if b_list[x]["review_count"] < median_review_count:
            print(true_mid - b_list[x]["review_count"])
            score -= (true_mid - b_list[x]["review_count"]) * 2
        # print(score) # -- for debugging --

        # Step 3.
        score += int((b_list[x]["rating"] - 3) * 10)

        # Step 4.
        if b_list[x].get("price", None) != None:
            # print(b_list[x].get("price", None)) # -- for debugging --
            score += ((4 - len(b_list[x]["price"])) * 300)
        else:
            score += 600
        # print(score) # -- for debugging --

        score = int(score)
        processed[b_list[x]["review_count"]] = score
        score_list.append(score)

    # -- START OF DEBUGGING --
    sorted_list = []
    for x in range(len(b_list)):
        sorted_list.append(b_list[x]["review_count"])
    # print(b_list_raw[x]["review_count"]) # -- for debugging --
    sorted_list = sorted(sorted_list)
    for count in sorted_list:
        print(str(count) + " : " + str(processed[count]))
    # print(sorted_list)  # -- for debugging --
    # print(processed) # -- for debugging --
    # -- END OF DEBUGGING --

def search(term, location, api_key):
    global business_list
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    search_api_url = 'https://api.yelp.com/v3/businesses/search'

    # -- We can start adding price range or minimum rating as parameters --
    params = {'term': term,
              'location': location,
              'limit': 50}  # -- find out how to change out limit --

    response = requests.get(search_api_url, headers=headers, params=params, timeout=5).json()
    # for x in range(len(response["businesses"])): # -- for debugging categories param --
    #     print(response["businesses"][x]["categories"]) # -- for debugging categories param --


    # -- will eventually return a FINAL list of busiesses --
    small_business_sort(term, response["businesses"])


    business_list = []
    for x in range(len(response["businesses"])): # -- change response/processed --
        business_list.append(response["businesses"][x])
        # print(response["businesses"][x]["price"])
    return business_list
