#! /usr/bin/python3
# myntra_scraper by Architrixs, 15 May 2021

import bs4
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys

def help():
    print("""Usage :-
    $ ./myntra_link_scraper.py [Arg1: n, Number of pages to look upto] [Arg2: outputFileName.txt]

    $ ./myntra_link_scraper.py --help or -h		# Show usage

    Example: $ ./myntra_link_scraper.py 20 output_links.txt
             \n""")
    exit()

#example_url = 'https://www.myntra.com/men-tshirts?p=1&rows=100'
product_links = set()
if len(sys.argv)==1 or sys.argv[1]== '--help' or sys.argv[1]=='-h' or len(sys.argv)<3:
    help()

if len(sys.argv) == 3:
    page_upto = int(sys.argv[1])
    output_file_name = sys.argv[-1]

else:
    help()

options = Options()
options.headless = True
# Create your driver
driver = webdriver.Firefox(options = options)

def get_product_links(url):
    print(url)
    try:
        print('getting page')

        driver.get(url)
        elem = driver.find_element_by_class_name('results-base')
        code = elem.get_attribute('innerHTML')
        
        
    except Exception as e:
        print(e)
        exit()
    print("making soup...")
    soup_res = bs4.BeautifulSoup(code, 'html.parser')
    #print(soup_res)
    
    data = soup_res.find_all('li',{'class':'product-base'})
    for d in data:
        link = d.find('a')['href']
        product_links.add(link)

def get_page_links(page_links):
    for url in page_links:
        get_product_links(url)
    
def main():
    page_links=['https://www.myntra.com/men-tshirts?p='+str(i)+'&rows=100' for i in range(1,page_upto+1)]

    t0 = time.time()
    print("starting driver")
    get_page_links(page_links)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(page_links)} page links.")
    print("Closing driver, please wait...")
    driver.quit()
    print("Links collected:", len(product_links))
    with open(output_file_name,'a' ,encoding="utf-8") as f:
        for link in product_links:
            f.write(link+'\n')
    print("File saved", output_file_name)

if __name__=="__main__": 
    main()