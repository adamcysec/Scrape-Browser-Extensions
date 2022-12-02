import requests
from bs4 import BeautifulSoup
#import urllib.parse
import time
from multiprocessing import Pool, cpu_count
import csv
from datetime import datetime

def main():
    start_time = time.time()

    root_sitemap_url = 'https://chrome.google.com/webstore/sitemap'
    # get the top level sitemap shard urls
    root_sitemap_xml = get_sitemap(root_sitemap_url)
    root_sitemap_urls = parse_sitemap_xml(root_sitemap_xml)

    # create queue for mutliprocessing
    queue = root_sitemap_urls

    print(f"starting work on {cpu_count()} cores")

    with Pool() as pool:
        res = pool.map(parse_extensions, queue)
    # the results from the Pool returns a list within a list
    # eg. res = [[{id, name}],[{}],[{}],[{}]...]

    print(f"--- {time.time() - start_time} seconds ---")
    
    out_csv_file(res)

def get_sitemap(url):
    """get the sitemap xml text
    

    Parameters:
    -----------
    url : str
        sitemap url

    Returns:
    --------
    response.text : str
        sitemap xml text
    """
    response =  requests.get(url)

    return response.text

def parse_sitemap_xml(sitemap_xml):
    """parse the webstore urls from the sitemap xml
    
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
    """multiprocess job to save extension data into a dict
    
    Parameters:
    -----------
    shard_url : str
        shard url contains potentially up to 300 extension urls
    
    Returns:
    --------
    chrome_webstore_dict : list
        a list containing dict
    """

    shard_sitemap_xml = get_sitemap(shard_url)
    shard_sitemap_urls = parse_sitemap_xml(shard_sitemap_xml)

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
    """save chrome extensions to csv file.
    
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