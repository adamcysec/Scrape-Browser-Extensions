# Scrape-Browser-Extensions

This repo contains python scrips for scraping all visible browser extension for Chrome and Edge.

The scripts output a CSV file containing the extension id and the extension name with the following fields:
`id`, `name`

You can view the CSV data zipped in directory [/extension data/](https://github.com/adamcysec/Scrape-Browser-Extensions/tree/main/extension%20data)

## Why scrape browser extensions?

### Malicious Extensions

Malicious browser extensions typically steal user data or visit advertisment related links in the background. 

  - I suggest reading this article from brave.com about malicious broswer extensions - [brave.com/learn/browser-extension-safety/#is-it-safe-to-use-browser-extensions](https://brave.com/learn/browser-extension-safety/#is-it-safe-to-use-browser-extensions)

By the time security news outlets have reported on these malicious extensions, the extensions have already been removed from the extension store. However the extension is not removed from the end user's browser until the user uninstalls it (that's if they ever do).

There are some repositories that aim to compile a list of malicious browser extension ids in order to scan for malicious extensions in a workplace environment. However, the work compiling the list is very manual and involves googling/tracking news articles.

### My idea - scrape extenions

If we take a snapshot of every extension on the Chrome/Edge store, then we would know what extensions are allowed on the store. We could then compare that list to a list of extensions installed in the workplace environment and might discover users with extensions no longer on the broswer store. 

There are several reasons an extension is removed from the store:

  1. Extensions that come [preinstalled](https://www.jamieweb.net/info/chrome-extension-ids/) in broswers were removed from the store.
  2. The developer decided to remove their extension from the store.
  3. Chrome/Edge removed the extension from their store (probably for good reasons).

## visible browser extension?



## The Tools

### `scrape-chromeWebstore.py`

This script scrapes extension data by enumerating the Chrome [sitemaps](https://chrome.google.com/webstore/sitemap).

**Dependencies**
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
  - `pip install beautifulsoup4`
- [lxml](https://pypi.org/project/lxml/)
  - `pip install lxml`

**Example**

`py scrape_chromeWebstore.py`

- the CSV is saved in the current working directory

**Output**

```
starting work on 16 cores
--- 17.575310230255127 seconds ---
file saved: edge_extensions.csv
```

### `scrape-EdgeAddons.py`

This script scrapes extension data by enumerating the page numbers for each category in Microsoft's store [api](https://microsoftedge.microsoft.com/addons/getfilteredextensions/Productivity?noItems=24&pgNo=1&IncludeExtensionDetailsFields=true).

**Example**

`py scrape_EdgeAddons.py`

- the CSV is saved in the current working directory

**Output**

```
starting work on 16 cores
--- 17.575310230255127 seconds ---
file saved: edge_extensions.csv
```
