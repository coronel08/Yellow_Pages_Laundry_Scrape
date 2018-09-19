# https://codereview.stackexchange.com/questions/173105/e-mail-crawler-for-yellowpages
import requests
import urllib
from lxml import html

# creates csv file
filename = 'Yellow_Pages.csv'
f = open(filename, 'w')
headers = 'Name, Address, City ,Postal \n'
f.write(headers)

#builds URL
URL = "https://www.yellowpages.com"
LOWER_LIMIT = 1
UPPER_LIMIT = 2
def build_url(item, location, page):
    params = urllib.parse.urlencode({
        'search_terms': item,
        'geo_location_terms': location,
        'page': page
    })
    return '{}/search?{}'.format(URL, params)

# function to write scraped info into csv file
def write_csv(item2Write):
    f.write(item2Write)

#webscraper that crawls and extracts info
def scrape():
    for page in range(LOWER_LIMIT, UPPER_LIMIT):
        url = build_url('Laundry', 'Los Angeles CA', page)
        html_ = requests.get(url).text
        for item in html.fromstring(html_).cssselect('div.info h2.n a:not([itemprop="name"]).business-name'):
# gets the business name
            for name in html.fromstring(requests.get(URL + item.attrib['href']).text).cssselect('div.sales-info'):
                location = str(name.xpath('//*[@id="main-header"]/article/div/h1/text()'))
                print(location[2:-2])
                f.write(location [2:-2] + ",")
# formats the address properly
            for address in html.fromstring(requests.get(URL + item.attrib['href']).text).cssselect('p.address'):
                street = str(address.xpath('//*[@id="main-header"]/article/section[2]/div[1]/p[1]/span[1]/text()'))
                city = str(address.xpath('//*[@id="main-header"]/article/section[2]/div[1]/p[1]/span[2]/text()'))
                postal = str(address.xpath('//*[@id="main-header"]/article/section[2]/div[1]/p[1]/span[4]/text()'))
                f.write(street [2:-2])
                f.write(city [2:-2])
                f.write(postal[2:-2] + "\n")
    f.close()

if __name__ == '__main__':
    scrape()
