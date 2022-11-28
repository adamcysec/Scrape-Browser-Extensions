import requests
from bs4 import BeautifulSoup
#import urllib.parse
import time
import json
from multiprocessing import Pool, cpu_count

def main():
    start_time = time.time()

    root_sitemap_url = 'https://chrome.google.com/webstore/sitemap'
    # get the top level sitemap shard urls
    root_sitemap_xml = get_site_map(root_sitemap_url)
    root_sitemap_urls = get_site_map_urls(root_sitemap_xml)

   

    queue = root_sitemap_urls

    print(f"starting work on {cpu_count()} cores")
    # start multi processing search
    with Pool() as pool:
        res = pool.map(parse_extensions, queue)

    print(f"--- {time.time() - start_time} seconds ---")
    out_json_file(res)

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

def parse_extensions(shard_url):
    # for each sitemap shard
    # get the extension urls
    # store the extension name and id in chrome_webstore_dict

    shard_sitemap_xml = get_site_map(shard_url)
    shard_sitemap_urls = get_site_map_urls(shard_sitemap_xml)

    chrome_webstore_dict = {}

    for url in shard_sitemap_urls:
        parts = url.split('/')
        #extension_name = urllib.parse.unquote(parts[5])
        extension_name = parts[5]
        extension_id = parts[6]
        chrome_webstore_dict[extension_id] = extension_name

    return chrome_webstore_dict

def out_json_file(chrome_webstore_dict):
    with open('./chrome_webstore_extensions.txt', 'w') as f:
        json.dump(chrome_webstore_dict, f)



if __name__ == '__main__':
    main()