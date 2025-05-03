# import required libraries
import requests as rq
import pandas as pd
import time

# url of API
url = 'https://api.coingecko.com/api/v3/coins/markets'

# create an empty list to store data in loop
all_data = []

# iterate over a loop and get more data
for page in range(1, 50):

    # define parameters
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': page,
        'sparkline': False
    }

    # make a connection to API
    api_response = rq.get(url, params = params)

    # check the response
    if api_response.status_code == 200:
        # get data in json format
        data = api_response.json()

        # check if data is not present just break
        if not data:
            print(f"Data not found in {page}")
            break
        # data addition to list
        all_data.extend(data)
        time.sleep(1.5)
    elif api_response.status_code == 429:
        print(f"Rate limit hit on page {page}. waiting 60 seconds before retrying...")
        time.sleep(60)
        continue
    else:
        print(f"Failed to fetch page {page}: {api_response.status_code}")
        break

# pandas dataframe
dataset = pd.DataFrame(all_data)

print(dataset[['id', 'symbol', 'current_price', 'market_cap', 'total_volume']])
# shape
print("Dataset dimensions: ", dataset.shape)