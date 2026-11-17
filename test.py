import time
import requests

host = "https://lrclib.net/api"
headers = {"User-Agent":"lrcsearcher v1.0 (https://github.com/flup1212/lrcsearcher)"}
title = "Starman"
artist = "David Bowie"
len = 100

def do_thign():
    response = requests.get(host+"/get?"+"track_name="+title+"&artist_name="+artist, headers=headers)

    if response.status_code == 200:
        #print(response.json().get("plainLyrics"))
        print("yes")
    elif response.status_code == 429:
        retry_after = response.json().get("Retry-After", 0)
        if retry_after > 0:
            print(f"Rate limit exceeded, retrying in {retry_after}")
            time.sleep(retry_after)
        else:
            print("Rate limit exceeded, retrying in 1 second")
            time.sleep(1)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

i = 0
for i in range(20):
    i += 1
    do_thign()