from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import time

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

try:
    # Instantiate the webdriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the website
    driver.get("https://ssn.trainings.dlabanalytics.com/")
    # Add a delay
    time.sleep(10)  # keep the window open for 10 seconds
except Exception as e:
    print(e)


driver.implicitly_wait(5)

try:
    #Use SSO to sign-in
    sso_button = driver.find_element(By.ID, "social-epam-idp")
    sso_button.click()

    driver.implicitly_wait(10)
except:
    driver.refresh()
    #Use SSO to sign-in
    sso_button = driver.find_element(By.ID, "social-epam-idp")
    sso_button.click()

    driver.implicitly_wait(10)


# Find the username field
username = driver.find_element(By.NAME, "loginfmt")  
username.send_keys("email@epam.com")  # replace "email@epam.com" with your epam.com email

next = driver.find_element(By.ID, "idSIButton9")
next.click()

### CONFIRM 2 STEP AUTHENTICATION IN THE APP
time.sleep(15)


for i in range(3):
    try:
        # Wait for the element to be clickable
        wait = WebDriverWait(driver, 10)
        settings = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/datalab-layout/datalab-navbar/mat-sidenav-container/mat-sidenav-content/div/datalab-resources/div/resources-grid/section/div/table/tbody/tr[2]/td/tr/td[7]")))

        # Click on the element
        settings.click()

        # If the click was successful, break the loop
        break
    except TimeoutException:
        # If the click was not successful, wait for 10 seconds before retrying
        time.sleep(10)
        

try:
    #Start the instance
    start_button = driver.find_element(By.XPATH, "/html/body/app-root/datalab-layout/datalab-navbar/mat-sidenav-container/mat-sidenav-content/div/datalab-resources/div/resources-grid/section/div/table/tbody/tr[2]/td/tr/td[7]/bubble-up/ul/div/li[1]/div/span")
    start_button.click()
except:
    pass

#Go to Jupyter Notebook
instance_button = driver.find_element(By.XPATH, "/html/body/app-root/datalab-layout/datalab-navbar/mat-sidenav-container/mat-sidenav-content/div/datalab-resources/div/resources-grid/section/div/table/tbody/tr[2]/td/tr/td[1]/span")
instance_button.click()
jup_link = driver.find_element(By.XPATH, "//a[@class='ellipsis none-select resources-url mat-tooltip-trigger']")
jup_link.click()

# Wait for the new tab to open
time.sleep(5)

# Switch to the Jupyter Notebook Home tab
driver.switch_to.window(driver.window_handles[1])

# Open the notebook if uploaded, upload if not and open
try:
    jup_nb = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div[2]/div[4]/div/a")
    jup_nb.click()
except:
    file_upload = driver.find_element(By.ID, "upload_span_input")
    file_upload.send_keys("Downloads/Final_DQE.ipynb")

    # Wait for the new tab to open
    time.sleep(5)

    jup_nb = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div[2]/div[4]/div/a")
    jup_nb.click()   

# Switch to the Jupyter Notebook tab
driver.switch_to.window(driver.window_handles[2])

#Open dropdown menu to run all
cell_menu = driver.find_element(By.ID, "celllink")
cell_menu.click()

time.sleep(15)

run_button = driver.find_element(By.ID, "run_all_cells")
run_button.click()

time.sleep(100)

# Close the browser
driver.quit()