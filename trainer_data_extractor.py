import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

links_visited = []

def extract_website_text(url, base_url, link = "root"):
    # Get the HTML content of the website page
    response = requests.get(url)
    html = response.content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all links on the website page
    links = soup.find_all('a')

    # Extract text from the website page
    website_text = soup.get_text()

    if website_text == "404 Not found - SingleStore Documentation":
        return

    with open(f'./data/{link}.txt', 'a') as file:
        file.write(website_text)

    # Extract text from all sub-links with the same base URL
    for link in links:
        file_name = link.get('href')
        if file_name:
            link_url = urljoin(base_url, file_name)
            link_domain = urlparse(link_url).netloc
            if link_url in links_visited:
                break
            if link_domain == urlparse(base_url).netloc and link_url.lower() not in links_visited:
                links_visited.append(link_url.lower())
                extract_website_text(link_url, base_url, re.sub(r'[^a-zA-Z0-9]+', '_', link_url))

extract_website_text("https://docs.singlestore.com", "https://docs.singlestore.com")
