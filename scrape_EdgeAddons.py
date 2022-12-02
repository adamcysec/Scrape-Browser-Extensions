import requests
import time
from datetime import datetime
import csv
from multiprocessing import Pool, cpu_count

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
        # eg. res = [[[{id, name}],[{}],[{}],[{}]]...]


    print(f"--- {time.time() - start_time} seconds ---")
    
    out_csv_file(res)

def work_job(category):
    """multiprocess job to query and extract edge extensions

    Parameters:
    -----------
    category : str
        extension category
    
    Returns:
    --------
    all_extension_dict : list
        list of lists containing a dict of extension data
    """

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
    """parse extension data from json objs

    Parameters:
    -----------
    json_data : dict
        edge extension dict

    Returns:
    --------
    extension_dict : dict
        extracted extension data
    """
    
    extension_dict = []
    
    extension_list = json_data['extensionList']

    for item in extension_list:
        extension_id = item['crxId']
        extension_name = item['name']
        extension_dict.append({'id' : extension_id, 'name' : extension_name})
    
    return extension_dict

def get_edge_query(edge_query_url):
    """query edge store api for extensions

    Parameters:
    -----------
    edge_query_url : str
        edge query url

    Returns:
    --------
    extensions_json : json objects
        list of json objs
    """
    
    response = requests.get(edge_query_url)
    extensions_json = response.json()
    
    return extensions_json

def out_csv_file(data):
    """save Chrome extensions to csv file.

    Parameters:
    -----------
    data : list
        a list of list of lists containing dicts
    outfilename : str
        user supplied file name
    """
    
    file_name = f"edge_extensions_{datetime.now().strftime('%Y-%m-%d')}.csv"

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