from bs4 import BeautifulSoup
from utils import save_to_csv, get_text_from_table, get_id_from_table, get_link_from_table, get_text_from_section, get_id_from_section
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
        company_name = get_text_from_table(row, 'views-field-title')
        company_id = get_id_from_table(row, 'views-field-title')
        company_link = get_link_from_table(row, 'views-field-title')

        # Visit company detail page and scrape more details
        if company_link:
            print(f'Scraping the company : {company_name}')

            driver.get(f'https://gi-intranet.insa-lyon.fr{company_link}')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Adresse
            address = get_text_from_section(soup, 'field-name-field-adresse')

            # Code postal
            postal_code = get_text_from_section(soup, 'field-name-field-code-postal')
            
            # Ville
            city = get_text_from_section(soup, 'field-name-field-ville')

            # Cedex 
            cedex = get_text_from_section(soup, 'field-name-field-cedex')

            # Pays
            country = get_text_from_section(soup, 'field-name-field-pays')

            # Courriel
            email = get_text_from_section(soup, 'field-name-field-courriel')

            # Site Web
            website = get_text_from_section(soup, 'field-name-field-site-web')

            # Nom du dirigeant
            leader = get_text_from_section(soup, 'field-name-field-nom-du-dirigeant')

            # Secteur d'activité
            activity = get_text_from_section(soup, 'field-name-field-secteur-d-activite2')

            # Code NAF
            naf_code = get_text_from_section(soup, 'field-name-field-code-naf')

            company_details = [address, postal_code, city, cedex, country, email, website, leader, activity, naf_code]
        else:
            company_details = [None] * 10  # If no link, leave other details empty

        # Combine data from the listing page with details page data
        data_list.append([company_id, company_name] + company_details)

    return data_list, ['ID', 'Société', 'Adresse', 'Code Postal', 'Ville', 'Cedex', 'Pays', 'Courriel', 'Site web', 'Nom Dirigeant', 'Secteur Activité', 'Code NAF']


# Function to scrape sites
def scrape_sites(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    data_list = []

    # Locate and scrape the data based on the columns defined in url_info
    rows = soup.select('table.views-table tbody tr')
    
    print(f'Scraping {len(rows)} sites...')

    for row in rows:
        # Site
        site_name = get_text_from_table(row, 'views-field-title')
        site_id = get_id_from_table(row, 'views-field-title')
        site_link = get_link_from_table(row, 'views-field-title')

        # Visit site detail page and scrape more details
        if site_link:
            print(f'Scraping the site : {site_name}')

            driver.get(f'https://gi-intranet.insa-lyon.fr{site_link}')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Adresse
            address = get_text_from_section(soup, 'field-name-field-adresse')

            # Code postal
            postal_code = get_text_from_section(soup, 'field-name-field-code-postal')
            
            # Ville
            city = get_text_from_section(soup, 'field-name-field-ville')

            # Pays
            country = get_text_from_section(soup, 'field-name-field-pays')

            # Téléphone
            phone = get_text_from_section(soup, 'field-name-field-telephone')

            # Courriel
            email = get_text_from_section(soup, 'field-name-field-courriel')

            # Site Web
            website = get_text_from_section(soup, 'field-name-field-site-web')

            # Société
            company = get_text_from_section(soup, 'field-name-field-societe')
            company_id = get_id_from_section(soup, 'field-name-field-societe')

            # Secteur d'activité
            activity = get_text_from_section(soup, 'field-name-field-secteur-d-activite2')

            # Code NAF
            date_creation = get_text_from_section(soup, 'field-name-field-date-de-creation')

            site_details = [address, postal_code, city, country, phone, email, website, company_id, company, activity, date_creation]
        else:
            site_details = [None] * 11  # If no link, leave other details empty


        # Store the data
        data_list.append([site_id, site_name] + site_details)

    return data_list, ['ID', 'Site', 'Adresse', 'Code Postal', 'Ville', 'Pays', 'Téléphone', 'Courriel', 'Site Web', 'ID Société', 'Société', 'Secteur Activité', 'Date Création']

# Function to scrape companies
def scrape_contacts(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    data_list = []

    # Locate and scrape the data based on the columns defined in url_info
    rows = soup.select('table.views-table tbody tr')
    
    print(f'Scraping {len(rows)} contacts...')

    for row in rows:
        # Contact
        contact_id = get_id_from_table(row, 'views-field-title')
        contact_link = get_link_from_table(row, 'views-field-title')

        # Visit site contact page and scrape more details
        if contact_link:
            print(f'Scraping the contact : {contact_link}')

            driver.get(f'https://gi-intranet.insa-lyon.fr{contact_link}')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Titre
            title = get_text_from_section(soup, 'field-name-field-titre')

            # Nom
            lastname = get_text_from_section(soup, 'field-name-field-nom')
            
            # Prénom
            firstime = get_text_from_section(soup, 'field-name-field-prenom')

            # Site
            site = get_text_from_section(soup, 'field-name-field-entreprise')
            site_id = get_id_from_section(soup, 'field-name-field-entreprise')

            # Service
            service = get_text_from_section(soup, 'field-name-field-service')

            # Fonctions
            functions = get_text_from_section(soup, 'field-name-field-fonctions')

            # Courriel
            email = get_text_from_section(soup, 'field-name-field-courriel')


            contact_details = [lastname, firstime, title, site_id, site, service, functions, email]
        else:
            contact_details = [None] * 8  # If no link, leave other details empty


        # Store the data
        data_list.append([contact_id] + contact_details)

    return data_list, ['ID', 'Nom', 'Prénom', 'Titre', 'ID Site', 'Site', 'Service', 'Fonctions', 'Courriel']

# General function to scrape all pages, with scrape_page passed as an argument
def scrape_all_pages(driver, page_info):
    page_name = page_info['name']
    base_url = page_info['url']
    scrape_function = page_info['scrape_function']

    url = base_url
    data_list = []
    while True:

        if not navigate_with_session_handling(driver, url) or driver.current_url != url:
            print(f"An error occured while accessing to the {page_name} page...")
            return
        
        # Get the "Next" button if exists
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        next_button = soup.select_one('li.pager-next a')

        # Scrape the current page using the passed scrape_page method
        page_data_list, columns = scrape_function(driver)
        data_list += page_data_list

        # No "Next" button means this is the last page
        if next_button is None:
            print("Reached the last page.")
            break

        if next_button:
            next_page_url = next_button['href']
            url = base_url + next_page_url

    save_to_csv(f"scraped_{page_name.lower()}.csv", columns, data_list)
    