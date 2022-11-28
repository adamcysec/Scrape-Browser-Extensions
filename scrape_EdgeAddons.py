import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import json

def main():
    #start_time = time.time()

    #sitemap_url = 'https://microsoftedge.microsoft.com/sitemap.xml'

    #sitemap_xml = get_site_map(sitemap_url)
    #sitemap_urls = get_site_map_urls(sitemap_xml)

    num = 100
    edge_query_url = f'https://microsoftedge.microsoft.com/addons/v3/getfilteredsearch?hl=en-US&gl=US&filteredCategories=Edge-Extensions&pgNo={num}&Query=*'
    get_edge_query(edge_query_url)
    print()

def get_edge_query(edge_query_url):
    response = requests.get(edge_query_url)
    print()


def get_site_map(url):
    """get the webstore sitemap xml text

    Returns:
    --------
    response.text : str
        sitemap xml text
    """

    response =  requests.get(url)

    return response.text

def get_site_map_urls(sitemap_xml):
    """get the webstore shard urls from the sitemap

    Parameters:
    -----------
    sitemap_xml : str
        raw xml
    
    Returns:
    --------
    sitemap_urls : list
        webstore shard urls
    """
    
    soup = BeautifulSoup(sitemap_xml, 'xml')
    urls = soup.find_all('loc')

    sitemap_urls = []

    for url in urls:
        sitemap_urls.append(url.text)

    return sitemap_urls


if __name__ == '__main__':
    main()