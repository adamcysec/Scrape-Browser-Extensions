import requests
from bs4 import BeautifulSoup
#import urllib.parse
import time
#import json
from datetime import datetime
import csv
#import codecs
from multiprocessing import Pool, cpu_count


# edge categories
# Accessibility
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Accessibility?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=tru

# Blogging
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Blogging?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Communication
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Communication?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Developer-Tools
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Developer-Tools?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Entertainment
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Entertainment?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# News-And-Weather
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/News-And-Weather?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Photos
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Photos?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Productivity
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Productivity?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Search-Tools
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Search-Tools?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Shopping
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Shopping?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Social
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Social?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true

# Sports
# https://microsoftedge.microsoft.com/addons/getfilteredextensions/Sports?hl=en-US&gl=US&noItems=24&pgNo=1&IncludeExtensionDetailsFields=true


def main():
    start_time = time.time()

    categories = [
        "Accessibility",
        "Blogging",
        "Communication",
        "Developer-Tools",
        "Entertainment",
        "News-And-Weather",
        "Photos",
        "Productivity",
        "Search-Tools",
        "Shopping",
        "Social",
        "Sports"
    ]

    print(f"starting work on {cpu_count()} cores")

    with Pool() as pool:
        res = pool.map(work_job, categories)
        # the results from the Pool returns a list within a list within a list with a dict
        # eg. res = [[{id, name}],[{}],[{}],[{}]...]


    print(f"--- {time.time() - start_time} seconds ---")
    
    out_csv_file(res, 'edge_extensions.csv')

def work_job(category):
    all_extension_dict = []
    
    pageNo = 1
    more_data = True
    
    while more_data:
        edge_query_url = f"https://microsoftedge.microsoft.com/addons/getfilteredextensions/{category}?noItems=24&pgNo={pageNo}&IncludeExtensionDetailsFields=true"
        extension_json  = get_edge_query(edge_query_url)
        more_data = extension_json['hasMorePages']
        extension_dict = parse_extension_json(extension_json)
        all_extension_dict.append(extension_dict)
        pageNo += 1

    return all_extension_dict

def parse_extension_json(json_data):
    extension_dict = []
    
    extension_list = json_data['extensionList']

    for item in extension_list:
        extension_id = item['crxId']
        extension_name = item['name']
        extension_dict.append({'id' : extension_id, 'name' : extension_name})
    
    return extension_dict

def get_edge_query(edge_query_url):
    response = requests.get(edge_query_url)
    
    return response.json()

def out_csv_file(data, outfilename):
    """save Chrome extensions to csv file.

    Parameters:
    -----------
    data : list
        a list of lists containing dicts
    outfilename : str
        user supplied file name
    """
    
    if outfilename:
        file_name = outfilename
    else:
        file_name = f"chrome_webstore_extensions_{datetime.now().strftime('%Y-%m-%d')}.csv"

    field_names = ['id', 'name']

    with open(file_name, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for item1 in data:
            for item2 in item1:
                writer.writerows(item2)

    print(f"file saved: {file_name}")


if __name__ == '__main__':
    main()