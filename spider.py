import requests
import re
import urllib.parse as urlparse

target_links = []
def menu():
    print("1. Look for hidden site pages")
    print("2. Scrape Site for all href")
    print("3. Quit")
    return input("Choose an Option:")

def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', 	response.content.decode(errors="ignore"))

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if '#' in link:
            link = link.split('#')[0]

        if url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)

def check(status):
    if status == 404:
        return None
    else:
        return status

def search(url, filename):
    with open(filename, 'r') as file:
            line = file.readline()
            while line:
                # Perform function on line
                url = url + line.strip()
                response = requests.get(url)
                stat = check(response.status_code)
                if stat:
                    print(url + " ===== " + str(stat))
                else:
                    continue
                # Read the next line
                line = file.readline()

while True:
    choice = menu()
    url = input("Enter url for target site: ")
    if choice == '1':
        print("Have a wordlist in the same directory as this file.")
        wl = input("Enter wordlist name: ")
        search(url, wl)
    elif choice == '2':
        print("Recursively finding all referenced sites...")
        crawl(url)
    elif choice == '3':
        print("Closing...")
        quit()
    else:
        print("Incorrect option selected, try again.")
      
      
