from navigator import connect_to_sso
from scraper import scrape_all_pages, scrape_sites, scrape_companies, scrape_contacts
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import getpass

PAGES = [
    {
        'name': 'Companies',
        'url': 'https://gi-intranet.insa-lyon.fr/v4/industrie/societes/liste',
        'scrape_function': scrape_companies,
    },
    {
        'name': 'Sites',
        'url': 'https://gi-intranet.insa-lyon.fr/v4/industrie/sites/liste',
        'scrape_function': scrape_sites
    },
    {
        'name': 'Contacts',
        'url': 'https://gi-intranet.insa-lyon.fr/v4/industrie/contacts/liste',
        'scrape_function': scrape_contacts
    },

]

# Specify the path to chromedriver
CHROME_DRIVER_PATH = './chromedriver.exe'

# Specity the URL of the website SSO
SSO_URL = 'https://login.insa-lyon.fr/cas/login'

# Prompt user for username and password
username = input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")  # Password is hidden


# Ask user to scrape all URLs or select specific ones
print("Available pages for scraping:")
for i, page_info in enumerate(PAGES, 1):
    print(f"{i}. {page_info['name']}")

option = input("Do you want to scrape all URLs or choose specific ones? (Enter 'all' or the ID of the pages you want to scrape separated by comma): ").strip().lower()

# Create a Service object for ChromeDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Connect to SSO
connect_to_sso(driver, SSO_URL, username, password)

if option == 'all':
    # Scrape all URLs
    for page_info in PAGES:
        print(f"Scraping: {page_info['name']}")
        scrape_all_pages(driver, page_info)
else:
    pages = option.split(',')
    for index in pages:
        try:
            idx = int(index) - 1
            page_info = PAGES[idx]
            print(f"Scraping: {page_info['name']}")
            scrape_all_pages(driver, page_info)
        except (ValueError, IndexError):
            print(f"Invalid selection: {index}")

# Close the browser after scraping
driver.quit()
