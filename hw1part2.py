import io, time, json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def retrieve_html(url):
    """
    Return the raw HTML at the specified URL.

    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    
    response = requests.get(url)
    return (response.status_code, response.text)

def location_search_params(api_key, location, **kwargs):
    """
    Construct url, headers and url_params. Reference API docs (link above) to use the arguments
    """
    url = 'https://api.yelp.com/v3/businesses/search'
    
    headers = {'Authorization' : 'Bearer ' + api_key}
    
    location_param = {"location" : location.strip()}
    
    url_params = kwargs
    url_params.update(location_param)

    return url, headers, url_params


def paginated_restaurant_search_requests(api_key, location, total):
    """
    Returns a list of tuples (url, headers, url_params) for paginated search of all restaurants
    Args:
        api_key (string): Your Yelp API Key for Authentication
        location (string): Business Location
        total (int): Total number of items to be fetched
    Returns:
        results (list): list of tuple (url, headers, url_params)
    """
    res = []
    
    numResPerPage = 10
    totalIter = total // numResPerPage
    for i in range(totalIter):
        res.append(location_search_params(api_key, location, limit = numResPerPage, offset=i * numResPerPage, categories = "restaurants"))
    
    # Remainder
    res.append(location_search_params(api_key, location, limit = total - numResPerPage * totalIter, offset=numResPerPage * totalIter, categories = "restaurants"))
    
    return res

def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    return [x['url'] for x in data]


def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.
    
    Args:
        html (string): String of HTML corresponding to a Yelp restaurant

    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """
    soup = BeautifulSoup(html,'html.parser')
    url_next = soup.find('link',rel='next')
    if url_next:
        url_next = url_next.get('href')
    else:
        url_next = None

    reviews = soup.find_all('div', itemprop="review")
    reviews_list = []

    authors = soup.find_all('meta', itemprop="author")
    ratings = soup.find_all('meta', itemprop="ratingValue")
    dates = soup.find_all('meta', itemprop="datePublished")
    descriptions = soup.find_all('p', itemprop="description")
    i = 0
    
    for item in reviews:
        reviews_list.append({
                'author': authors[i].attrs['content'],
                'rating': ratings[i+1].attrs['content'],
                'date': dates[i].attrs['content'],
                'description': descriptions[i].get_text()
        })
        i += 1
    return reviews_list, url_next

# 4% credits
def extract_reviews(url, html_fetcher):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.
        html_fetcher (function): A function that takes url and returns html status code and content
        

    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """
    reviews = []
    code, html = html_fetcher(url)
    reviews_list, url_next = parse_page(html)
    
    def get_each_rev(reviews_list):
        for rev in reviews_list:
            reviews.append(rev)
    
    get_each_rev(reviews_list)

    
    while (url_next != None):
        code, html = html_fetcher(url_next)
        reviews_list, url_next = parse_page(html)
        get_each_rev(reviews_list)


    return reviews