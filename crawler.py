import urllib.request as urllib2
import csv
try:
    from pip._internal import main
except:
    print("pip is not installed. Please Install pip then try again....")
    exit()

try:
    from bs4 import BeautifulSoup
except:
    main(['install', "beautifulsoup4"])


def p_red(skk): print("\033[91m {}\033[00m" .format(skk))
def p_green(skk): print("\033[92m {}\033[00m" .format(skk))
def p_yellow(skk): print("\033[93m {}\033[00m" .format(skk))
def p_purple(skk): print("\033[95m {}\033[00m" .format(skk))
def p_cyan(skk): print("\033[96m {}\033[00m" .format(skk))


url_dict = {}
def main_logic(page,count,main_url):
    p_green("Crawling Started......🕷")
    doc = page.read()
    soup = BeautifulSoup(doc,"html.parser")
    try:
        title = soup.title.string
    except:
        title = "No Title"
    url_dict[main_url] = {'URL':main_url,'TITLE':title}
    for link in soup.find_all('a'):
        li = link.get('href')
        li = str(li)
        if li.startswith(main_url) and li not in url_dict :
            get_all_links(li,main_url,count-1)

    #print(url_dict)
    writeCSV(url_dict)

def writeCSV(dict):
    with open('crawler_data.csv', 'w') as csvfile:
        fieldnames = ['URL', 'TITLE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([dict[key] for key in dict ])
    csvfile.close()

    p_green("Crawling Successfull... 'crawler_data.csv' generated as log...")


def pageDetails(url,main_url):
    try:
        page = urllib2.urlopen(url)
    except:
        return None
    doc = page.read()
    soup = BeautifulSoup(doc,"html.parser")
    try:
        title = soup.title.string
    except:
        title = "No Title"
    uni_set=set()
    for link in soup.find_all('a'):
        link = str(link.get('href'))
        if url.startswith(main_url) and link not in url_dict:
            uni_set.add(link)
    return uni_set,title


def get_all_links(url,main_url,count=None):
    if not count or count>=len(url_dict):
        if url.startswith(main_url) and url not in url_dict:
            print(url)
            try:
                page_links,title = pageDetails(url,main_url)
                url_dict[url] = {'URL':url,'TITLE':title}
                for link in page_links:
                    get_all_links(link, main_url,count)
            except:
                pass
        else:
            pass
    else:
        return

def start():
    p_purple("Welcome to Crawler .....")
    p_purple("Please enter inputs asked .....")
    one()

def one():
    p_purple("Enter The Url to Crawl ...")
    try:
        main_url = str(input())
        two(main_url)
    except:
        one()

def two(main_url):
    try:
        page = urllib2.urlopen(main_url)
        p_yellow("Your entered url is %s" % (main_url))
        three(page,main_url)
    except:
        p_red("Please Enter an valid input")
        one()

def three(page,main_url):
    try:
        p_purple("Enter Number of links to crawl or for indefinite crawl press only enter ...")
        count=str(input()).strip()
        if count == "":
            count = None
        else:
            count = int(count)
        main_logic(page,count,main_url)
    except:
        p_red("Please Enter an valid input")
        three(page)

start()



