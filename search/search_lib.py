"""
Travis Robinson
Oregon State
Computer Science
travisrobinson2006@gmail.com
robitrav@oregonstate.edu
"""

"""
search functions for Victoria. Includes functions to search in browser using desired search engines, as well as ability to search in computers drives
"""

#import modules
import webbrowser
import os
#import glob
import string
from ctypes import windll

#list of available engines for reference by other functions, as well as keying each engine name to the appropriate search url
#note--rename browser to engine
available_browsers = ['google','bing','yahoo','ask','aol']
browser_search_string = ["https://www.google.com/search?q=",
    "http://www.bing.com/search?q=",
    "https://search.yahoo.com/search?q=",
    "http://www.ask.com/web?q=",
    "http://search.aol.com/aol/search?q="]

"""
Description: open new tab in browser, perform search using desired engine
Input: engine and user query
Output: opens new tab in browser using url to engines query as well as user query
Note: need to strip off user command, just desired query (ie instead of searching for: search google for red rocket, should search for red rocket)
"""
def search_web(engine,query):
    url = ""#initialize url
    engine = engine.lower()
    if engine in available_browsers:#grab appropriate search url for desired engine
        url = url + browser_search_string[available_browsers.index(engine)]
    else:#default to google if no user engine specified
        url = url + browser_search_string[available_browsers.index('google')]
    for i in query:#each engines search url uses '+' between search terms--add those in here
        url = url + i
        if query.index(i) < len(query)-1:
            url = url + '+'
    webbrowser.open_new_tab(url)

"""
Description: searches a given directory of computer for name (a user provided file)
Input: directory to search and name of file to search for
Output: path names of all instances of file found
Note: need to improve method of parsing out the name of the file the user is searching for--as is may search for phrases instead of just the file name
"""
def search_directory(directory,name):
    name = name.lower()  # Convert up front in case it's pass mixed case
    for root, dirs, files in os.walk(directory,topdown=True):
        for i in files + dirs:
            if os.path.splitext(i)[0].lower() == name:
                yield os.path.join(root, i)

"""
Description: retrieves all drives on computer, uses search directory to search those drives
Input: name of file we want to fine
Output: path to all files of name in all drives
"""
def search_computer(name):
    drives = []
    result = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter+":\\")
        bitmask >>= 1
    for i in drives:
        pre_result = list(search_directory(i,name))
        result = result+pre_result
    if len(result) == 0:
        result.append("fileNotFound")
    return result
