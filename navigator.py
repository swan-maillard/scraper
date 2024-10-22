from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def connect_to_sso(driver, sso_url, username, password):
    driver.get(sso_url)

    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password') 

    username_input.send_keys(username) 
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)

# Function to handle the active session page
def handle_active_sessions(driver):
    # Check if the session selection page is present
    try:
        # Wait for the session page to appear
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "edit-session-reference")))
        
        # Find all radio buttons for session selection
        session_options = driver.find_elements(By.CSS_SELECTOR, 'input[name="session_reference"]')
        
        if session_options:
            # Select the first inactive session
            for session_option in session_options:
                label = driver.find_element(By.CSS_SELECTOR, f'label[for="{session_option.get_attribute("id")}"]')

                if (not session_option.is_selected()) and ("Your current session" not in label.text.strip()):
                    session_option.click() 
                    break
            
            # Submit the form to disconnect the selected session
            submit_button = driver.find_element(By.ID, "edit-submit")
            submit_button.click()
            
            return True  # Session handled, retry accessing the page
    except Exception:
        return False  # No session page detected or issue with handling

# Scrape the page with session handling retry
def navigate_with_session_handling(driver, url):
    while True:
        driver.get(url)
        
        # If no session page, proceed with scraping
        if url == driver.current_url:
            return True  # Successfully reached the target page
        
        # Check if we're on the session page
        if not handle_active_sessions(driver):
            return False