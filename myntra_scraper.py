#! /usr/bin/python3
# myntra_scraper by Architrixs, 15 May 2021
import requests
import bs4
import json
import time
import concurrent.futures
import sys

def help():
    print("""Usage :-
    $ ./myntra_scraper.py [Arg1: inputFileName.txt] [Arg2: outputFileName.json]

    $ ./myntra_scraper.py --help or -h		# Show usage

    Example: $ ./myntra_scraper.py test_out.txt test_scraped_data.json
             \n""")
    exit()

if len(sys.argv)==1 or sys.argv[1]== '--help' or sys.argv[1]=='-h' or len(sys.argv)<3:
    help()

if len(sys.argv) == 3:
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[-1]

else:
    help()

#print(links)
MAX_THREADS = 30
final_data ={}
def get_data(url):
    print(url)
    res = requests.get('https://www.myntra.com/'+url,headers={'User-Agent': 'Mozilla/5.0'})
    try:
        res.raise_for_status()
    except Exception as exc:
        print("There was a problem: %s" % (exc))
    
    print('making soup...')
    soup_res = bs4.BeautifulSoup(res.text,'html.parser')

    scripts = soup_res.find_all('script')
    data = json.loads(scripts[11].string[15:])
    id  = data["pdpData"]['id']
    brand = data["pdpData"]['brand']['name']
    product = data["pdpData"]['analytics']['articleType']
    gender  = data["pdpData"]['analytics']["gender"]
    description = data["pdpData"]["name"]
    mrp  = data["pdpData"]["price"]["mrp"]
    price = data["pdpData"]["price"]["discounted"]
    img1 = data["pdpData"]["media"]["albums"][0]["images"][0]["imageURL"]
    img2 = data["pdpData"]["media"]["albums"][0]["images"][1]["imageURL"]

    sizes = [sizes["label"] for sizes in data["pdpData"]["sizes"]]

    '''print(id, brand, product, description, mrp, price, gender)
    print(img1)
    print(img2)
    print(sizes)
    '''

    newdata={}
    newdata[id] = {'brand':brand, 'product':product, 'description': description, 'gender': gender, 'mrp':mrp, 'price':price,
    'sizes':sizes, 'product_link':'https://www.myntra.com/'+url, 'img1': img1, 'img2':img2}

    final_data.update(newdata)
    
    print('collecting info...')        
    time.sleep(0.25)

def get_url(links):
    #for url in links:
    #    get_data(url)
    threads = min(MAX_THREADS, len(links))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_data, links)

def main():
    with open(input_file_name,'r' ,encoding="utf-8") as f:
        product_links = f.readlines()
    links=[l.strip() for l in product_links]

    t0 = time.time()
    get_url(links)
    t1 = time.time()

    print(f"{t1-t0} seconds to download {len(links)} product links.")
    with open(output_file_name,'w' ,encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)
    print("File saved", output_file_name)

if __name__=="__main__": 
    main()
