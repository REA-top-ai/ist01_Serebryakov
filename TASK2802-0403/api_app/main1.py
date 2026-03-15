"""import requests as r
import pprint
apikey = "925f63e18e8242a388d64c2b01e448c7"
resp = input()
url = "https://newsapi.org/v2/everything?q="+resp+"&apiKey="+apikey
result = r.get(url)
pprint.pprint(result.json()['articles'][0]['url'])
 """
from client.api_methods import get_top_headlines, get_everything
import pprint
apikey = "*"

if __name__ == '__main__':
    out = []
    result = get_top_headlines(apikey, country="us")
    #result = get_everything(apikey, from_date="2026-03-14", sort_by="publishedAt") просит обязательно сортировать по основным аргументам(q, source, domains), не особо мне нравится
    count = 0
    for j in range(1,50):
        result = get_top_headlines(apikey, country="us", page="{j}")  
        if count < 50:
            for i in result["articles"]:
                if i["description"]!=None and i["title"] != None and i["title"] != " "  and i["url"] != None and len(i["description"]) >= 50 and count < 50:
                    count+=1
                    #print(i["publishedAt"]) проверка на самые новые, показывает что есть только вчерашние
                    out.append({
                        "title": i["title"],
                        "source": i["source"]["name"],
                        "published": i["publishedAt"],
                        "author": i["author"]
                    })
        else:
            break
    print(out)
    print(len(out))