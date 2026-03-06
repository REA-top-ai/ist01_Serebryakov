import requests as r

BASE_URL = 'https://newsapi.org/v2'
apikey = "925f63e18e8242a388d64c2b01e448c7"

"""def everything(base_url: str, #основа ссылки
                endpoint: str, # использование в апишке,
                api_key:str, 
                q:str, # query
                sources:str) -> str:

    return "s" """

def _make_request (endpoint: str,
                   apikey: str,
                   params: dict) -> dict[str, str]:
    url = f'{BASE_URL}/{endpoint}'
    default_params = {'apikey': apikey}

    if params: 
        default_params.update(params)

    try:
        response = r.get(url, params=default_params, timeout=10)
        return response.json()
    
    except r.exceptions.RequestException as e:
        raise Exception(f'Error request NEWSAPI {endpoint} : {e}')
    
    except ValueError as e:
        raise Exception(f'Error parsing JSON ({endpoint})')

def get_top_headlines(apikey = None, 
                        q: str = None,
                        country: str = None,
                        category: str = None,
                        sources: str = None,
                        pageSize: int = None,
                        page: str = None) -> dict[str, str]:
    params = {'q': q, 'country': country, 'category':category, "sources": sources, 'pageSize':pageSize, "page":page}
    params_final = {key:value for key, value in params.items() if value is not None}
    return _make_request('top-headlines', apikey, params_final)

def get_everything(api_key: str = None,
                  q: str = None,
                  search_in: str = None,
                  sources: str = None,
                  domains: str = None,
                  exclude_domains: str = None,
                  from_date: str = None,
                  to_date: str = None,
                  language: str = None,
                  sort_by: str = None,
                  page_size: int = None,
                  page: int = None) -> dict:
   
    allow = {
        "apiKey": api_key,
        "q": q,
        "searchIn": search_in,
        "sources": sources,
        "domains": domains,
        "excludeDomains": exclude_domains,
        "from": from_date,
        "to": to_date,
        "language": language,
        "sortBy": sort_by,
        "pageSize": page_size,
        "page": page
    }
    #вопрос по механике, если мы через kwargs будем передавать параметры, мы ж буквальгно тот же самый словарь будем формировать, только не будем проверять его руками, а будем его формировать через kwargs, так?
    params = {key: value for key, value in allow.items() if value is not None}
    return _make_request("everything", api_key, params)

#вроде как работает, по крайней мере я проверил))))) попробуйте у себя
def everything_kwarg(apikey: str = None,
        **kwargs) -> dict:
    return _make_request("everything", apikey, kwargs)

def get_sources(api_key: str = None,
               category: str = None,
               language: str = None,
               country: str = None) -> dict:
   
   allowed_params = {
    "apiKey": api_key,
    "category": category,
    "language": language,
    "country": country
    }

   params = {key: value for key, value in allowed_params.items() if value is not None}
   return _make_request("sources", api_key, params)

def sources_kwarg(apikey: str = None,
        **kwargs) -> dict:
    return _make_request("sources", apikey, kwargs)
#ну по идее тоже можно через кваргс

