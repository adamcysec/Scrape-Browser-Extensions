import requests
from bs4 import BeautifulSoup
#import urllib.parse
import time
import json
from multiprocessing import Pool, cpu_count
import csv
from datetime import datetime


def main():
    start_time = time.time()

    root_sitemap_url = 'https://chrome.google.com/webstore/sitemap'
    # get the top level sitemap shard urls
    root_sitemap_xml = get_site_map(root_sitemap_url)
    root_sitemap_urls = get_site_map_urls(root_sitemap_xml)

    # create queue for mutliprocessing
    queue = root_sitemap_urls

    print(f"starting work on {cpu_count()} cores")
    # start multi processing search
    with Pool() as pool:
        res = pool.map(parse_extensions, queue)
    # the results from the Pool returns a list within a list
    # eg. res = [[{id, name}],[{}],[{}],[{}]...]

    print(f"--- {time.time() - start_time} seconds ---")
    # save results to file
    out_csv_file(res)

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
    """save each extension url into a dict

    Parameters:
    -----------
    shard_url : str
        shard url contains potentially up to 300 extension urls

    Returns:
    --------
    chrome_webstore_dict : list
        a list containing dict
    """
    
    # for each sitemap shard
    # get the extension urls
    # store the extension name and id in chrome_webstore_dict

    shard_sitemap_xml = get_site_map(shard_url)
    shard_sitemap_urls = get_site_map_urls(shard_sitemap_xml)

    chrome_webstore_dict = []

    for url in shard_sitemap_urls:
        parts = url.split('/')
        #extension_name = urllib.parse.unquote(parts[5]) # url decode extension names
        extension_name = parts[5]
        extension_id = parts[6]

        if '?' in extension_id:
            id_parts = extension_id.split('?')
            extension_id = id_parts[0]

        chrome_webstore_dict.append({'id' : extension_id, 'name' : extension_name})

    return chrome_webstore_dict

def out_csv_file(data):
    """save Pool results to csv file.

    Parameters:
    -----------
    data : list
        a list of lists containing dicts
    """
    
    field_names = ['id', 'name']
    file_name = f"chrome_webstore_extensions_{datetime.now().strftime('%Y-%m-%d')}.csv"

    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for item in data:
            writer.writerows(item)

    print(f"file saved: {file_name}")


if __name__ == '__main__':
    main()