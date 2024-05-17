import requests
from bs4 import BeautifulSoup
import dns.resolver
import whois

# Function to fetch and parse webpage content
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve {url}")
        return None

# Function to extract meta tags
def extract_meta_tags(soup):
    meta_tags = {}
    for tag in soup.find_all("meta"):
        name = tag.get("name", "").lower()
        content = tag.get("content", "")
        if name:
            meta_tags[name] = content
    return meta_tags

# Function to extract headers
def extract_headers(soup):
    headers = {}
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        headers[header.name] = headers.get(header.name, []) + [header.text.strip()]
    return headers

# Function to extract links
def extract_links(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        text = link.text.strip()
        links.append({'text': text, 'url': href})
    return links

# Function to perform DNS lookup
def perform_dns_lookup(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [ip.address for ip in result]
    except Exception as e:
        print(f"DNS lookup failed: {e}")
        return None

# Function to get WHOIS information
def get_whois_info(domain):
    try:
        whois_info = whois.whois(domain)
        return whois_info
    except Exception as e:
        print(f"WHOIS lookup failed: {e}")
        return None

# Main function to gather information
def gather_information(url):
    print(f"Gathering information for {url}...\n")
    soup = fetch_webpage(url)
    if soup:
        meta_tags = extract_meta_tags(soup)
        headers = extract_headers(soup)
        links = extract_links(soup)

        print("Meta Tags:")
        for name, content in meta_tags.items():
            print(f"{name}: {content}")
        print("\nHeaders:")
        for header, texts in headers.items():
            for text in texts:
                print(f"{header}: {text}")
        print("\nLinks:")
        for link in links:
            print(f"Text: {link['text']}, URL: {link['url']}")

        domain = url.split("//")[-1].split("/")[0]
        dns_info = perform_dns_lookup(domain)
        if dns_info:
            print("\nDNS Information:")
            for ip in dns_info:
                print(ip)
        
        whois_info = get_whois_info(domain)
        if whois_info:
            print("\nWHOIS Information:")
            for key, value in whois_info.items():
                print(f"{key}: {value}")

if __name__ == "__main__":
    target_url = "https://zubairfeeds.com"
    gather_information(target_url)