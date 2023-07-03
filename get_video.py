import requests
import json
import random
import os

# replace this with the API key you got from Google
API_KEY = 'YOUR_API_KEY'

def get_popular_videos(region_code='US', max_results=50):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode={region_code}&maxResults={max_results}&key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something Else:",err)
    else:
        return response.json()

# use the function to get popular videos
data = get_popular_videos(max_results=50)

# get a random video from the list
if data:
    random_video = random.choice(data['items'])
    print(f"Video ID: {random_video['id']}")
    print(f"Title: {random_video['snippet']['title']}")
    
    # create the datasets folder if it doesn't exist
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    
    # save the data to a JSON file in the datasets folder
    with open(f'datasets/data.json', 'w') as f:
        json.dump(data, f)

