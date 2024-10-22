from bs4 import BeautifulSoup
from utils import save_to_csv, get_text_from_field, get_id_from_field, get_link_from_field
from navigator import navigate_with_session_handling

# Function to scrape companies
def scrape_companies(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    data_list = []

    # Locate and scrape the data based on the columns defined in url_info
    rows = soup.select('table.views-table tbody tr')
    
    print(f'Scraping {len(rows)} companies...')

    for row in rows:
        # Société
        COMPANY_FIELD = 'views-field-title';
        company_name = get_text_from_field(row, COMPANY_FIELD)
        company_id = get_id_from_field(row, COMPANY_FIELD)
        company_link = get_link_from_field(row, COMPANY_FIELD)

        # Ville
        CITY_FIELD = 'views-field-field-ville';
        city = get_text_from_field(row, CITY_FIELD)

        # Pays
        COUNTRY_FIELD = 'views-field-field-pays';
        country = get_text_from_field(row, COUNTRY_FIELD)

        # Site Web
        WEBSITE_FIELD = 'views-field-field-site-web';
        website = get_link_from_field(row, WEBSITE_FIELD)

        # if company_link:
        #     driver.get(f'https://gi-intranet.insa-lyon.fr{company_link}')
        #     time.sleep(3)  # Adjust the time to wait for the page to load
        #     company_html = driver.page_source
        #     company_soup = BeautifulSoup(company_html, 'html.parser')
        #     # Scrape additional company data from the linked page (if needed)
        #     adress_tag = company_soup.select_one('section.field-name-field-adresse div.field-item')
        #     if adress_tag:
        #         adress = adress_tag.get_text().strip()

        # Store the data
        data_list.append([company_id, company_name, city, country, website])


    return data_list, ['ID', 'Société', 'Ville', 'Pays', 'Site Web']

# Function to scrape sites
def scrape_sites(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    data_list = []

    # Locate and scrape the data based on the columns defined in url_info
    rows = soup.select('table.views-table tbody tr')
    
    print(f'Scraping {len(rows)} sites...')

    for row in rows:
        # Nom du site
        SITE_FIELD = 'views-field-title';
        site_name = get_text_from_field(row, SITE_FIELD)
        site_id = get_id_from_field(row, SITE_FIELD)
        site_link = get_link_from_field(row, SITE_FIELD)

        # Ville
        CITY_FIELD = 'views-field-field-ville';
        city = get_text_from_field(row, CITY_FIELD)

        # Pays
        COUNTRY_FIELD = 'views-field-field-pays';
        country = get_text_from_field(row, COUNTRY_FIELD)

        # Société
        COMPANY_FIELD = 'views-field-field-societe';
        company_name = get_text_from_field(row, COMPANY_FIELD)
        company_id = get_id_from_field(row, COMPANY_FIELD)

        # Store the data
        data_list.append([site_id, site_name, city, country, company_id, company_name])

    return data_list, ['ID', 'Site', 'Ville', 'Pays', 'ID Société', 'Société']

# Function to scrape companies
def scrape_contacts(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    data_list = []

    # Locate and scrape the data based on the columns defined in url_info
    rows = soup.select('table.views-table tbody tr')
    
    print(f'Scraping {len(rows)} contacts...')

    for row in rows:
        # Nom et prénom
        CONTACT_FIELD = 'views-field-title';
        contact_name = get_text_from_field(row, CONTACT_FIELD)
        contact_id = get_id_from_field(row, CONTACT_FIELD)
        contact_link = get_link_from_field(row, CONTACT_FIELD)

        # Site
        SITE_FIELD = 'views-field-field-entreprise';
        site_name = get_text_from_field(row, SITE_FIELD)
        site_id = get_id_from_field(row, SITE_FIELD)

        # Service
        SERVICE_FIELD = 'views-field-field-service';
        service = get_text_from_field(row, SERVICE_FIELD)

        # Fonctions
        FUNCTIONS_FIELD = 'views-field-field-fonctions';
        functions = get_text_from_field(row, FUNCTIONS_FIELD)

        # Courriel
        EMAIL_FIELD = 'views-field-field-courriel';
        email = get_text_from_field(row, EMAIL_FIELD)

        # Store the data
        data_list.append([contact_id, contact_name, site_id, site_name, service, functions, email])

    return data_list, ['ID', 'Contact', 'ID Site', 'Site', 'Service', 'Fonctions', 'Courriel']

# General function to scrape all pages, with scrape_page passed as an argument
def scrape_all_pages(driver, page_info):
    page_name = page_info['name']
    url = page_info['url']
    scrape_function = page_info['scrape_function']

    data_list = []

    if not navigate_with_session_handling(driver, url) or driver.current_url != url:
        print(f"An error occured while accessing to the {page_name} page...")
        return

    while True:
        # Scrape the current page using the passed scrape_page method
        page_data_list, columns = scrape_function(driver)
        data_list += page_data_list

        # Check if we're on the last page
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        last_page_button = soup.select_one('li.pager-last')
        if last_page_button is None:  # No "dernier" button means this is the last page
            print("Reached the last page.")
            break

        # Find the "suivant" button to go to the next page
        next_button = soup.select_one('li.pager-next a')
        if next_button:
           # Navigate to the next page using the href attribute
            next_page_url = next_button['href']
            driver.get(url + next_page_url)
        else:
            break  # No next button, stop the loop

    save_to_csv(f"scraped_{page_name.lower()}.csv", columns, data_list)
    