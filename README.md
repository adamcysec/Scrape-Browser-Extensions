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

There are some repositories that aim to compile a list of malicious browser extension ids in order to scan for malicious extensions in a workplace environment. However, the work compiling the list is very manual and invovles googling/tracking news articles.

### My idea - scrape extenions

If we take a snapshot of every extension on the Chrome/Edge store, then we would know what extensions are allowed on the store. We could then compare that list to a list of extensions installed in the workplace environment and might discover users with extensions no longer on the broswer store. 
