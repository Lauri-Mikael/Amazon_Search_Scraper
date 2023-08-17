import requests
from bs4 import BeautifulSoup

# A python script which can scrape a set number of product links for an Amazon search term. For example, if "dog toys" was searched, it'd copy the link for the first 100 products and save those links inside a text file.

lists = []

def get_product_links(search_term, num_links, page_number):
    base_url = 'https://www.amazon.com'
    search_url = f'{base_url}/s?k={search_term.replace(" ", "+")}&page={page_number}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_links = []
    while len(product_links) < num_links:
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for result in results:
            link_tag = result.find('a', {'class': 'a-link-normal'})
            if link_tag:
                product_links.append(base_url + link_tag['href'])
                if len(product_links) == num_links:
                    break

        next_page_link = soup.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-disabled'})
        if not next_page_link:
            res = soup.find('a', {'class': 's-pagination-item s-pagination-next'})

            next_page_link = soup.find('a', {'class': 's-pagination-item s-pagination-next'})
            next_page_url = ''
            if next_page_link:
                next_page_url = search_url + next_page_link.get('href', '')
            else:
                # Handle the case when the next page link is not found
                break
                
            response = requests.get(next_page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            break

    return product_links

# Type your search here
search_term = 'laptop' # Search Name
num_links = 100  # Number of links you want to get

# File write
i = 1

while(i <=num_links / 16 + 1):

    links = get_product_links(search_term, num_links, i)

    for link in links:
        lists.append(link)
    i = i + 1

j = 0
for listtag in lists:
    with open(search_term+"_amazon_links.txt", "a") as file:
        file.write(listtag + "\n")
        j = j + 1
        if (j == num_links):
            break
        