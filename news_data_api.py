from newsdataapi import NewsDataApiClient

from get_secrets import get_news_data_api_key

# API key authorization, Initialize the client with your API key

api = NewsDataApiClient(apikey=get_news_data_api_key())

# You can pass empty or with request parameters {ex. (country = "us")}

response = api.latest_api( q= "ronaldo" , country = "us")

"""
def latest_api(
            self, q:Optional[str]=None, qInTitle:Optional[str]=None, country:Optional[Union[str, list]]=None, category:Optional[Union[str, list]]=None,
            language:Optional[Union[str, list]]=None, domain:Optional[Union[str, list]]=None, timeframe:Optional[Union[int,str]]=None, size:Optional[int]=None,
            domainurl:Optional[Union[str, list]]=None, excludedomain:Optional[Union[str, list]]=None, timezone:Optional[str]=None, full_content:Optional[bool]=None,
            image:Optional[bool]=None, video:Optional[bool]=None, prioritydomain:Optional[str]=None, page:Optional[str]=None, scroll:Optional[bool]=False,
            max_result:Optional[int]=None, qInMeta:Optional[str]=None, tag:Optional[Union[str,list]]=None, sentiment:Optional[str]=None,
            region:Optional[Union[str,list]]=None,excludefield:Optional[Union[str,list]]=None,removeduplicate:Optional[bool]=None,raw_query:Optional[str]=None
        )->dict:
        """
print(response)

sources = api.sources_api()