# Web Scraper

Python web scraper to retrieve data from intranet pages requiring SSO authentication.

## Setup

### Step 1: Install ChromeDriver

This scraper requires ChromeDriver to work with Selenium. Download the version of ChromeDriver that matches your version of Chrome from [here](https://googlechromelabs.github.io/chrome-for-testing/#stable).

- Once downloaded, make sure the `chromedriver` executable is available in the location specified in the `main.py` file. With the current configuration it should be placed in the root directory of the project. (`CHROME_DRIVER_PATH = './chromedriver.exe'`)
- Update the path in the script if necessary.

### Step 2: Install Dependencies

Install the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

This will install the following:
- `selenium` for web automation.
- `beautifulsoup4` for HTML parsing.
- `pandas` for handling and exporting the scraped data.

### Step 3: Run the Script

1. Open a terminal and navigate to the project directory.
2. Run the following command to start the scraper:

```bash
python ./main.py
```

### Step 4: Usage

1. **Enter Credentials**: When prompted, enter your **username** and **password**. These will be used to authenticate via the SSO.
   
2. **Select Pages to Scrape**: You will be presented with a list of available pages to scrape. You can either:
   - Enter `all` to scrape all pages.
   - Or, select specific pages by entering their respective numbers separated by commas (e.g., `1,2`).

3. **Scraping in Progress**: The script will use Selenium to navigate to the appropriate page, extract the data, and store it in CSV format in the `/scraped_data` directory.

4. **Close the Browser**: Once the scraping is completed, the browser will automatically close.

### Customizing the Scraper

You can modify or add new scraping functions in the `scraper.py` module to target new pages or adapt the scraping logic for different types of data.