"""import requests as r
import pprint
apikey = "925f63e18e8242a388d64c2b01e448c7"
resp = input()
url = "https://newsapi.org/v2/everything?q="+resp+"&apiKey="+apikey
result = r.get(url)
pprint.pprint(result.json()['articles'][0]['url'])
 """
from client.api_methods import get_top_headlines
import pprint
apikey = "925f63e18e8242a388d64c2b01e448c7"

if __name__ == '__main__':
    result = get_top_headlines(apikey, q="apple")
    pprint.pprint(result)
    