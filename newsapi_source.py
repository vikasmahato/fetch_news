import pprint

from newsapi.newsapi_client import NewsApiClient

# Init
client = NewsApiClient(api_key='ba429edc68624c228c1c56ed6978c3f2')

# /v2/top-headlines
# top_headlines = client.get_top_headlines(q='bitcoin',
#                                           sources='bbc-news,the-verge',
#                                           category='business',
#                                           language='en',
#                                           country='us')

# /v2/everything
all_articles = client.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2025-03-16',
                                      to='2025-03-16',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

pprint.pprint(all_articles)

# /v2/top-headlines/sources
sources = client.get_sources()
pprint.pprint(sources)